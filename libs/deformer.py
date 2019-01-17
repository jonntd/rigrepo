'''
This module will house functions dealing with deformer based operations.
'''
# Maya modules
import maya.cmds as mc

# Python modules

# rigrepo Modules
import rigrepo.libs.common
import rigrepo.libs.skinCluster
import rigrepo.libs.cluster

def transferDeformers(source, target, deformerTypes = ["skinCluster"],
                        surfaceAssociation="closestPoint"):
    '''
    This will transfer all deformers and weights. If it's the same

    :param source: The geomertry you are transfer from
    :type source:  str

    :param target: The geometry you want to transfer to
    :type target: str | list

    :param surfaceAssociation: How to copy the weights from source to target available values 
                                are "closestPoint", "rayCast", or "closestComponent"
    :type surfaceAssociation: str
    '''
    # do some error checking
    hist = [node for node in mc.listHistory(source, pdo=True, interestLevel=1) if mc.nodeType(node) in deformerTypes]
    if hist:
        if 'skinCluster' in deformerTypes:
            rigrepo.libs.skinCluster.transferSkinCluster(source, target, surfaceAssociation)
        elif 'cluster' in deformerTypes:
            for cluster in rigrepo.libs.cluster.getClusters(source):
                rigrepo.libs.cluster.transferCluster(source, target, cluster, handle=True, surfaceAssociation="closestPoint", createNew=True)
