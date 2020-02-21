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
        self.addAttribute("neutralLowerCurve", "lidLower_neutral_{}_curve".format(side), attrType=str)
        self.addAttribute("neutralUpperCurve", "lidUpper_neutral_{}_curve".format(side), attrType=str)
        self.addAttribute("blinkLowerCurve", "lidLower_blink_{}_curve".format(side), attrType=str)
        self.addAttribute("blinkUpperCurve", "lidUpper_blink_{}_curve".format(side), attrType=str)
        self.addAttribute("closeLowerCurves", 
                            ['lidLower_middle_{}_curve'.format(side),'lidLower_closed_{}_curve'.format(side)], 
                            attrType=list)
        self.addAttribute("closeUpperCurves", 
                            ['lidUpper_middle_{}_curve'.format(side),'lidUpper_closed_{}_curve'.format(side)], 
                            attrType=list)
        self.addAttribute("openLowerCurves", ['lidLower_open_{}_curve'.format(side)], attrType=list)
        self.addAttribute("openUpperCurves", ['lidUpper_open_{}_curve'.format(side)], attrType=list)
        self.locatorGroup = "{}_locators".format(self.name)
        self.controlGroup = "{}_controls".format(self.name)
        self._skinClusters = list()

    def setup(self):
        '''
        This will create default nodes that should exists in the scene for the part to build.
        '''
        super(Blink, self).setup()

        for node in [self.locatorGroup, self.controlGroup]:
            if not mc.objExists(node):
                mc.createNode("transform", name=node)

        # parent the curve groups to the rig group
        lowerNeutralCurve = self.getAttributeByName('neutralLowerCurve').getValue()
        upperNeutralCurve = self.getAttributeByName('neutralUpperCurve').getValue()

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

        # CREATE THE CONTROLS FOR THE BLINK RIG.
        # Create the eyeSocket control
        eyeSocketNul, eyeSocketCtrl = rigrepo.libs.control.create(name="eyeSocket_{0}".format(side), 
                                          controlType="null",
                                          color=rigrepo.libs.common.YELLOW,
                                          hierarchy=['nul'])

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
                                              parent=eyeSocketCtrl)

        lowerLidNul, lowerLidDefAuto, lowerLidCtrl = rigrepo.libs.control.create(name="lidLower_{0}".format(side), 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul', 'def_auto'],
                                              parent=eyeSocketCtrl)

        # lock and hide scale attributes on the lid controls
        rigrepo.libs.attribute.lockAndHide([upperLidCtrl, lowerLidCtrl], ['s', 'sx', 'sy', 'sz', 't', 'tx', 'ty', 'tz'])

        # move the eyeSocket control to the position of the eyeCenter joint
        mc.xform(eyeSocketNul, ws=True, t=mc.xform(eyeCenter, q=True, ws=True, t=True))

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
        mc.pointConstraint(eyeSocketCtrl, eyeCenter)
        mc.orientConstraint(eyeSocketCtrl, eyeCenter)
        mc.scaleConstraint(eyeSocketCtrl, eyeCenter)
        children = mc.listRelatives(eyeCenter, c=True, type="joint") or list()

        for jnt in children:
            mc.setAttr("{}.segmentScaleCompensate".format(jnt), 0)
        #mc.connectAttr("{}.scale".format(eyeSocketCtrl), "{}.scale".format(eyeCenter), f=True)

        lidControlList = list()
        for section in ["Upper", "Lower"]:
            group = "lid{0}_{1}_{2}".format(section, side, rigrepo.libs.common.GROUP)
            neutralCurve = self.getAttributeByName("neutral{0}Curve".format(section)).getValue()
            blinkCurve = self.getAttributeByName("blink{0}Curve".format(section)).getValue()
            bindJointParent = eyeCenter
            closeCurves = self.getAttributeByName("close{0}Curves".format(section)).getValue()
            openCurves = self.getAttributeByName("open{0}Curves".format(section)).getValue()

            # setup the blendShape for the blink and then we will add the in-betweens later.
            blendShape = mc.blendShape([closeCurves[-1],openCurves[-1]],neutralCurve,w=[0,0])[0]
            mc.blendShape(neutralCurve, blinkCurve,w=[0,1])[0]

            #closed curves and set drivens
            rotValue = 0.0
            blendValue = 0.0
            for crv in closeCurves:
                mc.setDrivenKeyframe("{0}.{1}".format(blendShape, closeCurves[-1]),
                                    currentDriver="lid{0}_{1}_driver.rotateX".format(section, side), 
                                    dv=rotValue, 
                                    itt="linear",
                                    ott= "linear", 
                                    value=blendValue)
                rotValue+=40.0/len(closeCurves)
                blendValue+=1.0/len(closeCurves)
                if crv != closeCurves[-1]:
                    mc.blendShape(blendShape, e=True, ib=True, t=[neutralCurve, 0, crv, blendValue])
                mc.setDrivenKeyframe("{0}.{1}".format(blendShape, closeCurves[-1]),
                                    currentDriver="lid{0}_{1}_driver.rotateX".format(section, side), 
                                    dv=rotValue, 
                                    itt="linear",
                                    ott= "linear", 
                                    value=blendValue)

            # open curve blend and set driven's
            rotValue = 0.0
            blendValue = 0.0
            for crv in openCurves:
                mc.setDrivenKeyframe("{0}.{1}".format(blendShape, openCurves[-1]),
                            currentDriver="lid{0}_{1}_driver.rotateX".format(section, side), 
                            dv=rotValue, 
                            itt="linear", 
                            ott= "linear", 
                            value=blendValue)
                rotValue+=-40.0/len(openCurves)
                blendValue+=1.0/len(openCurves)
                if crv != openCurves[-1]:
                    mc.blendShape(blendShape, e=True, ib=True, t=[neutralCurve, 1, crv, blendValue])
                mc.setDrivenKeyframe("{0}.{1}".format(blendShape, openCurves[-1]), 
                            currentDriver="lid{0}_{1}_driver.rotateX".format(section, side), 
                            dv=rotValue, 
                            itt="linear", 
                            ott= "linear", 
                            value=blendValue)


            # variable to store all of the lid joints which will be used
            # when binding to the mesh.
            bindJointList = list()
            # loop through the vrts on the lid and create the joint setup
            # CURRENTLY WERE USING SELECTION.
            #====================================
            # get the position of the eyeCenter
            eyeCenterPosition = mc.xform(eyeCenter, q=True, ws=True, t=True)
            selList = om.MSelectionList()
            selList.add(neutralCurve)
            curveDagPath = selList.getDagPath(0)
            curveDagPath.extendToShape()
            curveFn = om.MFnNurbsCurve(curveDagPath)
            driverJntList = list()
            for i,vrt in enumerate(mc.ls("{0}.cv[*]".format(neutralCurve), fl=True)):
                #clear the selection first.
                mc.select(cl=True) 
                jntBase = mc.joint(name="{0}_{1}_base".format(neutralCurve, str(i).zfill(3)), 
                                    position=eyeCenterPosition)

                #clear the selection before we create the bind joint.
                mc.select(cl=True) 
                #get the vertex position in world space.
                vrtPosition = mc.xform(vrt,q=True,ws=True,t=True)
                jntBind = mc.joint(name="{0}_{1}_bind".format(neutralCurve, str(i).zfill(3)), 
                                    position=vrtPosition)
                # parent the bind joint to the base joint.
                mc.parent(jntBind,jntBase)
                #orient the joint
                mc.joint(jntBase,e=True, oj="xyz", secondaryAxisOrient= "yup")
                # set the bind joint to match the orientation of the base joint.
                mc.setAttr("{0}.jo".format(jntBind),0,0,0)
                mc.setAttr("{0}.radius".format(jntBind),.08)
                mc.setAttr("{0}.radius".format(jntBase),.08)
                
                #point on curve info node
                closestPoint = curveFn.closestPoint(om.MPoint(*vrtPosition))[0]
                param = rigrepo.libs.curve.getParamFromPosition(neutralCurve,
                            [closestPoint.x,closestPoint.y,closestPoint.z])
                poci = mc.createNode("pointOnCurveInfo", name="{0}_poci".format(jntBind))
                mc.setAttr("{0}.parameter".format(poci), param)
                mc.connectAttr("{0}.local".format(curveDagPath.fullPathName()),
                                "{0}.inputCurve".format(poci),
                                f=True)
                ctrlHierarchy = rigrepo.libs.control.create(name=jntBind.replace("_bind",""), 
                                                            controlType = "null", 
                                                            hierarchy=['nul','ort'],
                                                            parent=None)
                jntDriver = mc.joint(name="{0}_{1}_driver".format(neutralCurve, str(i).zfill(3)))
                mc.setAttr("{0}.radius".format(jntDriver),.08)
                mc.setAttr("{0}.v".format(jntDriver), 0)
                mc.connectAttr("{0}.position".format(poci), "{0}.t".format(ctrlHierarchy[0]),f=True)
                mc.xform(ctrlHierarchy[1],ws=True,t=vrtPosition)

                loc = mc.spaceLocator(name="{0}_{1}_loc".format(neutralCurve, str(i).zfill(3)))[0]
                mc.setAttr("{0}Shape.localScale".format(loc),.2,.2,.2)
                poci = mc.createNode("pointOnCurveInfo", name="{0}_loc_poci".format(jntBind))
                mc.setAttr("{0}.parameter".format(poci), param)
                mc.connectAttr("{0}Shape.local".format(blinkCurve), "{0}.inputCurve".format(poci),f=True)
                mc.connectAttr("{0}.position".format(poci), "{0}.t".format(loc),f=True)
                mc.parent(jntBase, eyeCenter)
                mc.aimConstraint(loc,jntBase,aimVector=(1,0,0),upVector=(0,1,0),wut="none")
                driverJntList.append(jntDriver)

                lidControlList.append(ctrlHierarchy[-1])
                # parent the locators and the controls to their respective groups
                mc.parent(loc, self.locatorGroup)
                mc.parent(ctrlHierarchy[0], self.controlGroup)

                # setup a scale constraint on the base joints for the socket scale
                #mc.scaleConstraint(eyeCenter, jntBase, mo=True)
                #mc.disconnectAttr('{}.scale'.format(eyeCenter), "{}.inverseScale".format(jntBase))
                mc.setAttr("{}.segmentScaleCompensate".format(jntBase))

            mc.select(driverJntList + [blinkCurve],r=True)

            # do the bind pre-matrix for the skinCluster on the blink curve.
            skinCluster = mc.skinCluster(n=blinkCurve+'_skinCluster')[0]
            self._skinClusters.append(skinCluster)
            for i,jnt in enumerate(driverJntList):
                parentOfJnt = mc.listRelatives(jnt,p=True)[0]
                mc.connectAttr('{0}.parentInverseMatrix[0]'.format(parentOfJnt),
                                '{0}.bindPreMatrix[{1}]'.format(skinCluster,i), f=True)


        upperControlList = lidControlList[:len(lidControlList)/2]
        lowerControlList = lidControlList[len(lidControlList)/2:]

        lidInnerNul, lidInnerCtrl = rigrepo.libs.control.create(name="lidInnerCorner_{0}".format(side), 
                                          controlType="diamond",
                                          color=rigrepo.libs.common.BLUE,
                                          hierarchy=['nul'],
                                          parent=eyeSocketCtrl)

        lidOuterNul, lidOuterCtrl = rigrepo.libs.control.create(name="lidOuterCorner_{0}".format(side), 
                                          controlType="diamond",
                                          color=rigrepo.libs.common.BLUE,
                                          hierarchy=['nul'],
                                          parent=eyeSocketCtrl)

        # create joints that can be used to skin the neutral curve and help drive the corners
        lidCornerJointList = list()
        for ctrl in (lidInnerCtrl, lidOuterCtrl):
            mc.select(ctrl, r=True)
            jnt = mc.joint(name="{0}_driver".format(ctrl))
            mc.setAttr("{0}.v".format(jnt), 0)
            lidCornerJointList.append(jnt)

        # Now move the controls into the average position of both upper and lower lid controls.
        mc.xform(lidInnerNul, ws=True, 
                t=rigrepo.libs.transform.getAveragePosition((upperControlList[0], lowerControlList[0])))

        mc.xform(lidOuterNul, ws=True, 
                t=rigrepo.libs.transform.getAveragePosition((upperControlList[-1], lowerControlList[-1])))

        # get the neutral curves. 
        # I AM PRETTY SURE THERE IS A MORE OPTIMAL WAY FOR ME TO CODE THIS.
        neutralLowerCurve = self.getAttributeByName("neutralLowerCurve").getValue()
        neutralUpperCurve = self.getAttributeByName("neutralUpperCurve").getValue()

        # put the eyeSocket as a skinCluster onto the neutral curve so it follows the rig.
        for crv in (neutralUpperCurve, neutralLowerCurve):
            cvList = rigrepo.libs.curve.getCVs(crv)
            skinCluster = mc.skinCluster([eyeCenter] + lidCornerJointList, crv, tsb=True, n=crv+'_skinCluster')[0]
            self._skinClusters.append(skinCluster)
            mc.skinPercent(skinCluster, cvList[0], tv=[(lidCornerJointList[0],1.0)]);
            mc.skinPercent(skinCluster, cvList[-1], tv=[(lidCornerJointList[1],1.0)]);
            for cv in cvList[1:-1]:
                mc.skinPercent(skinCluster, cv, tv=[(eyeCenter,1.0)]);

        # parent groups under the name of the part
        mc.parent([self.controlGroup, self.locatorGroup], self.name)

    def postBuild(self):
        '''
        '''
        for node in [self.locatorGroup, self.controlGroup]:
            if mc.getAttr("{}.v".format(node)):
                rigrepo.libs.attribute.lockAndHide(node,['t','r','s'])
        
        #hide the locator group
        mc.setAttr("{}.v".format(self.locatorGroup), 0)


        # parent the curve groups to the rig group
        lowerNeutralCurve = self.getAttributeByName('neutralLowerCurve').getValue()
        upperNeutralCurve = self.getAttributeByName('neutralUpperCurve').getValue()

        for node in (lowerNeutralCurve,upperNeutralCurve):
            parent = mc.listRelatives(node, p=True)[0]
            if mc.getAttr("{}.v".format(parent)):
                mc.setAttr("{}.v".format(parent), 0)

        # localize skinClusters
        rigrepo.libs.skinCluster.localize(self._skinClusters, self.name)

