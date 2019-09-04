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

class Neck(part.Part):
    '''
    '''
    def __init__(self, name, jointList, skullBind='skull_bind', splineName='neckIk', anchor="chest_top"):
        '''
        This is the constructor.
        '''
        super(Neck, self).__init__(name) 
        self._skullBind=skullBind
        self.addAttribute("anchor", anchor, attrType='str')
        self._splineName = splineName
        self.jointList = jointList

    def build(self):
        '''
        '''
        super(Neck, self).build()
        jointList = eval(self.jointList)
        self.spline = spline.SplineBase(jointList=jointList + [self._skullBind], splineName=self._splineName)
        self.spline.create()

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
        headNul,headCtrl = control.create(name="head", 
                                          controlType="cube",
                                          color=common.BLUE,
                                          hierarchy=['nul'])

        # head gimabl control
        # head 
        headGimbalNul,headGimbalCtrl = control.create(name="head_gimbal", 
                                          controlType="cube",
                                          color=common.BLUE,
                                          hierarchy=['nul'],
                                          parent=headCtrl)

        clusters = self.spline._clusters
        con = mc.pointConstraint(jointList[0], self._skullBind, headNul)
        mc.delete(con)
        mc.parent(headNul, neckCtrl) 
        mc.parent(clusters[2:], headGimbalCtrl)
        mc.orientConstraint(headGimbalCtrl, self.spline._endTwistNul, mo=1)
        skullOffset = mc.duplicate(self._skullBind, po=True, rr=True, name="{}_offset".format(self._skullBind))[0]
        mc.parent(skullOffset, headGimbalCtrl)
        mc.orientConstraint(skullOffset, self.spline._ikJointList[-1], mo=1)
        #mc.connectAttr(headCtrl+'.s', self._skullBind+'.s')

        anchor = self.getAttributeByName('anchor').getValue()
        if mc.objExists(anchor):
            mc.parentConstraint(anchor, neckNul, mo=1)
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 

        mc.parent(neckNul, self.name)
        mc.hide(self.spline._group, clusters)

    def postBuild(self):
        '''
        '''
        pass
