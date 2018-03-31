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
        self.spline = spline.SplineBase(jointList=jointList, splineName=self._splineName)
        self.spline.create()

        # Hips
        hipsCtrlHierarchy = control.create(name="hips", 
                                                controlType="cube",
                                                hierarchy=['nul'])
        hipsCtrl = hipsCtrlHierarchy[-1]
        hipsNul = hipsCtrlHierarchy[0]

        matrix = mc.xform(self._hipsBind, q=True, ws=True, matrix=True)
        mc.xform(hipsNul, ws=True, matrix=matrix)

        # hip swivel
        ctrlHierarchy = control.create(name="hip_swivel", 
                                                controlType="cube",
                                                color=common.GREEN,
                                                hierarchy=['nul'])
        hipSwivelCtrl = ctrlHierarchy[-1]
        hipSwivelNul = ctrlHierarchy[0]

        matrix = mc.xform(hipsCtrl, q=True, ws=True, matrix=True)
        mc.xform(hipSwivelNul, ws=True, matrix=matrix)
        averagePos = rigrepo.libs.transform.getAveragePosition(jointList[0:3])
        mc.xform(hipSwivelNul, ws=True, t=averagePos)
        mc.parent(hipSwivelNul, hipsCtrl)
        clusters = self.spline._clusters
        mc.parent(clusters[0:2], hipSwivelCtrl)
        mc.orientConstraint(hipSwivelCtrl, self.spline._startTwistNul, mo=1)
    
        # Parent the entire ik group to the hips
        mc.parent(self.spline.getGroup(), hipsCtrl) 


        # torso 
        ctrlHierarchy = control.create(name="torso", 
                                            controlType="cube",
                                            hierarchy=['nul'])
        torsoCtrl = ctrlHierarchy[-1]
        torsoNul = ctrlHierarchy[0]
        
        rotation = mc.xform(hipsCtrl, q=True, ws=True, rotation=True)
        averagePos = rigrepo.libs.transform.getAveragePosition(jointList[:2])
        mc.xform(torsoNul, ws=True, rotation=rotation)
        mc.xform(torsoNul, ws=True, t=averagePos)
        mc.parent(torsoNul, hipsCtrl) 

        # chest 
        ctrlHierarchy = control.create(name="chest", 
                                            controlType="cube",
                                            color=common.GREEN,
                                            hierarchy=['nul'])
        chestCtrl = ctrlHierarchy[-1]
        chestNul = ctrlHierarchy[0]

        matrix = mc.xform(jointList[-3], q=True, ws=True, matrix=True)
        averagePos = rigrepo.libs.transform.getAveragePosition(jointList[-3:-1])
        mc.xform(chestNul, ws=True, matrix=matrix)
        mc.xform(chestNul, ws=True, t=averagePos)
        mc.parent(chestNul, torsoCtrl)

        # chest top 
        ctrlHierarchy = control.create(name="chest_top", 
                                             controlType="cube",
                                             hierarchy=['nul'])
        chestTopCtrl = ctrlHierarchy[-1]
        chestTopNul = ctrlHierarchy[0]

        matrix = mc.xform(self._chestBind, q=True, ws=True, matrix=True)
        mc.xform(chestTopNul, ws=True, matrix=matrix)
        mc.parent(chestTopNul, chestCtrl)

        mc.parent(clusters[2:], chestCtrl)
        mc.orientConstraint(chestTopCtrl, self.spline._endTwistNul, mo=1)

        self._hipsCtrl = hipsCtrl
        self._hipSwivelCtrl = hipSwivelCtrl
        self._torsoCtrl = torsoCtrl
        self._chestCtrl = chestCtrl
        self._chestTopCtrl = chestTopCtrl
        mc.parentConstraint(chestTopCtrl, self._chestBind, mo=1) 
        mc.connectAttr(chestTopCtrl+'.s', self._chestBind+'.s')

        mc.parentConstraint(hipsCtrl, self._hipsBind, mo=1) 
        mc.connectAttr(hipsCtrl+'.s', self._hipsBind+'.s')

        mc.parent(hipsNul, self.name)
        mc.hide(self.spline._group, clusters)

    def postBuild(self):
        '''
        '''
        #turn of the visibility of the ikfk system
