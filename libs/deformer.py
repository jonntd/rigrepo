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

def copyDeformer(deformer, target):
    '''
    Make a copy of the passed deformers on the target

    :param target: Target transform of shape
    :param deformers: deformers to copy
    :return: Copied deformers
    '''

    if mc.nodeType(deformer) == 'wire':
        # Get data
        curve = mc.wire(deformer, q=1, wire=1)[0]
        baseCurve = mc.listConnections(deformer+'.baseWire[0]', p=1)[0]
        deformerOrder= mc.listHistory(target, pdo=1, il=2)
        print('order', deformerOrder)
        orderIndex = deformerOrder.index(deformer)
        # Note: wire command has issues when passing the shape, so get the transform
        curve = mc.listRelatives(curve, p=1)[0]
        rotation = mc.getAttr(deformer+'.rotation')
        dropOffDistance = mc.getAttr(deformer+'.dropoffDistance[0]')
        mc.select(cl=1)
        wireDeformer = mc.wire(target,
                               groupWithBase=False,
                               envelope=1.00,
                               crossingEffect=0.00,
                               localInfluence=0.00,
                               wire=curve,
                               name="{}_wire".format(target))[0]
        # Replace base curve
        newBaseCurve = mc.listConnections(wireDeformer+'.baseWire[0]')
        mc.connectAttr(baseCurve, wireDeformer+'.baseWire[0]', f=1)
        mc.delete(newBaseCurve)

        # Reorder deformer
        if orderIndex:
            mc.reorderDeformers(deformerOrder[orderIndex-1], wireDeformer, target)

        # set the default values for the wire deformer
        mc.setAttr("{}.rotation".format(wireDeformer), rotation)
        mc.setAttr("{}.dropoffDistance[0]".format(wireDeformer), dropOffDistance)
        return wireDeformer

def makeDeformerUnique(deformer, target):
    '''

    :param deformer:
    :param target:
    :return:
    '''
    copyDeformer(deformer, target)
    mc.deformer(deformer, e=1, rm=1, g=target)


