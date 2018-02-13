'''
This is a module for libraries used for transforms.
'''
import maya.api.OpenMaya as om
import maya.cmds as mc

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