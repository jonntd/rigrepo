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
import rigrepo.libs.attribute

class Spine(part.Part):
    '''
    '''
    def __init__(self, name, jointList, chestBind='chest_bind', hipsBind='hips_bind', splineName='spineIk', dataObj=None):
        '''
        This is the constructor.
        '''
        super(Spine, self).__init__(name, dataObj) 
        self._hipsCtrl = str()
        self._hipSwivelCtrl = str()
        self._torsoCtrl = str()
        self._chestCtrl = str()
        self._chestTopCtrl = str()
        self._chestIkCtrl = str()
        self._chestBind = chestBind
        self._hipsBind = hipsBind
        self.jointList = jointList
        self._splineName = splineName

    def getChestCtrl(self):
        return(self._chestCtrl)

    def getHipsCtrl(self):
        return(self._hipsCtrl)

    def getHipSwivelCtrl(self):
        return(self._hipSwivelCtrl)

    def build(self):
        '''
        '''
        super(Spine, self).build()

        jointList = eval(self.jointList)
        self.spline = spline.SplineBase(jointList=jointList + [self._chestBind], splineName=self._splineName)
        self.spline.create()

        # Hips
        hipsCtrlHierarchy = control.create(name="hips", 
                                                controlType="cube",
                                                hideAttrs=["sx", "sy", "sz","v"],
                                                hierarchy=['nul'])
        hipsCtrl = hipsCtrlHierarchy[-1]
        hipsNul = hipsCtrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(hipsCtrl, ["sx", "sy", "sz","v"])
        matrix = mc.xform(self._hipsBind, q=True, ws=True, matrix=True)
        mc.xform(hipsNul, ws=True, matrix=matrix)

        hipsGimbalCtrlHierarchy = control.create(name="hips_gimbal", 
                                                controlType="cube",
                                                hierarchy=['nul'],
                                                hideAttrs=["sx", "sy", "sz","v"],
                                                parent=hipsCtrl)
        hipsGimbalCtrl = hipsGimbalCtrlHierarchy[-1]
        hipsGimbalNul = hipsGimbalCtrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(hipsGimbalCtrl, ["sx", "sy", "sz","v"])
        mc.xform(hipsGimbalNul, ws=True, matrix=matrix)

        # hip swivel
        ctrlHierarchy = control.create(name="hip_swivel", 
                                                controlType="cube",
                                                color=common.GREEN,
                                                hideAttrs=["sx", "sy", "sz","v"],
                                                hierarchy=['nul'])
        hipSwivelCtrl = ctrlHierarchy[-1]
        hipSwivelNul = ctrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(hipSwivelCtrl, ["sx", "sy", "sz","v"])
        mc.xform(hipSwivelNul, ws=True, matrix=matrix)
        averagePos = rigrepo.libs.transform.getAveragePosition(jointList[0:3])
        mc.xform(hipSwivelNul, ws=True, t=averagePos)
        mc.parent(hipSwivelNul, hipsGimbalCtrl)
        clusters = self.spline._clusters
        mc.parent(clusters[0:2], hipSwivelCtrl)
        mc.orientConstraint(hipSwivelCtrl, self.spline._startTwistNul, mo=1)
    
        # Parent the entire ik group to the hips
        mc.parent(self.spline.getGroup(), hipsGimbalCtrl) 

        # torso 
        ctrlHierarchy = control.create(name="torso", 
                                            controlType="cube",
                                            hideAttrs=["sx", "sy", "sz", "v"],
                                            hierarchy=['nul'])
        torsoCtrl = ctrlHierarchy[-1]
        torsoNul = ctrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(torsoCtrl, ["sx", "sy", "sz", "v"])
        rotation = mc.xform(hipsCtrl, q=True, ws=True, rotation=True)
        averagePos = rigrepo.libs.transform.getAveragePosition(jointList[:2])
        mc.xform(torsoNul, ws=True, rotation=rotation)
        mc.xform(torsoNul, ws=True, t=averagePos)
        mc.parent(torsoNul, hipsGimbalCtrl) 

        # chest 
        ctrlHierarchy = control.create(name="chest", 
                                            controlType="cube",
                                            color=common.GREEN,
                                            hideAttrs=["sx", "sy", "sz", "v"],
                                            hierarchy=['nul'])
        chestCtrl = ctrlHierarchy[-1]
        chestNul = ctrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(chestCtrl, ["sx", "sy", "sz", "v"])
        matrix = mc.xform(jointList[-3], q=True, ws=True, matrix=True)
        averagePos = rigrepo.libs.transform.getAveragePosition(jointList[-3:-1])
        mc.xform(chestNul, ws=True, matrix=matrix)
        mc.xform(chestNul, ws=True, t=averagePos)
        mc.parent(chestNul, torsoCtrl)


        # chest IK
        ctrlHierarchy = control.create(name="chest_ik", 
                                            controlType="cube",
                                            color=common.GREEN,
                                            hideAttrs=["sx", "sy", "sz","v"],
                                            hierarchy=['nul'])
        chestIkCtrl = ctrlHierarchy[-1]
        chestIkNul = ctrlHierarchy[0]

        rigrepo.libs.attribute.lockAndHide(chestIkCtrl, ["sx", "sy", "sz","v"])

        mc.xform(chestIkNul, ws=True, matrix=matrix)
        mc.xform(chestIkNul, ws=True, t=averagePos)
        mc.parent(chestIkNul, chestCtrl)

        # chest top 
        ctrlHierarchy = control.create(name="chest_top", 
                                             controlType="cube",
                                             hideAttrs=["sx", "sy", "sz", "v"],
                                             hierarchy=['nul'])
        chestTopCtrl = ctrlHierarchy[-1]
        chestTopNul = ctrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(chestTopCtrl, ["sx", "sy", "sz", "v"])

        matrix = mc.xform(self._chestBind, q=True, ws=True, matrix=True)
        mc.xform(chestTopNul, ws=True, matrix=matrix)
        mc.parent(chestTopNul, chestIkCtrl)

        mc.parent(clusters[2:], chestIkCtrl)
        mc.orientConstraint(chestTopCtrl, self.spline._endTwistNul, mo=1)

        self._hipsCtrl = hipsCtrl
        self._hipSwivelCtrl = hipSwivelCtrl
        self._torsoCtrl = torsoCtrl
        self._chestCtrl = chestCtrl
        self._chestTopCtrl = chestTopCtrl
        self._chestIkCtrl = chestIkCtrl

        # Remove existing constraint on chestBind
        orientConstraint = mc.orientConstraint(self._chestBind, q=1)
        pointConstraint = mc.pointConstraint(self._chestBind, q=1)
        if orientConstraint:
            mc.delete(orientConstraint)
        if pointConstraint:
            mc.delete(pointConstraint)

        mc.pointConstraint(chestTopCtrl, self._chestBind, mo=1)
        mc.orientConstraint(chestTopCtrl, self._chestBind, mo=1)
        #mc.connectAttr(chestTopCtrl+'.s', self._chestBind+'.s')

        mc.parentConstraint(hipsGimbalCtrl, self._hipsBind, mo=1) 
        mc.connectAttr(hipsGimbalCtrl+'.s', self._hipsBind+'.s')

        mc.parent(hipsNul, self.name)
        mc.hide(self.spline._group, clusters)

    def postBuild(self):
        '''
        '''
        #turn of the visibility of the ikfk system
