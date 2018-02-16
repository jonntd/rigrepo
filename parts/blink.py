'''
This is not broken up into pieces yet. Just putting it here to hace access and work on it.
PLEASE DON'T MESS WITH THIS FILE!
'''
import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.libs.curve 
import rigrepo.libs.control 
import rigrepo.libs.transform
import rigrepo.libs.common
import rigrepo.libs.attribute
import rigrepo.libs.skinCluster
import rigrepo.parts.part as part

class Blink(part.Part):
    def __init__(self, name, side="l", anchor="head"):
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
        upperLidNul, upperLidCtrl = rigrepo.libs.control.create(name="lidUpper_{0}".format(side), 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul'],
                                              parent=eyeSocketCtrl)

        lowerLidNul, lowerLidCtrl = rigrepo.libs.control.create(name="lidLower_{0}".format(side), 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul'],
                                              parent=eyeSocketCtrl)

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
                                    currentDriver="lid{0}_{1}.rotateX".format(section, side), 
                                    dv=rotValue, 
                                    itt="linear",
                                    ott= "linear", 
                                    value=blendValue)
                rotValue+=40.0/len(closeCurves)
                blendValue+=1.0/len(closeCurves)
                if crv != closeCurves[-1]:
                    mc.blendShape(blendShape, e=True, ib=True, t=[neutralCurve, 0, crv, blendValue])
                mc.setDrivenKeyframe("{0}.{1}".format(blendShape, closeCurves[-1]),
                                    currentDriver="lid{0}_{1}.rotateX".format(section, side), 
                                    dv=rotValue, 
                                    itt="linear",
                                    ott= "linear", 
                                    value=blendValue)

            # open curve blend and set driven's
            rotValue = 0.0
            blendValue = 0.0
            for crv in openCurves:
                mc.setDrivenKeyframe("{0}.{1}".format(blendShape, openCurves[-1]),
                            currentDriver="lid{0}_{1}.rotateX".format(section, side), 
                            dv=rotValue, 
                            itt="linear", 
                            ott= "linear", 
                            value=blendValue)
                rotValue+=-40.0/len(openCurves)
                blendValue+=1.0/len(openCurves)
                if crv != openCurves[-1]:
                    mc.blendShape(blendShape, e=True, ib=True, t=[neutralCurve, 1, crv, blendValue])
                mc.setDrivenKeyframe("{0}.{1}".format(blendShape, openCurves[-1]), 
                            currentDriver="lid{0}_{1}.rotateX".format(section, side), 
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
                mc.setAttr("{0}.v".format(jntDriver))
                driverJntList.append(jntDriver)

                lidControlList.append(ctrlHierarchy[-1])
                # parent the locators and the controls to their respective groups
                mc.parent(loc, self.locatorGroup)
                mc.parent(ctrlHierarchy[0], self.controlGroup)

                # setup a scale constraint on the base joints for the socket scale
                #mc.scaleConstraint(eyeCenter, jntBase, mo=True)
                mc.disconnectAttr('{}.scale'.format(eyeCenter), "{}.inverseScale".format(jntBase))

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
            print crv
            skinCluster = mc.skinCluster([eyeCenter] + lidCornerJointList, crv, tsb=True, n=crv+'_skinCluster')[0]
            self._skinClusters.append(skinCluster)
            print skinCluster, lidCornerJointList
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
