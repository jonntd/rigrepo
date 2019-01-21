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

class Tongue(part.Part):
    '''
    '''
    def __init__(self, name, jointList, splineName='tongueIk', anchor="jaw"):
        '''
        This is the constructor.
        '''
        super(Tongue, self).__init__(name) 
        self.addAttribute("anchor", anchor, attrType='str')
        self._splineName = splineName
        self.jointList = jointList

    def build(self):
        '''
        '''
        super(Tongue, self).build()
        jointList = eval(self.jointList)
        self.spline = spline.SplineBase(jointList=jointList, splineName=self._splineName)
        self.spline.create()

        # Tongue Base
        tonugeBaseNul, tonugeBaseCtrl = control.create(name="tonuge_base", 
                                          controlType=None,
                                          color=common.RED,
                                          hierarchy=['nul'])

        matrix = mc.xform(jointList[0], q=True, ws=True, matrix=True)
        mc.xform(tonugeBaseNul, ws=True, matrix=matrix)

        # Parent the entire ik group to the neck
        mc.parent(self.spline.getGroup(), tonugeBaseCtrl) 

        # tongue Mid
        tonugeMidNul, tonugeMidCtrl = control.create(name="tonuge_mid", 
                                          controlType=None,
                                          color=common.RED,
                                          hierarchy=['nul'])

        # move the middle control between the last the middle joints
        mc.delete(mc.parentConstraint(jointList[-2], jointList[1], tonugeMidNul))

        mc.parent(tonugeMidNul, tonugeBaseCtrl) 

        # tongue Tip
        tonugeTipNul, tonugeTipCtrl = control.create(name="tonuge_tip", 
                                          controlType=None,
                                          color=common.RED,
                                          hierarchy=['nul'])

        # make the tongue tip matches the last joint in the chain
        matrix=mc.xform(jointList[-1], q=True, ws=True, matrix=True)
        mc.xform(tonugeTipNul, ws=True, matrix=matrix)

        clusters = self.spline._clusters
        mc.parent(tonugeTipNul, tonugeMidCtrl) 
        mc.parent(clusters[2:], tonugeTipCtrl)
        mc.orientConstraint(tonugeTipCtrl, self.spline._endTwistNul, mo=1)
        #mc.parentConstraint(tonugeTipCtrl, self._skullBind, mo=1)
        #mc.connectAttr(headCtrl+'.s', self._skullBind+'.s')

        anchor = self.getAttributeByName('anchor').getValue()
        if mc.objExists(anchor):
            mc.parentConstraint(anchor, tonugeBaseNul, mo=1)
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 

        mc.parent(tonugeBaseNul, self.name)
        mc.hide(self.spline._group, clusters)

    def postBuild(self):
        '''
        '''
        pass
