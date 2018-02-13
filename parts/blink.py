'''
This is not broken up into pieces yet. Just putting it here to hace access and work on it.
PLEASE DON'T MESS WITH THIS FILE!
'''
import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.libs.curve 
import rigrepo.libs.control 
import rigrepo.libs.transform
import rigrepo.parts.part as part

class Blink(part.Part):
    def __init__(self, name):
        '''
        '''
        # Create the attributes that the user will be able to change on the part
        # that will affect the build.
        super(Blink, self).__init__(name)
        self.addAttribute("eyeCenter", "lidLower_L", attrType=str)
        self.addAttribute("neutralCurve", "lidLower_l_neutral", attrType=str)
        self.addAttribute("blinkCurve", "lidLower_l_blink", attrType=str)
        self.addAttribute("bindJointParent", "eyeSocket_l_bind", attrType=str)
        self.addAttribute("closeCurves", ['lidLower_l_middle','lidLower_l_closed'], attrType=list)
        self.addAttribute("openCurves", ['lidLower_l_open'], attrType=list)

    def build(self):
        '''
        This will run the build of the eye rig.
        '''
        super(Blink, self).build()
        eyeCenter = self.getAttributeByName("eyeCenter").getValue()
        neutralCurve = self.getAttributeByName("neutralCurve").getValue()
        blinkCurve = self.getAttributeByName("blinkCurve").getValue()
        bindJointParent = self.getAttributeByName("bindJointParent").getValue()
        closeCurves = self.getAttributeByName('closeCurves').getValue()
        openCurves = self.getAttributeByName('openCurves').getValue()

        # setup the blendShape for the blink and then we will add the in-betweens later.
        blendShape = mc.blendShape([closeCurves[-1],openCurves[-1]],neutralCurve,w=[0,0])[0]
        mc.blendShape(neutralCurve, blinkCurve,w=[0,1])[0]

        #closed curves and set drivens
        rotValue = 0.0
        blendValue = 0.0
        for crv in closeCurves:
            mc.setDrivenKeyframe("{0}.{1}".format(blendShape, closeCurves[-1]),
                                currentDriver="{0}.rotateX".format(eyeCenter), dv=rotValue, itt="linear",
                                ott= "linear", value=blendValue)
            rotValue+=40.0/len(closeCurves)
            blendValue+=1.0/len(closeCurves)
            if crv != closeCurves[-1]:
                mc.blendShape(blendShape, e=True, ib=True, t=[neutralCurve, 0, crv, blendValue])
            mc.setDrivenKeyframe("{0}.{1}".format(blendShape, closeCurves[-1]),
                                currentDriver="{0}.rotateX".format(eyeCenter), dv=rotValue, itt="linear",
                                ott= "linear", value=blendValue)

        # open curve blend and set driven's
        rotValue = 0.0
        blendValue = 0.0
        for crv in openCurves:
            mc.setDrivenKeyframe("{0}.{1}".format(blendShape, openCurves[-1]),
                                currentDriver="{0}.rotateX".format(eyeCenter), dv=rotValue, itt="linear", 
                                ott= "linear", value=blendValue)
            rotValue+=-40.0/len(closeCurves)
            blendValue+=1.0/len(closeCurves)
            if crv != openCurves[-1]:
                mc.blendShape(blendShape, e=True, ib=True, t=[neutralCurve, 1, crv, blendValue])
            mc.setDrivenKeyframe("{0}.{1}".format(blendShape, openCurves[-1]), 
                                currentDriver="{0}.rotateX".format(eyeCenter), dv=rotValue, itt="linear", 
                                ott= "linear", value=blendValue)


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
            jntBase = mc.joint(name="{0}_{1}_base".format(eyeCenter.lower(), str(i).zfill(3)), 
                                position=eyeCenterPosition)
                                
            #clear the selection before we create the bind joint.
            mc.select(cl=True) 
            #get the vertex position in world space.
            vrtPosition = mc.xform(vrt,q=True,ws=True,t=True)
            jntBind = mc.joint(name="{0}_{1}_bind".format(eyeCenter.lower(), str(i).zfill(3)), 
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
                                                        controlType = "diamond", 
                                                        hierarchy=['nul','ort'],
                                                        parent=None)
            jntDriver = mc.joint(name="{0}_{1}_driver".format(eyeCenter.lower(), str(i).zfill(3)))
            mc.setAttr("{0}.radius".format(jntDriver),.08)
            mc.setAttr("{0}.v".format(jntDriver), 0)
            mc.connectAttr("{0}.position".format(poci), "{0}.t".format(ctrlHierarchy[0]),f=True)
            mc.xform(ctrlHierarchy[1],ws=True,t=vrtPosition)

            loc = mc.spaceLocator(name="{0}_{1}_loc".format(eyeCenter.lower(), str(i).zfill(3)))[0]
            mc.setAttr("{0}Shape.localScale".format(loc),.2,.2,.2)
            poci = mc.createNode("pointOnCurveInfo", name="{0}_loc_poci".format(jntBind))
            mc.setAttr("{0}.parameter".format(poci), param)
            mc.connectAttr("{0}Shape.local".format(blinkCurve), "{0}.inputCurve".format(poci),f=True)
            mc.connectAttr("{0}.position".format(poci), "{0}.t".format(loc),f=True)
            mc.parent(jntBase, bindJointParent)
            mc.aimConstraint(loc,jntBase,aimVector=(1,0,0),upVector=(0,1,0),wut="none")
            mc.setAttr("{0}.v".format(jntDriver))
            driverJntList.append(jntDriver)

        mc.select(driverJntList + [blinkCurve],r=True)
        skinCluster = mc.skinCluster()[0]
        for i,jnt in enumerate(driverJntList):
            parentOfJnt = mc.listRelatives(jnt,p=True)[0]
            mc.connectAttr('{0}.parentInverseMatrix[0]'.format(parentOfJnt),
                            '{0}.bindPreMatrix[{1}]'.format(skinCluster,i), f=True)
