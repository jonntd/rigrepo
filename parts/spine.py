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
    def __init__(self, name, jointList, chestBind='chest_bind', hipsBind='hips_bind', splineName='spineIk', dataObj=None, createBendySpline=False,
        hipSwivelPivot=2.5):
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
        self.addAttribute("geometry", "body_geo", attrType=str)
        self.addAttribute("bendyCurve", "spine_curve", attrType=str)
        self.addAttribute("createBendySpline", True, attrType=bool)
        self.addAttribute("hipSwivelPivot", hipSwivelPivot, attrType=float)

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
        # get the attributes from the user
        geometry = self.getAttributeByName("geometry").getValue()
        bendyCurve = self.getAttributeByName("bendyCurve").getValue()
        createBendySpline = self.getAttributeByName("createBendySpline").getValue()
        hipSwivelPivotValue = self.getAttributeByName("hipSwivelPivot").getValue()

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
        averagePos = rigrepo.libs.transform.getAveragePosition([jointList[0]])
        mc.xform(hipSwivelNul, ws=True, t=mc.xform(jointList[0], q=True, ws=True, t=True))

        mc.parent(hipSwivelNul, hipsGimbalCtrl)
        clusters = self.spline._clusters
        # create a group that is driven by the ctrl
        hipSwivelGrp = mc.createNode("transform", n="hips_swivel_grp")
        # move the group into the same matrix as the control
        mc.xform(hipSwivelGrp, ws=True, matrix=mc.xform(hipSwivelCtrl, q=True, ws=True, matrix=True))
        # parent the group into the same space as the control
        mc.parent(hipSwivelGrp, hipSwivelCtrl)
        mc.parent(clusters[0:2], hipSwivelGrp)
        mc.orientConstraint(hipSwivelGrp, self.spline._startTwistNul, mo=1)
    
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
        chestTopGrp = mc.createNode("transform", name="chest_top_grp")
        mc.xform(chestTopGrp, ws=True, matrix=matrix)
        mc.parent(chestTopGrp, chestTopCtrl)
        mc.orientConstraint(chestTopGrp, self.spline._endTwistNul, mo=1)

        # create pivot attributes to use for moving the pivot and tangent heights.
        mc.addAttr(hipSwivelCtrl, ln="pivotHeight", at="double", dv=0, min=0, max=4, keyable=False)
        mc.setAttr("{}.pivotHeight".format(hipSwivelCtrl), hipSwivelPivotValue)
        # tangent will be figured out later.
        #mc.addAttr(hipSwivelCtrl, ln="tangentHeight", at="double", dv=0, min=0, max=4, keyable=False)

        # get the aim axis
        tempNode = mc.createNode("transform", name="temp")
        mc.parent(tempNode, hipSwivelGrp)
        mc.xform(tempNode, ws=True, matrix=matrix)
        aimAxis=rigrepo.libs.transform.getAimAxis(hipSwivelGrp)
        mc.delete(tempNode)
        if '-' in aimAxis:
            hipSwivelPivotPma = mc.createNode('plusMinusAverage', n='hipSwivel_pivot_pma')
            mc.connectAttr('{}.pivotHeight'.format(hipSwivelCtrl), '{}.input1D[1]'.format(hipSwivelPivotPma), f=True)
            mc.setAttr('{}.input1D[0]'.format(hipSwivelPivotPma), -1)
            mc.setAttr('{}.operation'.format(hipSwivelPivotPma), 2)
            mc.connectAttr('{}.output1D'.format(hipSwivelPivotPma), '{}.rotatePivot{}'.format(hipSwivelCtrl, aimAxis.strip('-').capitalize()), f=True)
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
            mc.connectAttr('{}.pivotHeight'.format(hipSwivelCtrl), '{}.rotatePivot{}'.format(hipSwivelCtrl, aimAxis.capitalize()), f=True)
            #mc.connectAttr('{}.tangentHeight'.format(hipSwivelCtrl), '{}.rotatePivot{}'.format(clusters[1], aimAxis.capitalize()), f=True)

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

        mc.pointConstraint(chestTopGrp, self._chestBind, mo=1)
        mc.orientConstraint(chestTopGrp, self._chestBind, mo=1)
        #mc.connectAttr(chestTopCtrl+'.s', self._chestBind+'.s')

        mc.parentConstraint(hipSwivelGrp, self._hipsBind, mo=1) 
        mc.connectAttr(hipSwivelGrp+'.s', self._hipsBind+'.s')

        mc.parent(hipsNul, self.name)
        mc.hide(self.spline._group, clusters)
        
        if createBendySpline and mc.objExists(bendyCurve):
            bindmeshGeometry, follicleList, controlHieracrchyList, bendJointList = self.__buildCurveRig(bendyCurve, name='{}_bend'.format(self.getName()),parent=self.name)

            if mc.objExists(geometry):
                #deform the lid bindmesh with the lid curve using a wire deformer.
                wireDeformer = mc.wire(geometry, gw=False, en=1.00, ce=0.00, li=0.00, 
                        w=bendyCurve, name="{}_wire".format(bendyCurve))[0]
                baseCurveJointList=list()
                i = 0
                for jnt, controlList in zip(bendJointList, controlHieracrchyList):
                    # create the joint that we will use later to deform the base wire.
                    baseCurveJoint = mc.joint(name=jnt.replace("_jnt","_baseCurve_jnt"))
                    baseCurveJointList.append(baseCurveJoint)
                    # hide the base curve joint. Then parent it under the null node
                    mc.setAttr("{}.v".format(baseCurveJoint), 0)
                    mc.parent(baseCurveJoint, controlList[1])
                    mc.setAttr("{}.t".format(baseCurveJoint), 0, 0, 0)

                baseCurve = "{}BaseWire".format(bendyCurve)
                mc.parent([bendyCurve,baseCurve], self.name)
                baseCurveSkin = mc.skinCluster(*[baseCurveJointList]+mc.ls(baseCurve), 
                                            n="{}_skinCluster".format(baseCurve),
                                            tsb=True)[0]

                # set the default values for the wire deformer
                mc.setAttr("{}.rotation".format(wireDeformer), 0)
                mc.setAttr("{}.dropoffDistance[0]".format(wireDeformer), 100)

            bindMeshSkin = mc.skinCluster(*jointList+[self._hipsBind,self._chestBind]+mc.ls(bindmeshGeometry), 
                                                n="{}_skinCluster".format(bindmeshGeometry),
                                                tsb=True)[0]

            mc.skinPercent(bindMeshSkin , '{}.vtx[0:3]'.format(bindmeshGeometry), transformValue=[(self._hipsBind, 1.0), (jointList[0], 0.0)])
            mc.skinPercent(bindMeshSkin , '{}.vtx[4:7]'.format(bindmeshGeometry),  transformValue=[(jointList[0], 0.0), (jointList[1], 0.5), (jointList[2],0.0)])
            mc.skinPercent(bindMeshSkin , '{}.vtx[8:11]'.format(bindmeshGeometry), transformValue=[(jointList[3], 1.0), (jointList[1], 0.0)])
            mc.skinPercent(bindMeshSkin , '{}.vtx[12:15]'.format(bindmeshGeometry), transformValue=[(jointList[2], 0.0), (jointList[4], 0.5), (self._chestBind, .5)])
            mc.skinPercent(bindMeshSkin , '{}.vtx[16:19]'.format(bindmeshGeometry), transformValue=[(self._chestBind, 1.0), (jointList[1], 0.0), (jointList[2],0.0)])
        
    def postBuild(self):
        '''
        '''
        #turn of the visibility of the ikfk system

    def __buildCurveRig(self, curve, name='spine_bend', parent=None):
        '''
        This will build a rig setup based on the curve that is passed in.

        :param joints: NurbsCurve name you want to build the rig on.
        :type joints: list |tuple

        :param name: This will be used to name the control hierachy and joints in the rig.
        :type name: str

        :return: This method will return the data needed to make adjustments to rig.
        :rtype: tuple
        '''

        # If the name passed in doesn't exist, we will create a transform as the parent group
        # for the rig.
        if not mc.objExists(name):
            mc.createNode("transform", n=name)
        # create the bindmesh 
        #
        # follicleList = (follicle transform, follicle shape) 
        # bindmeshGeometry = geometry name of bindmesh
        #
        bindmeshGeometry, follicleList = rigrepo.libs.bindmesh.createFromCurve(name, curve)
        # emptry list to append controls to in the loop
        controlHieracrchyList = list()
        jointList = list()

        # loop through and create controls on the follicles so we have controls to deform the wire.
        for follicle in follicleList:
            # get the follicle transform so we can use it to parent the control to it.
            follicleIndex = follicleList.index(follicle)
            # create the control with a large enough hierarchy to create proper SDK's
            ctrlHierarchy = rigrepo.libs.control.create(name="{}_{}".format(name, follicleIndex), 
                controlType="circle", 
                hierarchy=['nul','ort','def_auto'],
                color= rigrepo.libs.common.YELLOW, 
                parent=follicle)

            rigrepo.libs.attribute.lockAndHide(ctrlHierarchy[-1], ["rx", "ry", "rz","sx", "sy", "sz"])

            # create the joint that will drive the curve.
            jnt = mc.joint(n="{}_{}_jnt".format(name, follicleIndex))
            # make sure the joint is in the correct space
            mc.setAttr("{}.translate".format(jnt), 0,0,0)
            mc.setAttr("{}.rotate".format(jnt), 0,0,0)
            mc.setAttr("{}.drawStyle".format(jnt),2)
            mc.setAttr("{}.displayHandle".format(ctrlHierarchy[-1]), 1)
            #mc.delete(mc.listRelatives(ctrlHierarchy[-1], c=True, shapes=True)[0])

            # zero out the nul for the control hierarchy so it's in the correct position.
            mc.setAttr("{}.translate".format(ctrlHierarchy[0]), 0,0,0)
            #mc.setAttr("{}.rotate".format(ctrlHierarchy[0]), 0,0,0)
            # set the visibility of the shape node for the follicle to be off.
            # append the control and the follicle transform to their lists
            controlHieracrchyList.append(ctrlHierarchy)
            jointList.append(jnt)

            # since it's the spine. We're not using the first and last controls. 
            # so we will untag them and hide them for now.
            if follicle == follicleList[0] or follicle == follicleList[-1]:
                if mc.objExists("{}.__control__".format(ctrlHierarchy[-1])):
                    mc.setAttr("{}.v".format(ctrlHierarchy[-1]),0)

        # This will parent all of the data for the rig to the system group "name"
        for data in (bindmeshGeometry, follicleList):
            mc.parent(data, name)

        #mc.pointConstraint(controlHieracrchyList[0][-1],controlHieracrchyList[2][-1], controlHieracrchyList[1][2], mo=True)
        #mc.pointConstraint(controlHieracrchyList[2][-1],controlHieracrchyList[4][-1], controlHieracrchyList[3][2], mo=True)

        # If parent the parent is passed in we will parent the system to the parent.
        if parent:
            if not mc.objExists(parent):
                mc.warning('Created the system but the current parent "{}" does not exist in the \
                    current Maya session.'.format(parent))
            else:
                mc.parent(name, parent)

        # create the skinCluster for the curve
        mc.skinCluster(*jointList + [curve], tsb=True, name="{}_skinCluster".format(curve))

        # set the visibility of the bindmesh.
        mc.setAttr("{}.v".format(bindmeshGeometry), 0 )
        mc.setAttr("{}.v".format(curve), 0 )
        return bindmeshGeometry, follicleList, controlHieracrchyList, jointList