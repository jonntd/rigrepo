'''
'''
import os
from collections import OrderedDict
import rigrepo.libs.curve 
import rigrepo.libs.common 
import rigrepo.libs.data.curve_data
import rigrepo.libs.attribute
import maya.cmds as mc

CONTROLPATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','controls.data')
DEBUG = False
def create(name="control", controlType = "square", hierarchy=['nul'], position=[0,0,0],
        rotation=[0,0,0], hideAttrs=['v'], parent=None, color=rigrepo.libs.common.BLUE, 
        transformType="transform"):
    '''
    This function will create a control hierarchy based on the arguments that are passed in. 
    It will also make sure the control is tagged properly.

    :param name: Name you wish to use for the control.
    :type name: str

    :param controlType: The shape you would like to use for the control.
    :type controlType: str

    :param hierarchy: List of nodes to be created as parents of the control
    :type hierarchy: list | tuple

    :param position: Point in space where the control will be positioned in the scene
    :type position: list | tuple

    :param rotation: Rotation in space where the control will be rotated in the scene
    :type rotation: list | tuple

    :param hideAttrs: List of attributes you wish to lock and hide from the channel box.
    :type hideAttrs: list | tuple

    :param parent: Parent for the controls nul node
    :type parent: str

    :param color: Color you 
    :type color: int

    :param transformType: Type of transform for the control. (i.e "transform", "joint")
    :type transformType: str
    '''
    curveData = rigrepo.libs.data.curve_data.CurveData()
    curveData.read(CONTROLPATH)
    data = curveData.getData()
    if data.has_key(controlType):
        shapeList = data[controlType]["shapes"].keys()
        for shape in shapeList:
            if shape == shapeList[0]:
                control = rigrepo.libs.curve.createCurveFromPoints(data[controlType]["shapes"][shape]['cvPositions'], 
                    degree=data[controlType]['shapes'][shape]['degree'],name=name, transformType=transformType)
                continue
            curve = rigrepo.libs.curve.createCurveFromPoints(data[controlType]["shapes"][shape]['cvPositions'], 
                    degree=data[controlType]['shapes'][shape]['degree'],name=name, transformType=transformType)
            curveShape = mc.listRelatives(curve, c=True, shapes=True)[0]
            mc.parent(curveShape, control, r=True, s=True)
            mc.rename(curveShape, "{}Shape".format(control))
            mc.delete(curve)
    elif controlType == "circle":
        if not hierarchy:
            control = name
        else:
            control = mc.createNode(transformType, name=name)

        curve = mc.circle(name=name+'_curve', c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1,
                          d=3, ut=0, tol=0.01, s=8, ch=False) [0]
        curveShape = mc.parent(mc.listRelatives(curve, c=True, shapes=True, type="nurbsCurve")[0], control, r=True, s=True)
        mc.rename(curveShape, control+'Shape')

        mc.delete(curve)
    else:
        control = mc.createNode(transformType, name=name)
        mc.setAttr("{0}.displayHandle".format(control), 1)

    if transformType == "joint":
        hideAttrs.append("radius")

    for attr in hideAttrs:
        if mc.objExists(control+'.'+attr):
            mc.setAttr(control+'.'+attr, k=0, cb=0)

    parent = parent

    hierarchyList = []

    # If there is a hierarchy argument passed in. We will loop through and create the hiearchy.
    if hierarchy:
        for suffix in hierarchy:
            node = mc.createNode("transform", n="{0}_{1}".format(control,suffix))
            if parent:
                mc.parent(node,parent)

            parent = node
            hierarchyList.append(node)

    # parent the control to the last hierachy node created.
    if parent:
        mc.parent(control, parent)

    if position and hierarchyList:
        mc.xform(hierarchyList[0], ws=True, t=position)
        
    if rotation and hierarchyList:
        mc.xform(hierarchyList[0], ws=True, rotation=rotation)

    if color:
        mc.setAttr("{0}.overrideEnabled".format(control), 1)
        mc.setAttr("{0}.overrideColor".format(control), color)

    if mc.nodeType(control) == "joint":
        mc.setAttr("{}.drawStyle".format(control), 2)

    tagAsControl(control)

    return hierarchyList + [control]



