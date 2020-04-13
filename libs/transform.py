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

def decomposeRotation(object, swingOnly=False, twistAxis='x', rotateOrder=5):
    '''
    Decompose the rotation of the given object. Adds a decomposeTwist attribute to the 
    given object with the resulting decomposed twist. A transform that is only the swing is
    returned.
    Currently assumes x is twist axis
    
    :param object: Object to decmpose twist for
    :type object: str

    :param swingOnly: Whether to use swing only or not.
    :type swingOnly: bool

    :param twistAxis: This should be the twist axis for the object
    :type twistAxis: str

    :param rotateOrder: Rotate order to use
    :type rotateOrder: int

    :return: Swing transform 
    :rtype: list
    '''
    doTwist = not(swingOnly)

    if not mc.pluginInfo('matrixNodes', q=1, loaded=1):
        mc.loadPlugin('matrixNodes')

    # Variables specific to which twist axis is being decomposed
    # If adding support for other axis these will need to be handled
    if twistAxis in ['x', 'X']:
        twistAxis = 'x'
        vector = (1, 0, 0)
    elif twistAxis in ['y', 'Y']:
        twistAxis = 'y'
        vector = (0, 1, 0)
    elif twistAxis in ['z', 'Z']:
        twistAxis = 'z'
        vector = (0, 0, 1)
    elif twistAxis in ['-x', '-X']:
        twistAxis = '-x'
        vector = (-1, 0, 0)
    elif twistAxis in ['-y', '-Y']:
        twistAxis = '-y'
        vector = (0, -1, 0)
    elif twistAxis in ['-z', '-Z']:
        twistAxis = '-z'
        vector = (0, 0, -1)

    aimTarget = mc.createNode('transform', n=object+'_twist', p=object)

    # have to make sure we move the aimTarget in the correct direction
    mc.setAttr(aimTarget+'.t', *vector)
    aimSourceGrp = mc.createNode('transform', n=object+'_swing_grp', p=object)
    aimSource = mc.createNode('transform', n=object+'_swing', p=aimSourceGrp)
    
    # Lock the aimSourceGrp to the parent's orientation.
    # This allows the group to be parented to the object but not receive the objects rotation
    parentMatrixDcmp = mc.createNode('decomposeMatrix', n=object+'_parentMatrix_dcmp')
    mc.connectAttr(object+'.inverseMatrix', parentMatrixDcmp+'.inputMatrix')
    mc.connectAttr(parentMatrixDcmp+'.outputRotate', aimSourceGrp+'.rotate')

    # Swing - get swing with aim constraint
    mc.aimConstraint(aimTarget, aimSource, offset=[0, 0, 0],
                     weight=1, aimVector=vector,
                     worldUpType="none",
                     upVector=[0, 0, 0])
    # Twist - get twist by orientConstraining the aim target to the aimSource (swing)
    #         The aim target has no rotation values since it is a child of the object.
    #         Constraining the aim target to the aimSource, which is only swinging, means
    #         the only rotate values that end up on the aim target is the inverse twist difference
    #         Once we reverse that twist value we have a clean twist.
    if doTwist:
        # orient constrain the target to get the twist
        mc.setAttr(aimTarget+'.rotateOrder', rotateOrder)
        mc.orientConstraint(aimSource, aimTarget)

        # Twist attr
        if not mc.objExists(object+'.decomposeTwist'):
            mc.addAttr(object, ln='decomposeTwist', at='double', k=1)
        mc.setAttr(object+'.decomposeTwist', cb=1, k=0)
        reverseEndTwist = mc.createNode('multiplyDivide', n=object+'_reverse_mul')
        mc.setAttr(reverseEndTwist+'.input2X', -1)
        mc.connectAttr(aimTarget+'.r'+twistAxis.strip("-"), reverseEndTwist+'.input1X')
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

