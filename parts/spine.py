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
    def __init__(self, name, jointList, chestBind='chest_bind', hipsBind='hips_bind', 
                splineName='spineIk', dataObj=None, createBendySpline=False, 
                hipSwivelPivot=3.5, chestPivotHeight=4.5):
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
        self.addAttribute("chestPivot", hipSwivelPivot, attrType=float)

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

        # store the joint list
        jointList = eval(self.jointList)

        # initialize the spline class
        self.spline = spline.SplineBase(jointList=jointList + [self._chestBind], 
                                        splineName=self._splineName)
        # create the spline
        self.spline.create()

        # get the name of the curveInfo node. This is hard coded to be this way in the
        # spline  code. If that changes, this will not work. We can change the code below
        # to use the API to get the length of the curve instead of this node, but for now, this 
        # is quicker because it's available already.
        spineCurveInfo = self._splineName+"_curveInfo"


        # get the attributes from the user
        geometry = self.getAttributeByName("geometry").getValue()
        bendyCurve = self.getAttributeByName("bendyCurve").getValue()
        createBendySpline = self.getAttributeByName("createBendySpline").getValue()
        hipSwivelPivotValue = self.getAttributeByName("hipSwivelPivot").getValue()
        chestPivotValue = self.getAttributeByName("chestPivot").getValue()
        # Hips
        hipsCtrlHierarchy = control.create(name="hips", 
                                                controlType="cube",
                                                hideAttrs=["sx", "sy", "sz","v"],
                                                hierarchy=['nul'])
        hipsCtrl = hipsCtrlHierarchy[-1]
        hipsNul = hipsCtrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(hipsCtrl, ["sx", "sy", "sz","v"])
        hipMatrix = mc.xform(self._hipsBind, q=True, ws=True, matrix=True)
        mc.xform(hipsNul, ws=True, matrix=hipMatrix)

        hipsGimbalCtrlHierarchy = control.create(name="hips_gimbal", 
                                                controlType="cube",
                                                hierarchy=['nul'],
                                                hideAttrs=["sx", "sy", "sz","v"],
                                                parent=hipsCtrl)
        hipsGimbalCtrl = hipsGimbalCtrlHierarchy[-1]
        hipsGimbalNul = hipsGimbalCtrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(hipsGimbalCtrl, ["sx", "sy", "sz","v"])
        mc.xform(hipsGimbalNul, ws=True, matrix=hipMatrix)

        # hip swivel
        ctrlHierarchy = control.create(name="hip_swivel", 
                                                controlType="cube",
                                                color=common.GREEN,
                                                hideAttrs=["sx", "sy", "sz","v"],
                                                hierarchy=['nul'])
        hipSwivelCtrl = ctrlHierarchy[-1]
        hipSwivelNul = ctrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(hipSwivelCtrl, ["sx", "sy", "sz","v"])
        mc.xform(hipSwivelNul, ws=True, matrix=hipMatrix)
        averagePos = rigrepo.libs.transform.getAveragePosition([jointList[0]])
        mc.xform(hipSwivelNul, ws=True, t=mc.xform(jointList[0], q=True, ws=True, t=True))

        mc.parent(hipSwivelNul, hipsGimbalCtrl)
        clusters = self.spline._clusters

        # create a group that is driven by the ctrl
        hipSwivelGrp = mc.createNode("transform", n="hips_swivel_grp")

        # move the group into the same matrix as the control
        mc.xform(hipSwivelGrp, ws=True, matrix=mc.xform(hipSwivelCtrl, 
                                                        q=True, ws=True, matrix=True))
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
        matrix = mc.xform(self._chestBind, q=True, ws=True, matrix=True)
        
        mc.xform(chestNul, ws=True, matrix=matrix)
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
        mc.parent(chestIkNul, chestCtrl)
        # connect the rotate pivots so the pivots for these two controls are in the same location.
        mc.connectAttr("{}.rp".format(chestCtrl),"{}.rp".format(chestIkCtrl), f=True)

        # chest top 
        ctrlHierarchy = control.create(name="chest_top", 
                                             controlType="cube",
                                             hideAttrs=["sx", "sy", "sz", "v"],
                                             hierarchy=['nul'])
        chestTopCtrl = ctrlHierarchy[-1]
        chestTopNul = ctrlHierarchy[0]
        rigrepo.libs.attribute.lockAndHide(chestTopCtrl, ["sx", "sy", "sz", "v"])

        mc.xform(chestTopNul, ws=True, matrix=matrix)
        mc.parent(chestTopNul, chestIkCtrl)

        mc.parent(clusters[2:], chestIkCtrl)
        chestTopGrp = mc.createNode("transform", name="chest_top_grp")
        mc.xform(chestTopGrp, ws=True, matrix=matrix)
        mc.parent(chestTopGrp, chestTopCtrl)
        mc.orientConstraint(chestTopGrp, self.spline._endTwistNul, mo=1)

        # ==========================================================================================
        # chest pivot
        # create pivot attributes to use for moving the pivot and tangent heights.
        mc.addAttr(chestCtrl, ln="pivotHeight", at="double", dv=0, min=0, max=10, keyable=False)
        mc.setAttr("{}.pivotHeight".format(chestCtrl), chestPivotValue)

        # create the remap node to use to remap the pivot height to the lenght of the curve
        chestRemapNode = mc.createNode("remapValue", n="chest_pivot_remap")

        # map the 0-10 to the length of the curve on the spine
        curveLength = mc.getAttr("{}.arcLength".format(spineCurveInfo))

        # set the max output value for the remap to be the length of the curve
        mc.setAttr("{}.outputMax".format(chestRemapNode), curveLength)

        # set the input max
        mc.setAttr("{}.inputMax".format(chestRemapNode), 10)

        # connect the slider for pivot to the input max
        mc.connectAttr("{}.pivotHeight".format(chestCtrl), 
                        "{}.inputValue".format(chestRemapNode), f=True)

        # get the aim axis
        chestPivotNulGrp = mc.createNode("transform", name="chestPivot_aim_nul")
        chestPivotAimGrp = mc.createNode("transform", name="chestPivot_aim_grp")
        chestPivotDriver = mc.createNode("transform", name="chestPivot_aim_drv")
        mc.parent(chestPivotAimGrp, chestPivotNulGrp)
        mc.parent(chestPivotNulGrp, chestCtrl)
        mc.parent(chestPivotDriver, chestPivotAimGrp)
        mc.xform(chestPivotNulGrp, ws=True, matrix=matrix)
        mc.xform(chestPivotDriver, ws=True, matrix=hipMatrix)
        aimAxis, aimVector = self._getDistanceVector(mc.getAttr('{}.t'.format(chestPivotDriver))[0])
        mc.parent(chestPivotNulGrp, chestNul)

        # move the transform back to the skull
        mc.xform(chestPivotDriver, ws=True, matrix=matrix)
        mc.xform(chestPivotNulGrp, ws=True, t=mc.xform(chestNul, q=True, ws=True, t=True))
        mc.orientConstraint(chestNul, chestPivotNulGrp)
        mc.parent(chestPivotDriver, chestNul)
        mc.pointConstraint(chestPivotAimGrp, chestPivotDriver)
        mc.orientConstraint(chestPivotAimGrp, chestPivotDriver)

        if '-' in aimAxis:
            chestCtrlPivotMdl = mc.createNode('multDoubleLinear', n='chest_pivot_mdl')
            mc.connectAttr('{}.outValue'.format(chestRemapNode), '{}.input1'.format(chestCtrlPivotMdl), f=True)
            mc.setAttr('{}.input2'.format(chestCtrlPivotMdl), -1)
            mc.connectAttr('{}.output'.format(chestCtrlPivotMdl), '{}.t{}'.format(chestPivotAimGrp, aimAxis.strip('-')), f=True)
            mc.connectAttr('{}.t'.format(chestPivotDriver), '{}.rotatePivot'.format(chestCtrl), f=True)
        else:
            mc.connectAttr('{}.outValue'.format(chestRemapNode), '{}.t{}'.format(chestPivotAimGrp, aimAxis), f=True)
            mc.connectAttr('{}.t'.format(chestPivotDriver), '{}.rotatePivot'.format(chestCtrl), f=True)


        # ==========================================================================================
        # hip swivel pivot

        # create pivot attributes to use for moving the pivot and tangent heights.
        mc.addAttr(hipSwivelCtrl, ln="pivotHeight", at="double", dv=0, 
                    min=0, max=10, keyable=False)
        mc.setAttr("{}.pivotHeight".format(hipSwivelCtrl), hipSwivelPivotValue)

        # create the remap node to use to remap the pivot height to the lenght of the curve
        hipSwivelRemapNode = mc.createNode("remapValue", n="hipSwivel_pivot_remap")

        # set the max output value for the remap to be the length of the curve
        mc.setAttr("{}.outputMax".format(hipSwivelRemapNode), curveLength)

        # set the input max
        mc.setAttr("{}.inputMax".format(hipSwivelRemapNode), 10)

        # connect the slider for pivot to the input max
        mc.connectAttr("{}.pivotHeight".format(hipSwivelCtrl), 
                        "{}.inputValue".format(hipSwivelRemapNode), f=True)

        # get the aim axis
        tempNode = mc.createNode("transform", name="temp")
        mc.parent(tempNode, hipSwivelGrp)
        mc.xform(tempNode, ws=True, matrix=matrix)
        aimAxis=rigrepo.libs.transform.getAimAxis(hipSwivelGrp)
        mc.delete(tempNode)
        if '-' in aimAxis:
            hipSwivelPivotMdl = mc.createNode('multDoubleLinear', n='hipSwivel_pivot_pma')

            mc.connectAttr("{}.outValue".format(hipSwivelRemapNode), 
                '{}.input1'.format(hipSwivelPivotMdl), f=True)

            mc.setAttr('{}.input2'.format(hipSwivelPivotMdl), -1)

            mc.connectAttr('{}.output'.format(hipSwivelPivotMdl), 
                '{}.rotatePivot{}'.format(hipSwivelCtrl, aimAxis.strip('-').capitalize()), f=True)
        else:
            mc.connectAttr("{}.outValue".format(hipSwivelRemapNode), 
                '{}.rotatePivot{}'.format(hipSwivelCtrl, aimAxis.capitalize()), f=True)

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

    def _getDistanceVector(self, distance):
        '''
        '''
        distanceValue = max(distance, key=abs)
        index = distance.index(distanceValue)
        attr = ["x","y","z"][index]
        value = round(distance[index], 4)
        if attr == "x":
            if value < 0:
                attr = "-x"
                vector = [-1,0,0]
            else:
                vector = [1,0,0]
        elif attr == "y":
            if value < 0:
                attr = "-y"
                vector = [0,-1,0]
            else:
                vector = [0,1,0]
        elif attr == "z":
            if value < 0:
                attr = "-z"
                vector = [0,0,-1]
            else:
                vector = [0,0,1]

        return (attr, vector)

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