def tagAsControl(ctrl):
    '''
    :param control: node to tag as a control
    :type control: str or list
    '''
    if not isinstance(ctrl, (tuple,list)):
        if not isinstance(ctrl, basestring):
            raise TypeError('{0} must be of type str, unicode, or list'.format(ctrl))
        ctrls = rigrepo.libs.common.toList(ctrl)
    else:
        ctrls = rigrepo.libs.common.toList(ctrl)

    for ctrl in ctrls:
        tagAttr = '{}.__control__'.format(ctrl)
        if not mc.objExists(tagAttr):
            mc.addAttr(ctrl, ln='__control__', at = 'message')

    return tagAttr


def untagAsControl(ctrl):
    '''
    :param control: node to tag as a control
    :type control: str or list
    '''
    if not isinstance(ctrl, (tuple,list)):
        if not isinstance(ctrl, basestring):
            raise TypeError('{0} must be of type str, unicode, or list'.format(ctrl))
        ctrls = rigrepo.libs.common.toList(ctrl)
    else:
        ctrls = rigrepo.libs.common.toList(ctrl)

    for ctrl in ctrls:
        tagAttr = '{}.__control__'.format(ctrl)
        if mc.objExists(tagAttr):
            mc.deleteAttr(ctrl, at='__control__')


def getControls(namespace = None):
    '''
    Gets all controls connect to an asset or every control in the scene depending on user input

    :param namespace: Asset you wish to look for controls on
    :type namespace: str

    :return: List of controls
    :rtype: list
    '''
    controls = None
    if not namespace:
        controls = mc.ls('*.__control__'.format(), fl=True, o=True)
    elif namespace:
        controls = mc.ls('{}:*.__control__'.format(namespace), fl=True, o=True)

    return controls

def setPoseAttr(controls, poseAttr=0):
    '''
    This will store all of the keyable attribute values at the time this function is called. 
    It will use the pose attr argument to figure out where to store it. If the attribute 
    already exist. It will just overwrite it.

    .. example:
        setPoseAttr(rigrepo.libs.control.getControls())
        setPoseAttr(rigrepo.libs.control.getControls(),1)

    :param controls: list of controls that you want to set pose on
    :type controls: str | list

    :param poseAttr: Attribute value you want to store this pose at.
    :type poseAttr: int
    '''
    # make sure the controls are set as a list.
    controls = rigrepo.libs.common.toList(controls)
    skipAttrs = ("message")
    skipAttrList = ["ikfk_switch"]
    for ctrl in controls:
        # store the attribute names
        ctrlPoseAttr = "{}.poseAttr_{}".format(ctrl,poseAttr)
        poseAttrName = ctrlPoseAttr.split(".")[-1]
        ctrlAttrDict = OrderedDict()

        # go through each attribute and store it in the dictionary
        for attr in mc.listAttr(ctrl, keyable=True):
            if not mc.getAttr("{}.{}".format(ctrl,attr),type=True) in skipAttrs and not attr in skipAttrList:
                ctrlAttrDict[str(attr)] = mc.getAttr("{}.{}".format(ctrl,attr))

        # if the pose doesn't exist, then we will create it.
        if not poseAttrName in mc.listAttr(ctrl):
            mc.addAttr(ctrl, ln=poseAttrName, dt= "string")

        # set the attribute
        mc.setAttr(ctrlPoseAttr, str(ctrlAttrDict), type="string")

def toPoseAttr(controls, poseAttr=0):
    '''
    This will set the pose based on the way it was stored using setPoseAttr

    .. example:
        toPoseAttr(rigrepo.libs.control.getControls())
        toPoseAttr(rigrepo.libs.control.getControls(),1)

    :param controls: list of controls that you want to set pose on
    :type controls: str | list

    :param poseAttr: Attribute value you want to store this pose at.
    :type poseAttr: int
    '''
    # Make sure the controls are a list.
    controls = rigrepo.libs.common.toList(controls)
    
    # loop throught the controls and try and set the attributes back to the way they were stored.
    for ctrl in controls:
        ctrlPoseAttr = "{}.poseAttr_{}".format(ctrl,poseAttr)
        poseAttrName = ctrlPoseAttr.split(".")[-1]

        # check to see if the attribute exists.
        if not poseAttrName in mc.listAttr(ctrl):
            continue

        # if the attribute exists then we can eval it into an OrderedDict        
        ctrlAttrDict = eval(mc.getAttr(ctrlPoseAttr))

        # loop through the attributes and set them if we can.
        for attr in ctrlAttrDict:
            try:
                # set the attributes if we can.
                mc.setAttr("{}.{}".format(ctrl,attr), ctrlAttrDict[attr])
            except:
                # raise a warning for now if we can't set it. 
                #Usually this is because it's connected or locked.
                if DEBUG:
                    mc.warning("Couldn't set {}.".format(attr))

