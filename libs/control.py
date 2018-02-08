'''
'''
import os
import rigrepo.libs.curve as curve
import rigrepo.libs.common as common
import rigrepo.libs.data.curve_data as curve_data
import maya.cmds as mc

CONTROLPATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','controls.data')

def create(name="control", controlType = "square", hierarchy=['nul'], position=[0,0,0], 
        rotation=[0,0,0], parent=None, color=common.BLUE):
    '''
    '''
    curveData = curve_data.CurveData()
    curveData.read(CONTROLPATH)
    data = curveData.getData()
    control = curve.createCurveFromPoints(data[controlType]['cvPositions'], 
        degree=data[controlType]['degree'],name=name)

    parent = parent

    hierarchyList = []

    if hierarchy:
        for suffix in hierarchy:
            node = mc.createNode("transform", n="{0}_{1}".format(control,suffix))
            if parent:
                mc.parent(node,parent)

            parent = node
            hierarchyList.append(node)

    if parent:
        mc.parent(control, parent)

    mc.xform(hierarchyList[0], ws=True, t=position)
    mc.xform(hierarchyList[0], ws=True, rotation=rotation)

    if color:
        mc.setAttr("{0}.overrideEnabled".format(control), 1)
        mc.setAttr("{0}.overrideColor".format(control), color)

    return hierarchyList + [control]



def tag_as_control(ctrl):
    '''
    :param control: node to tag as a control
    :type control: str or list
    '''
    if not isinstance(ctrl, list):
        if not isinstance(ctrl, basestring):
            raise TypeError('{0} must be of type str, unicode, or list'.format(ctrl))
        ctrls = common.toList(ctrl)
    else:
        ctrls = common.toList(ctrl)

    for ctrl in ctrls:
        tagAttr = attribute.addAttr(ctrl, 'tag_controls', attrType = 'message')

    return tagAttr



def getControls(asset = None):
    '''
    Gets all controls connect to an asset or every control in the scene depending on user input

    :param asset: Asset you wish to look for controls on
    :type asset: str

    :return: List of controls
    :rtype: list
    '''
    controls = None
    if not asset:
        controls = mc.ls('.tag_controls', fl = True)
    elif asset:
        controls = attribute.getConnections('%s.tag_controls' % asset,
                incoming = False,
                plugs = False)

    if controls:
        return controls

    return None

#shapes
#-----------------------
def translateShape (ctrl,
        translation = (0.0, 0.0, 0.0),
        index = 0 ,
        world = False):
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
                curve.getCVs (shape),
                relative = True,
                worldSpace = True)
    else:
        mc.move (translation [0],
                translation [1],
                translation [2],
                curve.getCVs (shape),
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
            curve.getCVs (shape),
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
            curve.getCVs (shape),
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
    shapes = common.getShapes(ctrl)

    #return shape based off of index
    if shapes:
        return shapes[index]

    return None