def mirror (trs, search = '_l_', replace = '_r_', axis = "x"):
    '''
    Mirror trs
    It won't create a new trs, it will only mirror the if there is an existing trs with the 
    replace in it matching the name of search and the currvent trs hase search in it.

    ..example ::
         mirror( mc.ls(sl=True) )

    :param joint: Point you want to mirror
    :type joint: str | list

    :param search: Search side token
    :type search: str

    :param replace: Replace side token
    :type replace: str
    '''

    # get given points
    trsList = common.toList(trs)

    # get selection
    selection = mc.ls(sl=True)

    posVector = ()
    if axis.lower() == 'x':
        posVector = (-1,1,1)
        rotVector = (0,180,0)
        scaleVector = (-1,1,1)
    elif axis.lower() == 'y':
        posVector = (1,-1,1)
        rotVector = (180,0,180)
        scaleVector = (1,1,1)
    elif axis.lower() == 'z':
        posVector = (1,1,-1)
        rotVector = (180,180,0)
        scaleVector = (1,1,1)

    # loop through the trs list and mirror across worldspace
    for trs in trsList:
        toTrs = trs.replace( search, replace )

        # check to make sure that both objects exist in the scnene
        if mc.objExists(trs) and mc.objExists(toTrs) and trs != toTrs:
            ortMatrix = om.MMatrix(mc.xform(trs,q=True, ws=True,matrix=True))
            trsMatrix = om.MTransformationMatrix(ortMatrix)
            mc.select(toTrs, r=True)
            selectionList = om.MGlobal.getActiveSelectionList()
            dagNode = selectionList.getDagPath(0)
            fnTransform = om.MFnTransform(dagNode)
            dagVector = fnTransform.translation(om.MSpace.kWorld)
            dagNodeOrtMatrix = om.MMatrix(mc.xform(dagNode.fullPathName(),q=True, ws=True,matrix=True))
            fnTransform.setTransformation(om.MTransformationMatrix(trsMatrix.asMatrixInverse()))
            fnTransform.setTranslation(dagVector, om.MSpace.kWorld)
            mc.setAttr("{}.scale".format(toTrs), *scaleVector)

    # --------------------------------------------------------------------------
    # re-select objects
    if selection:
        mc.select( selection, r=True )
    else:
        mc.select( cl= True)

def getDistanceVector(distance):
    '''
    This is a very specific way we want to grab vector direction when looking for what the aim
    vector is. Usually you want to us a child of a node transform values as the distance attribute.

    :param distance: The vector you want to use to get the direction to be used
    :type distance: list | tuple

    :return: We will return the axis and vector for you to use.
    :rtype: tuple
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

def newMirror (trs, search = '_l_', replace = '_r_', posVector=(-1,1,1), rotVector = (-1,1,1), scaleVector = (1,1,-1)):
    '''
    Mirror trs
    It won't create a new trs, it will only mirror the if there is an existing trs with the 
    replace in it matching the name of search and the currvent trs hase search in it.

    ..example ::
         mirror( mc.ls(sl=True) )

    :param joint: Point you want to mirror
    :type joint: str | list

    :param search: Search side token
    :type search: str

    :param replace: Replace side token
    :type replace: str
    '''

    # get given points
    trsList = common.toList(trs)

    # get selection
    selection = mc.ls(sl=True)

    # loop through the trs list and mirror across worldspace
    for trs in trsList:
        toTrs = trs.replace( search, replace )
        trsPos = mc.xform(trs, q=True, ws=True, t=True)
        # check to make sure that both objects exist in the scnene
        if mc.objExists(trs) and mc.objExists(toTrs) and trs != toTrs:
            ortMatrix = om.MMatrix(mc.xform(trs,q=True, ws=True,matrix=True))
            trsMatrix = om.MTransformationMatrix(ortMatrix)
            mc.select(toTrs, r=True)
            selectionList = om.MGlobal.getActiveSelectionList()
            dagNode = selectionList.getDagPath(0)
            fnTransform = om.MFnTransform(dagNode)
            rotation = trsMatrix.rotation(True)
            transformVector = om.MVector(trsPos[0] * posVector[0], trsPos[1] * posVector[1], trsPos[2] * posVector[2])
            dagNodeOrtMatrix = om.MMatrix(mc.xform(dagNode.fullPathName(),q=True, ws=True,matrix=True))
            newMatrix = om.MTransformationMatrix(trsMatrix.asMatrixInverse())
            newMatrix.setRotation(om.MQuaternion(rotation.x * rotVector[0], rotation.y * rotVector[1], rotation.z * rotVector[2], rotation.w))
            fnTransform.setTransformation(newMatrix)
            fnTransform.setTranslation(transformVector, om.MSpace.kWorld)
            mc.setAttr("{}.scale".format(toTrs), *scaleVector)

    # --------------------------------------------------------------------------
    # re-select objects
    if selection:
        mc.select( selection, r=True )
    else:
        mc.select( cl= True)