#shapes
#-----------------------
def translateShape (ctrl, translation = (0.0, 0.0, 0.0), index = 0 , world = False):
    '''
    Rotate control shape

    :param ctrl: Animation control
    :type ctrl: str

    :param translation: Translation vector
    :type translation: list

    :param index: Shape index
    :type index: int
    '''
    # Get control shape
    shape = getShape (ctrl, index)

    # Translate shape
    if world:
        mc.move (translation [0],
                translation [1],
                translation [2],
                rigrepo.libs.curve.getCVs (shape),
                relative = True,
                worldSpace = True)
    else:
        mc.move (translation [0],
                translation [1],
                translation [2],
                rigrepo.libs.curve.getCVs (shape),
                relative = True,
                objectSpace = True)

def rotateShape (ctrl, rotation = (0.0, 0.0, 0.0), index = 0):
    '''
    Rotate control shape

    :param ctrl: Animation control
    :type ctrl: str

    :param rotation: Rotation vector
    :type rotation: list

    :param index: Shape index
    :type index: int
    '''
    # Get control shape
    shape = getShapes(ctrl, index)

    # Rotate shape
    mc.rotate (rotation [0],
            rotation [1],
            rotation [2],
            rigrepo.libs.curve.getCVs (shape),
            relative = True,
            objectSpace = True)

def scaleShape (ctrl, scale = [1, 1, 1], index = 0):
    '''
    Rotate control shape

    :param ctrl: Animation control
    :type ctrl: str

    :param scale: Scale vector
    :type scale: list

    :param index: Shape index
    :type index: int
    '''
    # Get control shape
    shape = getShape (ctrl, index)

    # Scale shape
    mc.scale (scale [0],
            scale [1],
            scale [2],
            rigrepo.libs.curve.getCVs (shape),
            relative = True )

def getShape(ctrl, index = 0):
    '''
    gets shape based on index

    :param ctrl: Control you wish to get shape on
    :type ctrl: str

    :param index: Index of the shape on the control
    :type index: int
    '''
    #get shapes
    shapes = mc.listRelatives(ctrl, c=True, type="shape")

    #return shape based off of index
    if shapes:
        return shapes[index]

    return None


def displayLine(point1, point2, name = 'ctrlLine#', parent = str(), displayType=2):
    '''
    Create a display line between two points

    Example:
    ..python
        displayLine('l_uparm_sc_jnt', 'l_uparm_pv_ctrl')
        #Return: 'ctrlLine1'

        displayLine('l_uparm_sc_jnt', 'l_uparm_pv_ctrl', name = 'l_uparm_pv_displayLine')
        #Return: 'l_uparm_pv_displayLine'

    :param point1: First node to connect display line to
    :type point1: str

    :param point2: Second node to connect display line to
    :type point2: str

    :param displayType: Whether to display it as a reference or template
    :type displayType: int

    :return: Display line
    :rtype: str

    '''
    # make sure displayType is correct. If not, than instead of throwing an error. We will just
    # make sure it's set properly and let the code execute.
    if displayType not in [0,1,2]:
        mc.warning("The displayType argument must be (0,1,2). Currently it is {}. We're setting it to 2 for you since you passed in the incorrect value".format(displayType))
        displayType = 2
    #get posiitons of first and second points
    pnt1 = mc.xform(point1, q =True, ws = True, t = True)
    pnt2 = mc.xform(point2, q =True, ws = True, t = True)

    #create a pointList from point1 and point2 positions
    pointList = (pnt1,pnt2)

    #create display line from pointList
    displayLine = rigrepo.libs.curve.createCurveFromPoints(pointList, degree = 1, name = name)

    #cluster the two ends of the dispay line to point1 and point2
    mc.cluster( '{}.cv[0]'.format(displayLine),
            wn = [point1,point1],
            bs = True,
            name = '{}_1_{}'.format(displayLine, rigrepo.libs.common.CLUSTER))

    mc.cluster('{}.cv[1]'.format(displayLine),
            wn = [point2,point2],
            bs = True,
            name = '{}_2_{}'.format(displayLine, rigrepo.libs.common.CLUSTER))

    #override display type of displayLine to be templated
    mc.setAttr('{}.overrideEnabled'.format(displayLine), 1)
    mc.setAttr('{}.overrideDisplayType'.format(displayLine), displayType)
    mc.setAttr('{}.inheritsTransform'.format(displayLine), 0)

    if parent:
        mc.parent(displayLine, parent)

    return displayLine