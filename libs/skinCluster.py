'''
This module is for dealing with skinClusters inside Maya
'''
import maya.cmds as mc

def localize(skinClusters, transform):
    '''
    Localize skinCluster to the given transform

    :param skinCluster: skinCluster to localize
    :type skinCluster: str or list

    :param transform: Transform to localize against
    :type transform: str
    '''
    if isinstance(skinClusters, basestring):
        skinClusters = [skinClusters]
    for skinCluster in skinClusters:
        infs = mc.listConnections(skinCluster+'.matrix', type='transform')
        if not infs:
            return()
        for inf in infs:
           connection = mc.listConnections(inf+'.worldMatrix[0]', p=1, type='skinCluster')
           for con in connection:
               if skinCluster == con.split('.')[0]:
                   index = con.split('[')[1].split(']')[0]
                   # Nothing needs to be done if the bindPreMatrix is hooked up
                   if mc.listConnections('{0}.bindPreMatrix[{1}]'.format(skinCluster, index)):
                       continue
                   multMatrix = '{}__{}_localizeMatrix'.format(inf, skinCluster)
                   if not mc.objExists(multMatrix):
                       multMatrix = mc.createNode('multMatrix', n=multMatrix)
                   if not mc.isConnected(inf+'.worldMatrix[0]', multMatrix+'.matrixIn[1]'):
                       mc.connectAttr(inf+'.worldMatrix[0]', multMatrix+'.matrixIn[1]', f=1)
                   if not mc.isConnected(transform+'.worldInverseMatrix[0]', multMatrix+'.matrixIn[2]'):
                       mc.connectAttr(transform+'.worldInverseMatrix[0]', multMatrix+'.matrixIn[2]', f=1)
                   if not mc.isConnected(multMatrix+'.matrixSum', con):
                       mc.connectAttr(multMatrix+'.matrixSum', con, f=1)
