'''
This is the spline base class.

Anything that uses a spline ik solver
should start with this class.
'''
import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.parts.part as part
import rigrepo.libs.control as control
import rigrepo.libs.spline as spline
import rigrepo.libs.common as common
import rigrepo.libs.transform

class Neck(part.Part):
    '''
    '''
    def __init__(self, name, jointList, skullBind='skull_bind', splineName='neckIk', anchor="chest_top", scaleFactor=1.0,
        headPivot=3.5):
        '''
        This is the constructor.
        '''
        super(Neck, self).__init__(name) 
        self._skullBind=skullBind
        self.addAttribute("anchor", anchor, attrType='str')
        self.addAttribute("headPivot", headPivot, attrType='float')
        self.addAttribute("scaleFactor", scaleFactor, attrType='float')
        self._splineName = splineName
        self.jointList = jointList

    def build(self):
        '''
        '''
        super(Neck, self).build()
        jointList = eval(self.jointList)
        headPivotValue = self.getAttributeByName("headPivot").getValue()
        scaleFactor = self.getAttributeByName('scaleFactor').getValue()
        self.spline = spline.SplineBase(jointList=jointList + [self._skullBind], splineName=self._splineName, scaleFactor=scaleFactor)
        self.spline.create()

        # get the name of the curveInfo node. This is hard coded to be this way in the
        # spline  code. If that changes, this will not work. We can change the code below
        # to use the API to get the length of the curve instead of this node, but for now, this 
        # is quicker because it's available already.
        spineCurveInfo = self._splineName+"_curveInfo"

        grp=mc.rename(self.name, "{}_grp".format(self.name))

        # Neck
        neckNul,neckOrt,neckCtrl = control.create(name="neck", 
                                          controlType="cube",
                                          color=common.BLUE,
                                          hierarchy=['nul',"ort"])

        matrix = mc.xform(jointList[0], q=True, ws=True, matrix=True)
        mc.xform(neckNul, ws=True, matrix=matrix)

        # Parent the entire ik group to the neck
        mc.parent(self.spline.getGroup(), neckCtrl) 

        # head 
        headNul, headCtrl = control.create(name="head", 
                                          controlType="cube",
                                          color=common.BLUE,
                                          hierarchy=['nul'])

        # head gimabl control
        # head 
        headGimbalNul, headGimbalCtrl = control.create(name="head_gimbal", 
                                          controlType="cube",
                                          color=common.BLUE,
                                          hierarchy=['nul'],
                                          parent=headCtrl)

        clusters = self.spline._clusters
        headGimbalGrp = mc.createNode("transform", n="head_gimbal_grp")
        # move the group into the same matrix as the control
        mc.xform(headGimbalGrp, ws=True, matrix=mc.xform(headGimbalCtrl, q=True, ws=True, matrix=True))
        # parent the group into the same space as the control
        mc.parent(headGimbalGrp, headGimbalCtrl)
        # constrain the gimbal group to the gimbal control
        mc.connectAttr("{}.rp".format(headCtrl), "{}.rp".format(headGimbalCtrl), f=True)
        #mc.connectAttr("{}.rp".format(headGimbalCtrl), "{}.rp".format(headGimbalGrp), f=True)
        #mc.pointConstraint(headGimbalCtrl, headGimbalGrp)
        #mc.orientConstraint(headGimbalCtrl, headGimbalGrp)
        #mc.scaleConstraint(headGimbalCtrl, headGimbalGrp)

        # make sure the nul is where the joint is
        mc.xform(headNul, ws=True, t=mc.xform(self._skullBind, q=True, ws=True, t=True))
        # tangent will be figured out later.
        #mc.addAttr(hipSwivelCtrl, ln="tangentHeight", at="double", dv=0, min=0, max=4, keyable=False)
         # make sure the nul is where the joint is
        mc.xform(headNul, ws=True, t=mc.xform(self._skullBind, q=True, ws=True, t=True))

        # create pivot attributes to use for moving the pivot and tangent heights.
        mc.addAttr(headCtrl, ln="pivotHeight", at="double", dv=0, min=0, max=10, keyable=False)
        mc.setAttr("{}.pivotHeight".format(headCtrl), headPivotValue)

        # create the remap node to use to remap the pivot height to the lenght of the curve
        headRemapNode = mc.createNode("remapValue", n="head_pivot_remap")

        # map the 0-10 to the length of the curve on the spine
        curveLength = mc.getAttr("{}.arcLength".format(spineCurveInfo))

        # set the max output value for the remap to be the length of the curve
        mc.setAttr("{}.outputMax".format(headRemapNode), curveLength)

        # set the input max
        mc.setAttr("{}.inputMax".format(headRemapNode), 10)

        # connect the slider for pivot to the input max
        mc.connectAttr("{}.pivotHeight".format(headCtrl), 
                        "{}.inputValue".format(headRemapNode), f=True)

        # get the aim axis
        headPivotNulGrp = mc.createNode("transform", name="headPivot_aim_nul")
        headPivotAimGrp = mc.createNode("transform", name="headPivot_aim_grp")
        headPivotDriver = mc.createNode("transform", name="headPivot_aim_drv")
        mc.parent(headPivotAimGrp, headPivotNulGrp)
        mc.parent(headPivotNulGrp, headGimbalGrp)
        mc.parent(headPivotDriver, headPivotAimGrp)
        mc.xform(headPivotNulGrp, ws=True, matrix=matrix)
        # get the aim axis
        aimAxis=rigrepo.libs.transform.getAimAxis(headGimbalGrp)
        mc.parent(headPivotNulGrp, headNul)
        vector = om.MVector(*mc.getAttr("{}.t".format(headPivotNulGrp)))
        vector.normalize()
        distanceValue = max(vector, key=abs)
        index = (vector.x, vector.y, vector.z).index(distanceValue)
        aimVector = list()
        for i in range(len(vector)):
            if i == index:
                aimVector.append(1)
            else:
                aimVector.append(0)

        # move the transform back to the skull
        mc.xform(headPivotNulGrp, ws=True, matrix=mc.xform(headCtrl, q=True, ws=True, matrix=True))
        mc.parent(headPivotDriver, headNul)
        mc.pointConstraint(headPivotAimGrp, headPivotDriver, mo=False)
        mc.orientConstraint(headPivotAimGrp, headPivotDriver, mo=False)

        mc.aimConstraint(neckCtrl,headPivotAimGrp, w=1, upVector=(0,0,0), aimVector=aimVector, wut="none")
        if '-' in aimAxis:
            headCtrlPivotMdl = mc.createNode('multDoubleLinear', n='head_pivot_mdl')
            mc.connectAttr('{}.outValue'.format(headRemapNode), '{}.input1'.format(headCtrlPivotMdl), f=True)
            mc.setAttr('{}.input2'.format(headCtrlPivotMdl), -1)
            mc.connectAttr('{}.output'.format(headCtrlPivotMdl), '{}.t{}'.format(headPivotAimGrp, aimAxis.strip('-')), f=True)
            mc.connectAttr('{}.t'.format(headPivotDriver), '{}.rotatePivot'.format(headCtrl), f=True)
        else:
            mc.connectAttr('{}.outValue'.format(headRemapNode), '{}.t{}'.format(headPivotAimGrp, aimAxis), f=True)
            mc.connectAttr('{}.t'.format(headPivotDriver), '{}.rotatePivot'.format(headCtrl), f=True)

        mc.parent(headNul, neckCtrl) 
        mc.parent(clusters[2:], headGimbalGrp)
        mc.orientConstraint(headGimbalGrp, self.spline._endTwistNul, mo=1)
        # make the offset joint for the skull
        skullOffset = mc.duplicate(self._skullBind, po=True, rr=True, name="{}_offset".format(self._skullBind))[0]
        mc.setAttr(skullOffset+'.v', 0)
        mc.parent(skullOffset, headGimbalGrp)
        mc.orientConstraint(skullOffset, self.spline._ikJointList[-1], mo=1)
        # connect the scale of the gimbal group to the scale of skull bind
        headScaleMdn = mc.createNode("multiplyDivide", n="head_scale_mdn")
        mc.connectAttr("{}.s".format(headCtrl), "{}.input1".format(headScaleMdn), f=True)
        mc.connectAttr("{}.s".format(headGimbalCtrl), "{}.input2".format(headScaleMdn), f=True)
        mc.connectAttr("{}.output".format(headScaleMdn), "{}.s".format(self._skullBind), f=True)

        anchor = self.getAttributeByName('anchor').getValue()
        if mc.objExists(anchor):
            mc.parentConstraint(anchor, neckNul, mo=1)
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 

        mc.parent(neckNul, grp)
        mc.hide(self.spline._group, clusters)

    def postBuild(self):
        '''
        '''
        # Something is cause flipping with the decompose unless this rotate order is changed.
        # Needs to be debugged, setting here for now
        mc.setAttr("neckIk_end_twist.rotateOrder", 5)
