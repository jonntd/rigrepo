'''
'''

import maya.cmds as mc

def toList(values):
    '''
    '''
    if not isinstance(values, (list,tuple)):
        values = [values]

    return values

def lock(nodes,attrs):
    '''
    locks attributes
    '''
    nodes = toList(nodes)
    attrs = toList(attrs)

    for node in nodes:
        for attr in attrs:  
            mc.setAttr("{0}.{1}".format(node,attr), lock=True)

def hide(node, attr):
    '''
    '''
    nodes = toList(nodes)
    attrs = toList(attrs)

    for node in nodes:
        for attr in attrs:  
            mc.setAttr("{0}.{1}".format(node,attr), keyable=False)


def lockAndHide(nodes, attrs):
    '''
    '''
    lock(nodes, attrs)
    hide(nodes, attrs)