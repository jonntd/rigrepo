'''
'''

import maya.cmds as mc
import rigrepo.libs.common as common


def lock(node,attr):
    '''
    lock attributes

    :param node: Attribute parent node
    :type node: str | list

    :param attr: Attribute name(s) or path(s)
    :type attr: str or list
    '''
    nodeList = common.toList(node)
    attrList = common.toList(attr)

    for node in nodeList:
        for attr in attrList:  
            mc.setAttr("{0}.{1}".format(node,attr), lock=True)

def hide(node, attr):
    '''
    hide attributes

    :param node: Attribute parent node
    :type node: str | list

    :param attr: Attribute name(s) or path(s)
    :type attr: str or list
    '''
    nodeList = common.toList(node)
    attrList = common.toList(attr)

    for node in nodeList:
        for attr in attrList:  
            mc.setAttr("{0}.{1}".format(node,attr), keyable=False)


def lockAndHide(node, attr):
    '''
    lock and hide attributes

    :param node: Attribute parent node
    :type node: str | list

    :param attr: Attribute name(s) or path(s)
    :type attr: str or list
    '''
    lock(node, attr)
    hide(node, attr)


def unlock(node, attr):
    '''
    unlock attributes

    :param node: Attribute parent node
    :type node: str | list

    :param attr: Attribute name(s) or path(s)
    :type attr: str or list
    '''
    nodeList = common.toList(node)
    attrList = common.toList(attr)

    #lock attributes
    for node in nodeList:
        for attr in attrList:
            mc.setAttr("{0}.{1}".format(node,attr), l = False)


def unhide(node, attr):     
    '''
    unhide attributes

    :param node: Attribute parent node
    :type node: str | list

    :param attr: Attribute name(s) or path(s)
    :type attr: str or list
    '''

    nodeList = common.toList(node)
    attrList = common.toList(attr)

    #lock attributes
    for node in nodeList:
        for attr in attrList:
            mc.setAttr("{0}.{1}".format(node,attr), k = True)    


def unlockAndUnhide(attr, node):
    '''
    unlock and unhide attributes

    :param node: Attribute parent node
    :type node: str | list

    :param attr: Attribute name(s) or path(s)
    :type attr: str or list

    '''
    unlock(attr, node)
    unhide(attr,node)
