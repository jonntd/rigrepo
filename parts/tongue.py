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
        tongueBaseNul, tongueBaseCtrl = control.create(name="tongue_base",
                                          controlType=None,
                                          color=common.RED,
                                          hierarchy=['nul'],
                                          type='face')

        # Hook up scale
        scale_nul = mc.createNode('transform', p=jointList[0], n='tongue_scale_nul')
        mc.parent(scale_nul, mc.listRelatives(jointList[0], p=1)[0])
        mc.parent(jointList[0], scale_nul)
        mc.connectAttr(tongueBaseCtrl+'.s', scale_nul+'.s')
        mc.setAttr(jointList[0]+'.segmentScaleCompensate', 0)

        matrix = mc.xform(jointList[0], q=True, ws=True, matrix=True)
        mc.xform(tongueBaseNul, ws=True, matrix=matrix)

        # Parent the entire ik group to the neck
        mc.parent(self.spline.getGroup(), tongueBaseCtrl)

        # tongue Mid
        tongueMidNul, tongueMidCtrl = control.create(name="tongue_mid",
                                          controlType=None,
                                          color=common.RED,
                                          hideAttrs=['sx', 'sy', 'sz', 'v'],
                                          hierarchy=['nul'],
                                          type='face')

        # move the middle control between the last the middle joints
        mc.delete(mc.parentConstraint(jointList[-2], jointList[1], tongueMidNul))

        mc.parent(tongueMidNul, tongueBaseCtrl)

        # tongue Tip
        tongueTipNul, tongueTipCtrl = control.create(name="tongue_tip",
                                          controlType=None,
                                          color=common.RED,
                                          hideAttrs=['sx', 'sy', 'sz', 'v'],
                                          hierarchy=['nul'],
                                          type='face')

        # make the tongue tip matches the last joint in the chain
        matrix=mc.xform(jointList[-1], q=True, ws=True, matrix=True)
        mc.xform(tongueTipNul, ws=True, matrix=matrix)

        clusters = self.spline._clusters
        mc.parent(tongueTipNul, tongueMidCtrl)
        mc.parent(clusters[2:], tongueTipCtrl)
        mc.orientConstraint(tongueTipCtrl, self.spline._endTwistNul, mo=1)
        #mc.parentConstraint(tongueTipCtrl, self._skullBind, mo=1)
        #mc.connectAttr(headCtrl+'.s', self._skullBind+'.s')

        anchor = self.getAttributeByName('anchor').getValue()
        if mc.objExists(anchor):
            mc.parentConstraint(anchor, tongueBaseNul, mo=1)
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 

        mc.parent(tongueBaseNul, self.name)
        mc.hide(self.spline._group, clusters)

    def postBuild(self):
        '''
        '''
        pass
