'''
This is the spline base class.

Anything that uses a spline ik solver
should start with this class.
'''
import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.control as control
import rigrepo.libs.spline as spline

class Spine(part.Part):
    '''
    '''
    def __init__(self, name, jointList, chestBind='chest_bind', hipsBind='hips_bind', splineName='spineIk'):
        '''
        This is the constructor.
        '''
        super(Spine, self).__init__(name) 
        self.spline = spline.SplineBase(jointList=jointList, splineName=splineName)
        self._hipsCtrl = str()
        self._hipSwivelCtrl = str()
        self._torsoCtrl = str()
        self._chestCtrl = str()
        self._chestTopCtrl = str()
        self._chestBind = chestBind
        self._hipsBind = hipsBind

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

        self.spline.create()
        jointList = self.spline.getJointList()

        # Hips
        hipsCtrlHierarchy = control.create(name="hips", 
                                                controlType="cube",
                                                hierarchy=['nul'])
        hipsCtrl = hipsCtrlHierarchy[-1]
        hipsNul = hipsCtrlHierarchy[0]

        matrix = mc.xform(jointList[0], q=True, ws=True, matrix=True)
        mc.xform(hipsNul, ws=True, matrix=matrix)

        # hip swivel
        ctrlHierarchy = control.create(name="hip_swivel", 
                                                controlType="diamond",
                                                hierarchy=['nul'])
        hipSwivelCtrl = ctrlHierarchy[-1]
        hipSwivelNul = ctrlHierarchy[0]

        matrix = mc.xform(hipsCtrl, q=True, ws=True, matrix=True)
        mc.xform(hipSwivelNul, ws=True, matrix=matrix)
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

        con = mc.pointConstraint(jointList[0], jointList[-1], torsoNul)
        mc.delete(con)
        mc.parent(torsoNul, hipsCtrl) 

        # chest 
        ctrlHierarchy = control.create(name="chest", 
                                            controlType="cube",
                                            hierarchy=['nul'])
        chestCtrl = ctrlHierarchy[-1]
        chestNul = ctrlHierarchy[0]

        con = mc.parentConstraint(self._chestBind, chestNul)
        mc.delete(con)
        mc.parent(chestNul, torsoCtrl)

        # chest top 
        ctrlHierarchy = control.create(name="chest_top", 
                                            controlType="diamond",
                                            hierarchy=['nul'])
        chestTopCtrl = ctrlHierarchy[-1]
        chestTopNul = ctrlHierarchy[0]

        con = mc.parentConstraint(jointList[-1], chestTopNul)
        mc.delete(con)
        mc.parent(chestTopNul, chestCtrl)

        mc.parent(clusters[2:], chestTopCtrl)
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
