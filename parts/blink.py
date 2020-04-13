'''
This is not broken up into pieces yet. Just putting it here to hace access and work on it.
PLEASE DON'T MESS WITH THIS FILE!
'''
import maya.cmds as mc
import numpy
import maya.api.OpenMaya as om
import rigrepo.libs.curve 
import rigrepo.libs.control 
import rigrepo.libs.transform
import rigrepo.libs.common
import rigrepo.libs.attribute
import rigrepo.libs.skinCluster
import rigrepo.libs.cluster
import rigrepo.libs.weights
import rigrepo.parts.part as part
import rigrepo.libs.bindmesh as bindmesh


class Blink(part.Part):
    def __init__(self, name, side="l", anchor="face_upper", dataObj=None):
        '''
        '''
        # Create the attributes that the user will be able to change on the part
        # that will affect the build.
        super(Blink, self).__init__(name)
        self.addAttribute("side", side, attrType=str)
        self.addAttribute("anchor", anchor, attrType=str)
        self.addAttribute("eyeCenterJoint", "eyeSocket_{}_bind".format(side), attrType=str)
        self.addAttribute("lowerCurve", "blinkLower_{}_curve".format(side), attrType=str)
        self.addAttribute("upperCurve", "blinkUpper_{}_curve".format(side), attrType=str)
        self.addAttribute("lidCurve", "lid_{}_curve".format(side), attrType=str)
        self.addAttribute("geometry", "body_geo", attrType=str)
        self.addAttribute("eyeGeometry", "eye_{}_geo".format(side), attrType=str)

        self.controlGroup = "{}_controls".format(self.name)
        self._skinClusters = list()

    def setup(self):
        '''
        This will create default nodes that should exists in the scene for the part to build.
        '''
        super(Blink, self).setup()

        for node in [self.controlGroup]:
            if not mc.objExists(node):
                mc.createNode("transform", name=node)

        # parent the curve groups to the rig group
        lowerNeutralCurve = self.getAttributeByName('lowerCurve').getValue()
        upperNeutralCurve = self.getAttributeByName('upperCurve').getValue()

        for node in (lowerNeutralCurve,upperNeutralCurve):
            parent = mc.listRelatives(node, p=True)[0]
            if not mc.listRelatives(parent, p=True):
                mc.parent(parent, self.rigGroup)

    def build(self):
        '''
        This will run the build of the eye rig.
        '''
        super(Blink, self).build()
        eyeCenter = self.getAttributeByName("eyeCenterJoint").getValue()
        side = self.getAttributeByName("side").getValue()
        anchor = self.getAttributeByName("anchor").getValue()
        geometry = self.getAttributeByName("geometry").getValue()
        eyeGeometry = self.getAttributeByName("eyeGeometry").getValue()
        upperCurve = self.getAttributeByName("upperCurve").getValue()
        lowerCurve = self.getAttributeByName("lowerCurve").getValue()
        lidCurve = self.getAttributeByName("lidCurve").getValue()

        # CREATE THE CONTROLS FOR THE BLINK RIG.
        # Create the eyeSocket control
        eyeSocketNul, eyeSocketCtrl = rigrepo.libs.control.create(name="eyeSocket_{0}".format(side), 
                                          controlType="null",
                                          color=rigrepo.libs.common.YELLOW,
                                          hierarchy=['nul'],
                                          type='face')

        #parent the socket control to the anchor if it exist in the scene.
        if mc.objExists(anchor):
            mc.parent(eyeSocketNul, anchor)
        else:
            mc.warning("{} is not in the currnet Maya session!!!!".format(anchor))


        # create the upper and lower lid corner controls.
        upperLidNul, upperLidDefAuto, upperLidCtrl = rigrepo.libs.control.create(name="lidUpper_{0}".format(side), 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul', 'def_auto'],
                                              parent=eyeSocketCtrl,
                                              type='face')

        lowerLidNul, lowerLidDefAuto, lowerLidCtrl = rigrepo.libs.control.create(name="lidLower_{0}".format(side), 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul', 'def_auto'],
                                              parent=eyeSocketCtrl,
                                              type='face')

        # lock and hide scale attributes on the lid controls
        rigrepo.libs.attribute.lockAndHide([upperLidCtrl, lowerLidCtrl], ['s', 'sx', 'sy', 'sz', 't', 'tx', 'ty', 'tz', 'ry', 'rz'])

        # create drivers for the the lids.
        lowerLidDriver = mc.createNode("joint", name="lidLower_{0}_driver".format(side))
        lowerLidCollision = mc.createNode("joint", name="lidLower_{0}_collision_driver".format(side))
        mc.xform(lowerLidCollision, ws=True, matrix=mc.xform(lowerLidCtrl, q=True, ws=True, matrix=True))
        mc.parent(lowerLidDriver, lowerLidNul)
        mc.parent(lowerLidCollision, lowerLidNul)
        mc.pointConstraint(lowerLidCtrl, lowerLidCollision)
        mc.orientConstraint(lowerLidCtrl, lowerLidCollision)
        mc.pointConstraint(lowerLidCollision, lowerLidDriver)
        mc.orientConstraint(lowerLidCollision, lowerLidDriver, skip='x')
        mc.setAttr("{}.drawStyle".format(lowerLidDriver), 2)

        # create drivers for the the lids.
        upperLidDriver = mc.createNode("joint", name="lidUpper_{0}_driver".format(side))
        mc.parent(upperLidDriver, upperLidNul)
        mc.pointConstraint(upperLidCtrl, upperLidDriver)
        mc.orientConstraint(upperLidCtrl, upperLidDriver)
        mc.setAttr("{}.drawStyle".format(upperLidDriver), 2)

        # ----------------------------------------------------------
        # Blink collision setup
        # ----------------------------------------------------------
        sumPlusMinusAverage = mc.createNode('plusMinusAverage', name='{}_sum_pma'.format(self.name))
        mc.connectAttr('{}.rx'.format(upperLidCtrl), '{}.input1D[0]'.format(sumPlusMinusAverage), f=True)
        mc.connectAttr('{}.rx'.format(lowerLidCollision), '{}.input1D[1]'.format(sumPlusMinusAverage), f=True)

        diffPlusMinusAverage = mc.createNode('plusMinusAverage', name='{}_diff_pma'.format(self.name))
        mc.setAttr('{}.input1D[0]'.format(diffPlusMinusAverage), 40)
        mc.connectAttr('{}.output1D'.format(sumPlusMinusAverage), '{}.input1D[1]'.format(diffPlusMinusAverage), f=True)
        mc.setAttr('{}.operation'.format(diffPlusMinusAverage), 2)

        scaleMultDoubleLinear = mc.createNode('multDoubleLinear', name='{}_scale_mdl'.format(self.name))
        mc.connectAttr('{}.output1D'.format(diffPlusMinusAverage), '{}.input1'.format(scaleMultDoubleLinear), f=True)
        mc.setAttr('{}.input2'.format(scaleMultDoubleLinear), -.010)

        scalePlusMinusAverage = mc.createNode('plusMinusAverage', name='{}_scale_pma'.format(self.name))
        mc.connectAttr('{}.output'.format(scaleMultDoubleLinear), '{}.input1D[1]'.format(scalePlusMinusAverage), f=True)
        mc.setAttr('{}.input1D[0]'.format(scalePlusMinusAverage), 1)

        lowerLidSumPlusMinusAverage = mc.createNode('plusMinusAverage', name='{}_lower_sum_pma'.format(self.name))
        mc.connectAttr('{}.rx'.format(lowerLidCollision), '{}.input1D[0]'.format(lowerLidSumPlusMinusAverage), f=True)
        mc.connectAttr('{}.output1D'.format(diffPlusMinusAverage), '{}.input1D[1]'.format(lowerLidSumPlusMinusAverage), f=True)

        collisionCondition = mc.createNode('condition', name='{}_collision_cnd'.format(self.name))
        mc.setAttr('{}.operation'.format(collisionCondition), 4)
        mc.connectAttr('{}.output1D'.format(diffPlusMinusAverage), '{}.firstTerm'.format(collisionCondition), f=True)
        mc.connectAttr('{}.rx'.format(lowerLidCollision), '{}.colorIfFalseR'.format(collisionCondition), f=True)
        mc.connectAttr('{}.output1D'.format(lowerLidSumPlusMinusAverage), '{}.colorIfTrueR'.format(collisionCondition), f=True)

        scaleCondition = mc.createNode('condition', name='{}_scale_cnd'.format(self.name))
        mc.setAttr('{}.operation'.format(scaleCondition), 0)
        mc.connectAttr('{}.outColorR'.format(collisionCondition), '{}.firstTerm'.format(scaleCondition), f=True)
        mc.connectAttr('{}.output1D'.format(scalePlusMinusAverage), '{}.colorIfTrueR'.format(scaleCondition), f=True)
        mc.connectAttr('{}.output1D'.format(lowerLidSumPlusMinusAverage), '{}.secondTerm'.format(scaleCondition), f=True)

        mc.connectAttr('{}.outColorR'.format(collisionCondition), '{}.rx'.format(lowerLidDriver), f=True)

        # move the eyeSocket control to the position of the eyeCenter joint
        mc.xform(eyeSocketNul, ws=True, t=mc.xform(eyeCenter, q=True, ws=True, t=True))

        lidSqaushCluster = rigrepo.libs.cluster.create(geometry, 
                                        "lid_squash_{}_cluster".format(side),
                                        parent=self.name, 
                                        parallel=False)

        # move the lid sqaush cluster to match the eye center joint
        mc.xform("{}_nul".format(lidSqaushCluster), ws=True, matrix=mc.xform(eyeCenter, q=True, ws=True, matrix=True))

        mc.connectAttr('{}.outColorR'.format(scaleCondition), '{}_ctrl.sx'.format(lidSqaushCluster), f=True)
        mc.connectAttr('{}.outColorR'.format(scaleCondition), '{}_ctrl.sy'.format(lidSqaushCluster), f=True)
        mc.connectAttr('{}.outColorR'.format(scaleCondition), '{}_ctrl.sz'.format(lidSqaushCluster), f=True)

        # rotate the lower lid so it's inverted to match the rotation on x for the upper lid.
        mc.setAttr("{0}.rotateZ".format(lowerLidNul), 180)

        # connect the rotate X axis of the lid controls to the rotateAxis X
        # create a multDoubleLinear node
        for node in (lowerLidCtrl, upperLidCtrl):
            # set the handle positions by default
            mc.setAttr("{0}.selectHandleY".format(node), .2)
            mdl = mc.createNode("multDoubleLinear", n="{}_rot_mdl".format(node))
            mc.connectAttr("{}.rx".format(node), "{}.input1".format(mdl), f=True)
            mc.setAttr("{}.input2".format(mdl), -1)
            mc.connectAttr("{}.output".format(mdl), "{}.rotateAxisX".format(node), f=True)

        #point, orient constraint the socket joint to the socket control. Also connect scale
        mc.parentConstraint(eyeSocketCtrl, eyeCenter)
        mc.scaleConstraint(eyeSocketCtrl, eyeCenter)
        
        children = mc.listRelatives(eyeCenter, c=True, type="joint") or list()

        for jnt in children:
            mc.setAttr("{}.segmentScaleCompensate".format(jnt), 0)

        for section in ["Upper", "Lower"]:
            group = "lid{0}_{1}_{2}".format(section, side, rigrepo.libs.common.GROUP)
            # create the cluster at the and position it at the same position as eyeCenter
            lidCluster = rigrepo.libs.cluster.create(geometry, 
                                        "blink{0}_{1}_cluster".format(section, side),
                                        parent=self.name, 
                                        parallel=False)
            sectionCurve = self.getAttributeByName("{}Curve".format(section.lower())).getValue()

            # move the lid cluster to match the eye center joint
            mc.xform("{}_nul".format(lidCluster), ws=True, matrix=mc.xform(eyeCenter, q=True, ws=True, matrix=True))

            bindmeshGeometry, follicleList, jointList = self.__buildBlinkRig(sectionCurve, name="blink{0}_{1}".format(section, side), parent=self.name)
            # create the setDriven's for the cluster to follow the blink
            values = zip((0, 20, 40, -20),(0, 35, 65, -15))
            if section == "Lower":
                values = zip((0, 20, 40, -20),(0, -35, -65, 15))
            for driverValue, value in values:
                currentDriver = "lid{0}_{1}_driver.rotateX".format(section, side)
                mc.setDrivenKeyframe("{0}_def_auto.rotateX".format(lidCluster),
                                        currentDriver=currentDriver,
                                        dv=driverValue,
                                        itt="linear",
                                        ott= "linear", 
                                        value=value)

                # Set driven key post and pre infinity extrapolation
                dkey = mc.listConnections(currentDriver, scn=1, type='animCurveUA')[-1]
                mc.setAttr(dkey + '.preInfinity', 1)
                mc.setAttr(dkey + '.postInfinity', 1)
                mc.keyTangent(dkey, index=(0, 0), inTangentType='spline')
                mc.keyTangent(dkey, index=(0, 0), outTangentType='spline')
                mc.keyTangent(dkey, index=(3, 3), inTangentType='spline')
                mc.keyTangent(dkey, index=(3, 3), outTangentType='spline')

            # create the driver joint.
            mc.select("{}_ort".format(lidCluster))
            driverJnt = mc.joint(name="blink{}_{}_driver".format(section, side))
            mc.setAttr("{}.drawStyle".format(driverJnt), 2)
            mc.setAttr("{}.rotate".format(driverJnt), 0, 0, 0)
            mc.setAttr("{}.translate".format(driverJnt), 0, 0, 0)
            # constrain the driver to the ctrl of the cluster nodes
            mc.orientConstraint("{0}_ctrl".format(lidCluster), driverJnt)

            #deform the lid bindmesh with the lid curve using a wire deformer.
            wireDeformer = mc.wire(geometry, gw=False, en=1.00, ce=0.00, li=0.00, 
                    w=sectionCurve, name="{}_wire".format(sectionCurve))[0]

            # set the default values for the wire deformer
            mc.setAttr("{}.rotation".format(wireDeformer), 0)
            mc.setAttr("{}.dropoffDistance[0]".format(wireDeformer), 100)

            # create skinCluster for the base wire
            baseCurve = "{}BaseWire".format(sectionCurve)

            mc.cluster(bindmeshGeometry, name='{}__{}'.format(bindmeshGeometry,lidCluster), wn=["{0}_cls_hdl".format(lidCluster),"{0}_cls_hdl".format(lidCluster)], bs=1)
            rigrepo.libs.cluster.localize('{}__{}'.format(bindmeshGeometry,lidCluster), "{0}_auto".format(lidCluster), bindmeshGeometry)
            mc.cluster(baseCurve, name='{}__{}'.format(baseCurve,lidCluster), wn=["{0}_cls_hdl".format(lidCluster),"{0}_cls_hdl".format(lidCluster)], bs=1)
            rigrepo.libs.cluster.localize('{}__{}'.format(baseCurve,lidCluster), "{0}_auto".format(lidCluster), baseCurve) 


        # create the lid tweaker rig
        bindmeshGeometry, follicleList, controlHierarchyList, jointList = self.__buildCurveRig(lidCurve, "lid_{}".format(side), 'rig' )

        #deform the lid bindmesh with the lid curve using a wire deformer.
        wireDeformer = mc.wire(geometry, gw=False, en=1.00, ce=0.00, li=0.00, 
                w=lidCurve, name="{}_wire".format(lidCurve))[0]
        baseCurveJointList=list()
        for jnt, controlList in zip(jointList, controlHierarchyList):
            # create the joint that we will use later to deform the base wire.
            baseCurveJoint = mc.joint(name=jnt.replace("_jnt","_baseCurve_jnt"))
            baseCurveJointList.append(baseCurveJoint)
            # hide the base curve joint. Then parent it under the null node
            mc.setAttr("{}.v".format(baseCurveJoint), 0)
            mc.parent(baseCurveJoint, controlList[1])
            mc.setAttr("{}.t".format(baseCurveJoint), 0, 0, 0)

            if controlList[0].endswith('_r_nul'):
                mc.setAttr(controlList[0]+'.ry', -180)
                mc.setAttr(controlList[0]+'.sz', -1)

        # ------------------
        # ATTEMP TO RENAME
        # get the y positions and the eye center position
        eyeCenterPos = mc.xform(eyeCenter, q=True, ws=True, t=True)
        yvalueList = [mc.xform(controlList[0], q=True, ws=True, t=True)[1] for controlList in controlHierarchyList]
        yvalueListCopy = list(yvalueList)
        yvalueListCopy.sort()
        controlSplitSize = (len(controlHierarchyList) - 2) / 2

        # get the x positions for the controls highest
        xvalueList = [mc.xform(controlHierarchyList[yvalueList.index(value)][0], q=True, ws=True, t=True)[0] for value in yvalueListCopy[controlSplitSize+2:]]
        xvalueListCopy = list(xvalueList)
        xvalueListCopy.sort()
        index = 0
        if eyeCenterPos[0] <= 0:
            xvalueListCopy.reverse()
        for value in yvalueListCopy[controlSplitSize+2:]:
            controlHierarchy = controlHierarchyList[yvalueList.index(value)]
            newControlName = 'lid_up_{}_{}'.format(xvalueListCopy.index(xvalueList[index])+1, side)
            oldControlName = controlHierarchy[-1]
            for node in controlHierarchy:
                controlHierarchy[controlHierarchy.index(node)] = mc.rename(node, node.replace(oldControlName, newControlName))
            index += 1

        # get the x positions for the controls lowest
        xvalueList = [mc.xform(controlHierarchyList[yvalueList.index(value)][0], q=True, ws=True, t=True)[0] for value in yvalueListCopy[:controlSplitSize+2]]
        xvalueListCopy = list(xvalueList)
        xvalueListCopy.sort()
        if eyeCenterPos[0] <= 0:
            xvalueListCopy.reverse()
        index = 0
        for value in yvalueListCopy[:controlSplitSize+2]:
            controlHierarchy = controlHierarchyList[yvalueList.index(value)]
            newControlName = 'lid_low_{}_{}'.format(xvalueListCopy.index(xvalueList[index])+1, side)
            oldControlName = controlHierarchy[-1]
            for node in controlHierarchy:
                controlHierarchy[controlHierarchy.index(node)] = mc.rename(node, node.replace(oldControlName, newControlName))
            index += 1

        # name the corner controls.
        for value in yvalueListCopy[controlSplitSize:-controlSplitSize]:
            controlHierarchy = controlHierarchyList[yvalueList.index(value)]
            oldControlName = controlHierarchy[-1]
            controlPos = mc.xform(oldControlName, q=True, ws=True, t=True)
            if eyeCenterPos[0] >= 0:
                if controlPos[0] > eyeCenterPos[0]:
                    newControlName = 'lid_corner_outer_{}'.format(side)
                else:
                    newControlName = 'lid_corner_inner_{}'.format(side)
            elif eyeCenterPos[0] < 0: 
                if controlPos[0] < eyeCenterPos[0]:
                    newControlName = 'lid_corner_outer_{}'.format(side)
                else:
                    newControlName = 'lid_corner_inner_{}'.format(side)

            for node in controlHierarchy:
                controlHierarchy[controlHierarchy.index(node)] = mc.rename(node, node.replace(oldControlName, newControlName))
                

        baseCurve = "{}BaseWire".format(lidCurve)
        mc.parent(baseCurve, "lid_{}".format(side))
        baseCurveSkin = mc.skinCluster(*baseCurveJointList+mc.ls(baseCurve), 
                                    n="{}_skinCluster".format(baseCurve),
                                    tsb=True)[0]

        # set the weights to have proper weighting
        wtObj = rigrepo.libs.weights.getWeights(baseCurveSkin)
        weightList = list()
        for i, inf in enumerate(wtObj):
            array = numpy.zeros_like(wtObj.getWeights(inf))[0]
            array[i] = 1
            weightList.append(array)
        wtObj.setWeights(weightList)
        rigrepo.libs.weights.setWeights(baseCurveSkin, wtObj)

        # set the default values for the wire deformer
        mc.setAttr("{}.rotation".format(wireDeformer), 0)
        mc.setAttr("{}.dropoffDistance[0]".format(wireDeformer), 100)
        mc.parent(lidCurve, "lid_{}".format(side))

        # parent groups under the name of the part
        mc.parent([self.controlGroup], self.name)

        # create the socket lift cluster
        socketLiftCluster = rigrepo.libs.cluster.create(geometry, 
                                        "socketLift_{0}_cluster".format(side),
                                        parent=anchor, 
                                        parallel=False)

        # create the socket lift cluster
        socketStretchCluster = rigrepo.libs.cluster.create(mc.ls([geometry,eyeGeometry]), 
                                        "socketStretch_{0}_cluster".format(side),
                                        parent=anchor, 
                                        parallel=False)

        # move the cluster into the correct location
        mc.xform("{}_nul".format(socketLiftCluster), ws=True, matrix=mc.xform(upperLidCtrl, q=True, ws=True, matrix=True))
        mc.xform("{}_nul".format(socketStretchCluster), ws=True, matrix=mc.xform(upperLidCtrl, q=True, ws=True, matrix=True))

        #turn off visibility of the handle and create the socket lift attribute on the upperLid
        mc.setAttr("{}_ctrl.displayHandle".format(socketLiftCluster), 0)
        mc.setAttr("{}_ctrl.displayHandle".format(socketStretchCluster), 0)
        mc.addAttr(upperLidCtrl, ln="socketLift", at="double", min=-10, max=10, dv=0, keyable=True)

        socketClusterList = rigrepo.libs.cluster.transferCluster(geometry, bindmeshGeometry, socketStretchCluster, handle=True)
        #socketClusterList.extend(rigrepo.libs.cluster.transferCluster(geometry, baseCurve, socketLiftCluster, handle=True))

        # this will localize the blink agains the model group and auto node
        for cluster in socketClusterList:
            clusterName = cluster.split("__")[-1]
            rigrepo.libs.cluster.localize(cluster, "{}_auto".format(clusterName), "model")

        # loop through and create the setDriven keyframe for the socketLift
        for driverValue, value in zip((0, 10, -10), (1, 10, -10)):
            mc.setDrivenKeyframe("{0}_def_auto.scaleY".format(socketLiftCluster),
                                        currentDriver="{}.socketLift".format(upperLidCtrl), 
                                        dv=driverValue,
                                        itt="linear",
                                        ott= "linear", 
                                        value=value)

        # handle the automation of the scaling through the rotation of the upperLid driver
        for driverValue, value in zip((0, -20), (1, 10)):
            mc.setDrivenKeyframe("{0}_def_auto.scaleY".format(socketStretchCluster),
                                            currentDriver="{}.rotateX".format(upperLidCtrl), 
                                            dv=driverValue,
                                            itt="linear",
                                            ott= "linear", 
                                            value=value)

        # connect the scale of the uppper lid control to the socket stretch cluster
        mc.connectAttr("{}.scaleY".format(upperLidCtrl), "{}_ctrl.scaleY".format(socketStretchCluster), f=True)
        # connect the position and rotation of socketStretchCluster to socketLiftCluster
        mc.connectAttr("{}_ort.rotate".format(socketStretchCluster), "{}_ort.rotate".format(socketLiftCluster), f=True)
        mc.connectAttr("{}_ort.translate".format(socketStretchCluster), "{}_ort.translate".format(socketLiftCluster), f=True)

    def postBuild(self):
        '''
        '''
        for node in [self.controlGroup]:
            if mc.getAttr("{}.v".format(node)):
                rigrepo.libs.attribute.lockAndHide(node,['t','r','s'])


        # parent the curve groups to the rig group
        lowerNeutralCurve = self.getAttributeByName('lowerCurve').getValue()
        upperNeutralCurve = self.getAttributeByName('upperCurve').getValue()

        for node in (lowerNeutralCurve,upperNeutralCurve):
            parent = mc.listRelatives(node, p=True)[0]
            if mc.getAttr("{}.v".format(parent)):
                mc.setAttr("{}.v".format(parent), 0)

        # localize skinClusters
        rigrepo.libs.skinCluster.localize(self._skinClusters, self.name)


    def __buildBlinkRig(self, curve, name='blink', parent=None):
        '''
        This will build a rig setup based on the curve that is passed in.

        :param curve: NurbsCurve name you want to build the rig on.
        :type curve: str

        :param name: This will be used to name the control hierachy and joints in the rig.
        :type name: str

        :return: This method will return the data needed to make adjustments to rig.
        :rtype: tuple
        '''
        # Do some check
        if not mc.objExists(curve):
            raise RuntimeError("{} doesn't exist in the current Maya session.".format(curve))
        # If the name passed in doesn't exist, we will create a transform as the parent group
        # for the rig.
        grp="{}_grp".format(name)
        if not mc.objExists(grp):
            mc.createNode("transform", n=grp)
        # create the bindmesh 
        #
        # follicleList = (follicle transform, follicle shape) 
        # bindmeshGeometry = geometry name of bindmesh
        #
        bindmeshGeometry, follicleList = bindmesh.createFromCurve(name, curve)
        # emptry list to append controls to in the loop
        controlHierarchyList = list()
        jointList = list()

        # loop through and create controls on the follicles so we have controls to deform the wire.
        for follicle in follicleList:
            # get the follicle transform so we can use it to parent the control to it.
            follicleIndex = follicleList.index(follicle)
            mc.select(follicle, r=True)

            # create the joint that will drive the curve.
            jnt = mc.joint(n="{}_{}_jnt".format(name, follicleIndex))
            mc.setAttr("{}.translate".format(jnt), 0,0,0)
            mc.setAttr("{}.rotate".format(jnt), 0,0,0)
            mc.setAttr("{}.drawStyle".format(jnt),2)
            jointList.append(jnt)

        # This will parent all of the data for the rig to the system group "name"
        for data in (bindmeshGeometry, follicleList):
            mc.parent(data, grp)

        # If parent the parent is passed in we will parent the system to the parent.
        if parent:
            if not mc.objExists(parent):
                mc.warning('Created the system but the current parent "{}" does not exist in the \
                    current Maya session.'.format(parent))
            else:
                mc.parent(grp, parent)

        # create the skinCluster for the lipMainCurve
        mc.skinCluster(*jointList + [curve], tsb=True, name="{}_skinCluster".format(curve))

        # set the visibility of the bindmesh.
        mc.setAttr("{}.v".format(bindmeshGeometry), 0 )
        mc.setAttr("{}.v".format(curve), 0 )
        return bindmeshGeometry, follicleList, jointList

    def __buildCurveRig(self, curve, name='lid', parent=None):
        '''
        This will build a rig setup based on the curve that is passed in.

        :param curve: NurbsCurve name you want to build the rig on.
        :type curve: str

        :param name: This will be used to name the control hierachy and joints in the rig.
        :type name: str

        :return: This method will return the data needed to make adjustments to rig.
        :rtype: tuple
        '''
        # Do some check
        if not mc.objExists(curve):
            raise RuntimeError("{} doesn't exist in the current Maya session.".format(curve))
        # If the name passed in doesn't exist, we will create a transform as the parent group
        # for the rig.
        if not mc.objExists(name):
            mc.createNode("transform", n=name)
        # create the bindmesh 
        #
        # follicleList = (follicle transform, follicle shape) 
        # bindmeshGeometry = geometry name of bindmesh
        #
        bindmeshGeometry, follicleList = bindmesh.createFromCurve(name, curve)
        # emptry list to append controls to in the loop
        controlHierarchyList = list()
        jointList = list()

        # loop through and create controls on the follicles so we have controls to deform the wire.
        for follicle in follicleList:
            # get the follicle transform so we can use it to parent the control to it.
            follicleIndex = follicleList.index(follicle)
            # create the control with a large enough hierarchy to create proper SDK's
            ctrlHierarchy = rigrepo.libs.control.create(name="{}_{}".format(name, follicleIndex), 
                controlType="square", 
                hierarchy=['nul','ort','rot_def_auto','def_auto'], 
                parent=follicle,
                type='face')

            # create the joint that will drive the curve.
            jnt = mc.joint(n="{}_{}_jnt".format(name, follicleIndex))
            # make sure the joint is in the correct space
            mc.setAttr("{}.translate".format(jnt), 0,0,0)
            mc.setAttr("{}.rotate".format(jnt), 0,0,0)
            mc.setAttr("{}.drawStyle".format(jnt),2)
            mc.setAttr("{}.displayHandle".format(ctrlHierarchy[-1]), 1)
            mc.delete(mc.listRelatives(ctrlHierarchy[-1], c=True, shapes=True)[0])

            # zero out the nul for the control hierarchy so it's in the correct position.
            mc.setAttr("{}.translate".format(ctrlHierarchy[0]), 0,0,0)
            #mc.setAttr("{}.rotate".format(ctrlHierarchy[0]), 0,0,0)
            # set the visibility of the shape node for the follicle to be off.
            # append the control and the follicle transform to their lists
            controlHierarchyList.append(ctrlHierarchy)
            jointList.append(jnt)

        # This will parent all of the data for the rig to the system group "name"
        for data in (bindmeshGeometry, follicleList):
            mc.parent(data, name)

        # If parent the parent is passed in we will parent the system to the parent.
        if parent:
            if not mc.objExists(parent):
                mc.warning('Created the system but the current parent "{}" does not exist in the \
                    current Maya session.'.format(parent))
            else:
                mc.parent(name, parent)

        # create the skinCluster for the lipMainCurve
        mc.skinCluster(*jointList + [curve], tsb=True, name="{}_skinCluster".format(curve))

        # set the visibility of the bindmesh.
        mc.setAttr("{}.v".format(bindmeshGeometry), 0 )
        mc.setAttr("{}.v".format(curve), 0 )
        return bindmeshGeometry, follicleList, controlHierarchyList, jointList