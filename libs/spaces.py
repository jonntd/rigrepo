'''
Spaces module
'''
# Import Maya modules
import maya.cmds as mc

# Import rigrepo modules
from rigrepo.libs import attribute
from rigrepo.libs import transform
from rigrepo.libs import common

def create( node, attrNode = None , parent=None, spaceAttrName="space"):
    '''
    Create space switcher

    :param node: Transform node to be constrained.
    :type node: str
    :param attrNode: Node where the 'space' attribute is going to be created.
    :type attrNode: str
    :param parent: Parent for the spaces group.
    :type parent: str
    :return: Spaces group
    :rtype: str
    '''
    # Load decompose matrix plugin

    # get attribute node
    if attrNode == None:
        attrNode = node

    # check if exists
    if mc.objExists( '{}.spaceGroup'.format(node)):
        raise RuntimeError, 'This node has spaces already. Use addSpace instead'

    # --------------------------------------------------------------------------
    # CREATE GROUP
    #
    grp = mc.createNode('transform',n='{}{}'.format(node,'Spaces'), parent=parent  )
    mc.setAttr('{}.{}'.format(grp,'inheritsTransform'),False)
    decomMatrixNode = mc.createNode('decomposeMatrix')
    mc.connectAttr( '{}.{}'.format(node,'parentMatrix'), '{}.{}'.format(decomMatrixNode,'inputMatrix') )
    mc.connectAttr( '{}.{}'.format(decomMatrixNode,'outputTranslate'), '{}.{}'.format(grp,'translate') )
    mc.connectAttr( '{}.{}'.format(decomMatrixNode,'outputRotate'), '{}.{}'.format(grp,'rotate') )
    mc.connectAttr( '{}.{}'.format(decomMatrixNode,'outputScale'), '{}.{}'.format(grp,'scale') )

    # --------------------------------------------------------------------------
    # CREATE LOCAL SPACE
    #
    mc.addAttr(attrNode, ln='space', nn=spaceAttrName, at='enum', enumName='local', keyable=True)
    localSpace = mc.createNode('transform', name='{}_{}'.format(grp,'local'), parent=grp)
    mc.xform(localSpace, ws=True, matrix=mc.xform(node, q=True, ws=True, matrix=True))
    attribute.lockAndHide(localSpace, ['t','r','s','v'])

    # --------------------------------------------------------------------------
    # CREATE CONSTRAINT
    #
    constraint = mc.parentConstraint( localSpace, node )[0]

    # --------------------------------------------------------------------------
    # CREATE MESSAGE ATTRIBUTES
    #
    # attrNode
    mc.addAttr( node, k=True, ln='attrNode', at='message' )
    mc.connectAttr( '{}.{}'.format(attrNode,'space'), '{}.{}'.format(node,'attrNode') )

    # node
    mc.addAttr( attrNode, k=True, ln='node', at='message' )
    mc.connectAttr( '{}.{}'.format(node,'message'), '{}.{}'.format(attrNode,'node') )

    # spaceGroup
    mc.addAttr( node, k=True, ln='spaceGroup', at='message' )
    mc.connectAttr( '{}.{}'.format(grp,'message'), '{}.{}'.format(node,'spaceGroup') )

    # spaceConstraint
    mc.addAttr( node, k=True, ln='spaceConstraint', at='message' )
    mc.connectAttr( '{}.{}'.format(constraint,'message'), '{}.{}'.format(node,'spaceConstraint') )
    # --------------------------------------------------------------------------

    return grp

def addSpace(node, targetList, nameList, spaceGroup, attrNode=None, constraintType='parent'):
    '''Adds new space.

    :param node: Transform node to be constrained.
    :type node: str
    :param target: New target for spaces.
    :type target: str
    :param attrNode: Node where the 'space' attribute is going to be created.
    :type attrNode: str
    :param name: Name of the target in the enum attribute.
    :type name: str
    :param constraintType: orient' or 'parent'
    :type constraintType: str
    '''
    targetList = common.toList(targetList)
    for target, name in zip(targetList, nameList):
        # get new spaces
        existingSpaces = mc.attributeQuery( 'space', node=attrNode, listEnum=True)[0].split(':')

        if name in existingSpaces or target in existingSpaces:
            raise RuntimeError, 'There is a space with that name in "{}.{}"'.format(attrNode,'space')

        # edit enum attribute
        mc.addAttr( '{}.{}'.format(attrNode,'space'), e=True, enumName=':'.join(existingSpaces+[name]) )

        # create new space
        newSpace = mc.createNode('transform', name='{}_{}'.format(spaceGroup, name), parent=spaceGroup)
        mc.xform(newSpace, ws=True, matrix=mc.xform(node, q=True, ws=True, matrix=True))
        #mc.setAttr( '{}.{}' .format (newSpace, 'displayLocalAxis') , True)
        if constraintType == 'orient':
            mc.orientConstraint( target, newSpace, mo=True )
        else:
            mc.parentConstraint( target, newSpace, mo=True )

        # create constraint
        constraint = mc.parentConstraint( newSpace, node, mo=True )[0]

        # connect spaces
        # get spaces in constraint
        aliasList  = mc.parentConstraint( constraint, q=True, weightAliasList=True )
        targetList = mc.parentConstraint( constraint, q=True, targetList=True )

        # key constraint
        for i in range(len(aliasList)):

            # Create Condition Node ( R: used for weight, G: used for node state )
            condNode = mc.createNode('condition')
            mc.setAttr( '{}.{}'.format(condNode,'operation'), 0 ) # < equal
            mc.setAttr( '{}.{}'.format(condNode,'secondTerm'), i )
            mc.connectAttr( '{}.{}'.format(attrNode,'space'), '{}.{}'.format(condNode, 'firstTerm'), f=True )

            # Weight Condition
            mc.setAttr( '{}.{}'.format(condNode,'colorIfTrueR'), 1 )
            mc.setAttr( '{}.{}'.format(condNode,'colorIfFalseR'), 0 )
            mc.connectAttr( '{}.{}'.format(condNode,'outColorR'), '{}.{}'.format(constraint, aliasList[i]), f=True )