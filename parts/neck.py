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
        headPivot=(0,0,0)):
        '''
        This is the constructor.
        '''
        super(Neck, self).__init__(name) 
        self._skullBind=skullBind
        self.addAttribute("anchor", anchor, attrType='str')
        self.addAttribute("headPivot", "{}".format(headPivot), attrType='str')
        self._splineName = splineName
        self.jointList = jointList

    def build(self):
        '''
        '''
        super(Neck, self).build()
        jointList = eval(self.jointList)
        headPivot = eval(self.getAttributeByName("headPivot").getValue())
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
        mc.parent(headGimbalGrp, mc.listRelatives(headGimbalCtrl, p=True)[0])
        mc.connectAttr("{}.t".format(headGimbalCtrl), "{}.t".format(headGimbalGrp), f=True)
        mc.connectAttr("{}.r".format(headGimbalCtrl), "{}.r".format(headGimbalGrp), f=True)
        mc.connectAttr("{}.rp".format(headGimbalCtrl), "{}.rp".format(headGimbalGrp), f=True)
        mc.connectAttr("{}.s".format(headGimbalCtrl), "{}.s".format(headGimbalGrp), f=True)
        #mc.scaleConstraint(headGimbalCtrl, headGimbalGrp)
        mc.xform(headNul, ws=True, t=mc.xform(self._skullBind, q=True, ws=True, t=True))
        if headPivot == (0,0,0):
            headPivot = rigrepo.libs.transform.getAveragePosition((jointList[-2], self._skullBind))
            mc.xform(headCtrl, ws=True, rp=headPivot)
            mc.xform(headGimbalCtrl, ws=True, rp=headPivot)
        else:
            mc.xform(headCtrl, relative=True, rp=headPivot)
            mc.xform(headGimbalCtrl, relative=True, rp=headPivot)
        mc.parent(headNul, neckCtrl) 
        mc.parent(clusters[2:], headGimbalGrp)
        mc.orientConstraint(headGimbalGrp, self.spline._endTwistNul, mo=1)

        # connect the scale to the skullBind
        '''
        jnt = mc.ls(mc.listConnections("{}.s".format(self._skullBind), plugs=False), type="joint")[0]
        skullScalePma = mc.createNode("plusMinusAverage", name="{}_scale_pma".format(self._skullBind))
        mc.connectAttr("{}.s".format(jnt), "{}.input3D[0]".format(skullScalePma), f=True)
        mc.connectAttr("{}.s".format(headGimbalGrp), "{}.input3D[1]".format(skullScalePma), f=True)
        mc.connectAttr("{}.output3D".format(skullScalePma), "{}.s".format(self._skullBind), f=True)
        '''
        skullOffset = mc.duplicate(self._skullBind, po=True, rr=True, name="{}_offset".format(self._skullBind))[0]
        mc.setAttr(skullOffset+'.v', 0)
        mc.parent(skullOffset, headGimbalGrp)
        mc.orientConstraint(skullOffset, self.spline._ikJointList[-1], mo=1)
        #mc.connectAttr(headGimbalGrp+'.s', self._skullBind+'.s', f=True)
        mc.scaleConstraint(headGimbalGrp, self._skullBind)

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
