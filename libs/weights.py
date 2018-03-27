import maya.cmds as mc
import 
def setWeights(node, weights, map=None): 
    '''
    Sets weights for specified deformers.

    :param node: Deformer name
    :type node: str
    :param weights: List of tuples. [(pntIndex, value),...]
    :type weights: List
    :param map: Name of influence or deformer map to assing weights to.
    :type map: str
    :returns: None
    '''

    if mc.nodeType(node) == 'skinCluster': 
        # find the inf index 
        inf = map
        infIndex = None 
        con = mc.listConnections(inf+'.worldMatrix[0]', p=1, d=1, s=0) 
        for c in con: 
            if node+'.matrix' in c: 
                infIndex = c.split('[')[1][:-1] 
        if infIndex:
            for weight in weights: 
                pntIndex,value = weight
                mc.setAttr(node+'.wl['+pntIndex+'].w['+infIndex+']', value) 

    if mc.nodeType(node) == 'cluster': 
        for w in weights: 
            pntIndex,value = weight
            mc.setAttr(node+'.wl[0].w['+pntIndex+']', value) 


def getWeights(node, map=None):
    '''
    Gets weights for specified deformers.

    :param node: Deformer name
    :type node: str
    :param weights: List of tuples. [(pntIndex, value),...]
    :type weights: List
    :param map: Name of influence or deformer map to assing weights to.
    :type map: str
    :returns: None
    '''

    if mc.nodeType(node) == 'skinCluster': 
        # find the inf index 
        inf = map
        infIndex = None 
        con = mc.listConnections(inf+'.worldMatrix[0]', p=1, d=1, s=0) 
        for c in con: 
            if node+'.matrix' in c: 
                infIndex = c.split('[')[1][:-1] 
        if infIndex:
            for weight in weights: 
                pntIndex,value = weight
                mc.getAttr(node+'.wl['+pntIndex+'].w['+infIndex+']', value) 

    if mc.nodeType(node) == 'cluster': 
        for w in weights: 
            pntIndex,value = weight
            mc.setAttr(node+'.wl[0].w['+pntIndex+']', value) 