class BlinkNew(part.Part):
    def __init__(self, name, side="l", anchor="face_upper", dataObj=None):
        '''
        '''
        # Create the attributes that the user will be able to change on the part
        # that will affect the build.
        super(BlinkNew, self).__init__(name)
        self.addAttribute("side", side, attrType=str)
        self.addAttribute("anchor", anchor, attrType=str)
        self.addAttribute("eyeCenterJoint", "eyeSocket_{}_bind".format(side), attrType=str)
        self.addAttribute("lowerCurve", "blinkLower_{}_curve".format(side), attrType=str)
        self.addAttribute("upperCurve", "blinkUpper_{}_curve".format(side), attrType=str)
        self.addAttribute("lidCurve", "lid_{}_curve".format(side), attrType=str)
        self.addAttribute("geometry", "body_geo", attrType=str)

        self.controlGroup = "{}_controls".format(self.name)
        self._skinClusters = list()

    def setup(self):
        '''
        This will create default nodes that should exists in the scene for the part to build.
        '''
        super(BlinkNew, self).setup()

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
        super(BlinkNew, self).build()
        eyeCenter = self.getAttributeByName("eyeCenterJoint").getValue()
        side = self.getAttributeByName("side").getValue()
        anchor = self.getAttributeByName("anchor").getValue()
        geometry = self.getAttributeByName("geometry").getValue()
        upperCurve = self.getAttributeByName("upperCurve").getValue()
        lowerCurve = self.getAttributeByName("lowerCurve").getValue()
        lidCurve = self.getAttributeByName("lidCurve").getValue()

        # CREATE THE CONTROLS FOR THE BLINK RIG.
        # Create the eyeSocket control
        eyeSocketNul, eyeSocketCtrl = rigrepo.libs.control.create(name="eyeSocket_{0}".format(side), 
                                          controlType="null",
                                          color=rigrepo.libs.common.YELLOW,
                                          hierarchy=['nul'])

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
                                              parent=eyeSocketCtrl)

        lowerLidNul, lowerLidDefAuto, lowerLidCtrl = rigrepo.libs.control.create(name="lidLower_{0}".format(side), 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul', 'def_auto'],
                                              parent=eyeSocketCtrl)

        # lock and hide scale attributes on the lid controls
        rigrepo.libs.attribute.lockAndHide([upperLidCtrl, lowerLidCtrl], ['s', 'sx', 'sy', 'sz', 't', 'tx', 'ty', 'tz'])

        # create drivers for the the lids.
        lowerLidDriver = mc.createNode("joint", name="lidLower_{0}_driver".format(side))
        mc.parent(lowerLidDriver, lowerLidNul)
        mc.pointConstraint(lowerLidCtrl, lowerLidDriver)
        mc.orientConstraint(lowerLidCtrl, lowerLidDriver)
        mc.setAttr("{}.drawStyle".format(lowerLidDriver), 2)

        # create drivers for the the lids.
        upperLidDriver = mc.createNode("joint", name="lidUpper_{0}_driver".format(side))
        mc.parent(upperLidDriver, upperLidNul)
        mc.pointConstraint(upperLidCtrl, upperLidDriver)
        mc.orientConstraint(upperLidCtrl, upperLidDriver)
        mc.setAttr("{}.drawStyle".format(upperLidDriver), 2)


        # move the eyeSocket control to the position of the eyeCenter joint
        mc.xform(eyeSocketNul, ws=True, t=mc.xform(eyeCenter, q=True, ws=True, t=True))

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
        socketStretchCluster = rigrepo.libs.cluster.create(geometry, 
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
            mc.setDrivenKeyframe("{0}_ctrl.scaleY".format(socketLiftCluster),
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
                parent=follicle)

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