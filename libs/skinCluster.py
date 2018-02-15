import maya.cmds as mc

def localize(skinCluster, transform):
    '''
    Localize skinCluster to the given transform

    :param skinCluster: skinCluster to localize
    :type skinCluster: str

    :param transform: Transform to localize against
    :type transform: str
    '''
    infs = mc.listConnections(skinCluster+'.matrix', type='transform')
    if not infs:
        return()
    for inf in infs:
       connection = mc.listConnections(inf+'.worldMatrix[0]', p=1, type='skinCluster')
       for con in connection:
           if skinCluster == con.split('.')[0]:
               multMatrix = '{}_{}_matrixMul'.format(inf, skinCluster)
               if not mc.objExists(multMatrix):
                   multMatrix = mc.createNode('multMatrix', n=multMatrix)
               if not mc.isConnected(inf+'.worldMatrix[0]', multMatrix+'.matrixIn[1]'):
                   mc.connectAttr(inf+'.worldMatrix[0]', multMatrix+'.matrixIn[1]', f=1)
               if not mc.isConnected(transform+'.worldInverseMatrix[0]', multMatrix+'.matrixIn[2]'):
                   mc.connectAttr(transform+'.worldInverseMatrix[0]', multMatrix+'.matrixIn[2]', f=1)
               if not mc.isConnected(multMatrix+'.matrixSum', con):
                   mc.connectAttr(multMatrix+'.matrixSum', con, f=1)
