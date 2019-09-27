'''
This is the spline base class.

Anything that uses a spline ik solver
should start with this class.
'''
import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.control as control
import rigrepo.libs.spline as spline
import rigrepo.libs.common as common
import rigrepo.libs.transform

class Neck(part.Part):
    '''
    '''
    def __init__(self, name, jointList, skullBind='skull_bind', splineName='neckIk', anchor="chest_top",
        headPivot=2.0):
        '''
        This is the constructor.
        '''
        super(Neck, self).__init__(name) 
        self._skullBind=skullBind
        self.addAttribute("anchor", anchor, attrType='str')
        self.addAttribute("headPivot", headPivot, attrType='float')
        self._splineName = splineName
        self.jointList = jointList

    def build(self):
        '''
        '''
        super(Neck, self).build()
        jointList = eval(self.jointList)
        headPivotValue = self.getAttributeByName("headPivot").getValue()
        self.spline = spline.SplineBase(jointList=jointList + [self._skullBind], splineName=self._splineName)
        self.spline.create()
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

        # create pivot attributes to use for moving the pivot and tangent heights.
        mc.addAttr(headCtrl, ln="pivotHeight", at="double", dv=0, min=0, max=4, keyable=False)
        mc.setAttr("{}.pivotHeight".format(headCtrl), headPivotValue)
        # tangent will be figured out later.
        #mc.addAttr(hipSwivelCtrl, ln="tangentHeight", at="double", dv=0, min=0, max=4, keyable=False)
        # get the aim axis
        tempNode = mc.createNode("transform", name="temp")
        mc.parent(tempNode, headGimbalGrp)
        mc.xform(tempNode, ws=True, matrix=matrix)
        aimAxis=rigrepo.libs.transform.getAimAxis(headGimbalGrp)
        mc.delete(tempNode)
        if '-' in aimAxis:
            headCtrlPivotPma = mc.createNode('plusMinusAverage', n='head_pivot_pma')
            mc.connectAttr('{}.pivotHeight'.format(headCtrl), '{}.input1D[1]'.format(headCtrlPivotPma), f=True)
            mc.setAttr('{}.input1D[0]'.format(headCtrlPivotPma), -1)
            mc.setAttr('{}.operation'.format(headCtrlPivotPma), 2)
            mc.connectAttr('{}.output1D'.format(headCtrlPivotPma), '{}.rotatePivot{}'.format(headCtrl, aimAxis.strip('-').capitalize()), f=True)
            # this should be setting the tangent, but we're using clusters. Still need time to 
            # figure this part out
            '''
            hipSwivelTangentPivotPma = mc.createNode('plusMinusAverage', n='hipSwivel_tangent_pivot_pma')
            mc.connectAttr('{}.tangentHeight'.format(hipSwivelCtrl), '{}.input1D[1]'.format(hipSwivelTangentPivotPma), f=True)
            mc.setAttr('{}.input1D[0]'.format(hipSwivelTangentPivotPma), -1)
            mc.setAttr('{}.operation'.format(hipSwivelTangentPivotPma), 2)
            mc.connectAttr('{}.input1D'.format(hipSwivelTangentPivotPma), '{}.rotatePivot{}'.format(clusters[1], aimAxis.strip('-').capitalize()), f=True)
            '''
        else:
            mc.connectAttr('{}.pivotHeight'.format(headCtrl), '{}.rotatePivot{}'.format(headCtrl, aimAxis.capitalize()), f=True)
            #mc.connectAttr('{}.tangentHeight'.format(hipSwivelCtrl), '{}.rotatePivot{}'.format(clusters[1], aimAxis.capitalize()), f=True)

        mc.parent(headNul, neckCtrl) 
        mc.parent(clusters[2:], headGimbalGrp)
        mc.orientConstraint(headGimbalGrp, self.spline._endTwistNul, mo=1)
        # make the offset joint for the skull
        skullOffset = mc.duplicate(self._skullBind, po=True, rr=True, name="{}_offset".format(self._skullBind))[0]
        mc.setAttr(skullOffset+'.v', 0)
        mc.parent(skullOffset, headGimbalGrp)
        mc.orientConstraint(skullOffset, self.spline._ikJointList[-1], mo=1)
        # connect the scale of the gimbal group to the scale of skull bind
        #mc.connectAttr(headGimbalGrp+'.s', self._skullBind+'.s', f=True)
        mc.scaleConstraint(headGimbalGrp, self._skullBind)
        mc.setAttr("{}.segmentScaleCompensate".format(self._skullBind), False)

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
        pass
