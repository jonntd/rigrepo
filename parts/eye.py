'''
This is not broken up into pieces yet. Just putting it here to hace access and work on it.
PLEASE DON'T MESS WITH THIS FILE!
'''
'''
import maya.cmds as cmds
import maya.api.OpenMaya as om
import japeto.libs.curve as jcurve
reload(jcurve)
import rigtools.libs.control as control

#Object used for the eye center location
eyeCenter = "eyeSocket_l_bind"
neutralCurve = "lidUpper_l_neutral"
blinkCurve = "lidUpper_l_blink"
# variable to store all of the lid joints which will be used
# when binding to the mesh.
bindJointList = list()
# loop through the vrts on the lid and create the joint setup
# CURRENTLY WERE USING SELECTION.
#====================================
# get the position of the eyeCenter
eyeCenterPosition = cmds.xform(eyeCenter,q=True,ws=True,t=True)
selList = om.MSelectionList()
selList.add(neutralCurve)
curveDagPath = selList.getDagPath(0)
curveDagPath.extendToShape()
curveFn = om.MFnNurbsCurve(curveDagPath)
driverJntList = list()
for i,vrt in enumerate(cmds.ls("{0}.cv[*]".format(neutralCurve),fl=True)):
    #clear the selection first.
    cmds.select(cl=True) 
    jntBase = cmds.joint(name="lidUpper_l_{0}_base".format(str(i).zfill(3)),position=eyeCenterPosition)
    #clear the selection before we create the bind joint.
    cmds.select(cl=True) 
    #get the vertex position in world space.
    vrtPosition = cmds.xform(vrt,q=True,ws=True,t=True)
    jntBind = cmds.joint(name="lidUpper_l_{0}_bind".format(str(i).zfill(3)),position=vrtPosition)
    # parent the bind joint to the base joint.
    cmds.parent(jntBind,jntBase)
    #orient the joint
    cmds.joint(jntBase,e=True,oj="xyz",secondaryAxisOrient= "yup")
    # set the bind joint to match the orientation of the base joint.
    cmds.setAttr("{0}.jo".format(jntBind),0,0,0)
    cmds.setAttr("{0}.radius".format(jntBind),.08)
    cmds.setAttr("{0}.radius".format(jntBase),.08)
    
    #point on curve info node
    closestPoint = curveFn.closestPoint(om.MPoint(*vrtPosition))[0]
    param = jcurve.getParamFromPosition(neutralCurve,[closestPoint.x,closestPoint.y,closestPoint.z])
    poci = cmds.createNode("pointOnCurveInfo", name="{0}_poci".format(jntBind))
    cmds.setAttr("{0}.parameter".format(poci), param)
    cmds.connectAttr("{0}.local".format(curveDagPath.fullPathName()), "{0}.inputCurve".format(poci),f=True)
    ctrlHierarchy = control.createControl(name=jntBind.replace("_bind",""), controlType = "diamond", hierarchy=['nul','ort'],parent=None)
    jntDriver = cmds.joint(name="lidUpper_l_{0}_driver".format(str(i).zfill(3)))
    cmds.setAttr("{0}.t".format(jntDriver))
    cmds.connectAttr("{0}.position".format(poci), "{0}.t".format(ctrlHierarchy[0]),f=True)
    cmds.xform(ctrlHierarchy[1],ws=True,t=vrtPosition)

    loc = cmds.spaceLocator(name="lidUpper_l_{0}_loc".format(str(i).zfill(3)))[0]
    cmds.setAttr("{0}Shape.localScale".format(loc),.2,.2,.2)
    poci = cmds.createNode("pointOnCurveInfo", name="{0}_loc_poci".format(jntBind))
    cmds.setAttr("{0}.parameter".format(poci), param)
    cmds.connectAttr("{0}Shape.local".format(blinkCurve), "{0}.inputCurve".format(poci),f=True)
    cmds.connectAttr("{0}.position".format(poci), "{0}.t".format(loc),f=True)
    cmds.parent(jntBase,eyeCenter)
    cmds.aimConstraint(loc,jntBase,aimVector=(1,0,0),upVector=(0,1,0),wut="none")
    cmds.setAttr("{0}.v".format(jntDriver))
    driverJntList.append(jntDriver)

cmds.select(driverJntList + [blinkCurve],r=True)
skinCluster = cmds.skinCluster()[0]
for i,jnt in enumerate(driverJntList):
    parentOfJnt = cmds.listRelatives(jnt,p=True)[0]
    mc.connectAttr('{0}.parentInverseMatrix[0]'.format(parentOfJnt),'{0}.bindPreMatrix[{1}]'.format(skinCluster,i),f=True
'''