'''
This is a module for libraries used for transforms.
'''
import maya.api.OpenMaya as om
import maya.cmds as mc
import rigrepo.libs.common as common

def getDagPath(node):
    '''
    This will return the dag path of the first node
    it finds with the value of the node name you pass in.

    :param node: Name of the node you want the dagPath for.
    :type node: str
    '''

    # Do some error checking
    if not mc.objExists(node):
        raise RuntimeError("{0} does not exist in the current Maya session.".format(node))


    # get a selection list and the dagPath for the node.
    selList = om.MSelectionList()
    selList.add(node)
    
    return selList.getDagPath(0)



def decomposeRotation(object):
    '''
    Decompose the rotation of the given object. Adds a decomposeTwist attribute to the 
    given object with the resutling decomposed twist. A transform that is only the swing is
    returned.
    Currently assumes x is twist axis
    
    :param object: Object to decmpose twist for
    :type object: str
    :return: Swing transform 
    :rtype: list
    '''
    if not mc.pluginInfo('matrixNodes', q=1, loaded=1):
        mc.loadPlugin('matrixNodes')

    # Variables specific to which twist axis is being decomposed
    # If adding support for other axis these will need to be handled
    twistAxis = 'x'
    vector = (1, 0, 0)
    rotateOrder = 5

    aimTarget = mc.createNode('transform', n=object+'_twist', p=object)
    mc.setAttr(aimTarget+'.t'+twistAxis, 1)
    aimSourceGrp = mc.createNode('transform', n=object+'_swing_grp', p=object)
    aimSource = mc.createNode('transform', n=object+'_swing', p=aimSourceGrp)
    
    # Lock the aimSourceGrp to the parent's orientation.
    parentMatrixDcmp = mc.createNode('decomposeMatrix', n=object+'_parentMatrix_dcmp')
    mc.connectAttr(object+'.inverseMatrix', parentMatrixDcmp+'.inputMatrix')
    mc.connectAttr(parentMatrixDcmp+'.outputRotate', aimSourceGrp+'.rotate')
 
    # aim constriant
    mc.aimConstraint(aimTarget, aimSource, offset=[0, 0, 0],
                     weight=1, aimVector=vector,
                     worldUpType="none",
                     upVector=[0, 0, 0])
    # orient constrain the target to get the twist
    mc.setAttr(aimTarget+'.rotateOrder', rotateOrder)
    mc.orientConstraint(aimSource, aimTarget)

    # Twist attr
    if not mc.objExists(object+'.decomposeTwist'):
        mc.addAttr(object, ln='decomposeTwist', at='double', k=1)
    mc.setAttr(object+'.decomposeTwist', cb=1, k=0)
    reverseEndTwist = mc.createNode('multiplyDivide', n=object+'_reverse_mul')
    mc.setAttr(reverseEndTwist+'.input2X', -1)
    mc.connectAttr(aimTarget+'.r'+twistAxis, reverseEndTwist+'.input1X')
    mc.connectAttr(reverseEndTwist+'.outputX', object+'.decomposeTwist')

    return(aimSource) 

def getAveragePosition(nodes):
    '''
    This will return an average position for nodes passed in.

    :param nodes: Node list you wish to get the average position for.
    :type param: list | tuple
    '''
    # make sure to pass a list to the loop
    node = common.toList(nodes)

    # set the default poition of the point
    point = om.MPoint(0,0,0)
    for node in nodes:
        if not mc.objExists(node):
            raise RuntimeError("{0} doesn't exists in the current Maya session!".format(node))

        # add the new node position to the point
        point += om.MPoint(*mc.xform(node, q=True, ws=True, t=True))

    # devide the point by the amount of nodes that were passed in.
    point = point / len(nodes)

    return (point.x, point.y, point.z)

def getAxis( transform, vector=(0,1,0) ):
    '''Returns the closest axis to the given vector.

    .. python ::

        import maya.cmds as cmds

        # Simple Example
        t = mc.createNode('transform')
        getAxis( t, (1,0,0) )
        # Result: 'x'

        # Joint Example
        j1 = mc.joint(p=(0, 0, 0))
        j2 = mc.joint(p=(0, 0, 2))
        mc.joint( j1, e=True, zso=True, oj='xyz', sao='yup')
        getAxis( j1, (1,0,0) )
        # Result: '-z'

    :param transform: Transform node to calculate the vector from
    :type transform: str
    :param vector: Vector to compare with the transform matrix.
    :type vector: list or tuple
    :returns: x,-x,y,-y,z,-z
    :rtype: str
    '''

    # get dag path
    dpath = getDagPath( transform )

    # get world matrix
    matrix = dpath.inclusiveMatrix()

    # get vectors
    xVector = om.MVector( matrix[0], matrix[1], matrix[2]) 
    yVector = om.MVector( matrix[3], matrix[4], matrix[5])
    zVector = om.MVector( matrix[6], matrix[7], matrix[8])
    vVector = om.MVector( vector[0], vector[1], vector[2] )
    axis   = None
    factor = -1

    # x
    dot = xVector * vVector
    if dot > factor:
        factor = dot
        axis = 'x'

    # -x
    dot = -xVector * vVector
    if dot > factor:
        factor = dot
        axis = '-x'

    # y
    dot = yVector * vVector
    if dot > factor:
        factor = dot
        axis = 'y'

    # -y
    dot = -yVector * vVector
    if dot > factor:
        factor = dot
        axis = '-y'

    # z
    dot = zVector * vVector
    if dot > factor:
        factor = dot
        axis = 'z'

    # -z
    dot = -zVector * vVector
    if dot > factor:
        factor = dot
        axis = '-z'

    return axis      


def getAimAxis ( transform, allowNegative = True):
    '''
    Get transform aim axis based on relatives.
    This is a wrap of getAxis(), uses the average position of the children to pass the vector.

    :param transform: Transform to get the aim axis from.
    :type transform: str

    :param allowNegative: Allow negative axis
    :type allowNegative: bool

    :return: Return aim axis
    :rtype: str
    '''

    pos  = mc.xform( transform, q=True, ws=True, rp=True )
    rel  = getAveragePosition( mc.listRelatives(transform, type="transform"))
    axis = getAxis( transform, (rel[0]-pos[0], rel[1]-pos[1], rel[2]-pos[2] ) )

    if not allowNegative:
        return axis[-1]

    return axis