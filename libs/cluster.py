'''
This is the module that will house functions and classes that have to do with clusters.
'''
import maya.cmds as mc
import rigrepo.libs.common
def create(mesh,name,parent=None,contraintTypes=['point','orient','scale'], 
    parallel=False, modelTransform="model", local=True):
    '''
    This will create a localized cluster.

    :param mesh: mesh to create cluster on.
    :type mesh: str | list

    :param name: The name you wish to use for the cluster when naming it.
    :type name: str

    :param parent: The parent of the cluster
    :type parent: str

    :param constraintTypes: The different type of constraints you want the cluster to have.
    :type constraintTypes: list

    :return: The cluster which was created by this function
    :rtype: str 
    '''
    for nodeName in [name+'_nul',name+'_ort',name+'_auto',name+'_hdl',name+'_cls_hdl']:
        node = mc.createNode('transform',n=nodeName)
        mc.parent(node,parent)
        parent = node
    
    parent = name+'_auto'
    for nodeName in [name+'_def_auto',name+'_ctrl']:
        node = mc.createNode('transform',n=nodeName)
        mc.parent(node,parent)
        parent = node
    
    mc.select(mc.ls(mesh),r=True)
    # create and localize the cluster
    cls = mc.cluster(name=name, wn=[name+'_cls_hdl',name+'_cls_hdl'],bs=1, par=parallel)[0]
    if local:
        localize(cls, name+'_auto', modelTransform)
    

    if 'orient' in contraintTypes:
        mc.orientConstraint(name+'_ctrl',name+'_cls_hdl')
    if 'point' in contraintTypes:
        mc.pointConstraint(name+'_ctrl',name+'_cls_hdl')
    if 'scale' in contraintTypes:
        mc.scaleConstraint(name+'_ctrl',name+'_cls_hdl')
    
    return cls

def localize(cluster, transform, modelTransform, weightedCompensation=False):
    for i, geometry in enumerate(mc.cluster(cluster, q=True, geometry=True)):
        parentTransform = mc.listRelatives(geometry, p=True) or listRelatives
        if parentTransform:
            mc.connectAttr(parentTransform[0]+'.worldMatrix', cluster+'.geomMatrix[{}]'.format(i), f=True)
        else:
            mc.connectAttr(modelTransform+'.worldMatrix', cluster+'.geomMatrix[{}]'.format(i), f=True)
    mc.connectAttr(transform+'.worldInverseMatrix', cluster+'.bindPreMatrix', f=True)
    if weightedCompensation:
        mc.connectAttr(transform+'.worldInverseMatrix', cluster+'.weightedCompensationMatrix', f=True)

def getClusters(geometry):
    '''
    This will check the geometry to see if it has a cluster in it's histroy stack

    :param geometry: The mesh you want to check for a cluster
    :type geometry: str
    '''
    # check the history to see if there is a cluster
    hist = [node for node in mc.listHistory(geometry, pdo=True) if mc.nodeType(node) == "cluster"]
    hist.reverse()
    return hist

def transferCluster(source, target, deformer, handle=False, surfaceAssociation="closestPoint", createNew=True):
    '''
    This will transfer cluster from one mesh to another. If the target doesn't have a
    cluster on it, it will create a new cluster. Then once there is a cluster
    We will copy weights over.

    :param source: The geomertry you are transfer from
    :type source:  str

    :param target: The geometry you want to transfer to
    :type target: str | list

    :param surfaceAssociation: How to copy the weights from source to target available values 
                                are "closestPoint", "rayCast", or "closestComponent"
    :type surfaceAssociation: str
    '''
    # do some error checking
    if not mc.objExists(source):
        raise RuntimeError('The source mesh "{}" does not exist in the current Maya session.'.format(source))
    if not isinstance(surfaceAssociation, basestring):
        raise TypeError('The surfaceAssociation argument must be a string.')
    if deformer:
        if not mc.objExists(deformer):
            raise RuntimeError("{} doesn't exist in the current Maya session!".format(deformer))

    # first we will turn the target into a list if it's not already a list
    meshList = rigrepo.libs.common.toList(target)
    
    # make sure we have a cluster on the source mesh
    clusterList = list()
    for mesh in meshList:
        if not mc.objExists(mesh):
            mc.warning('The target mesh "{}" does not exist in the current Maya session.'.format(target))
            continue

        # check to see if there is a cluster already  on the target mesh
        hist = [node for node in mc.ls(mc.listHistory(mesh, pdo=True, il=1), type='geometryFilter') if mc.nodeType(node) == "cluster"]

        # if there is no cluster, we will create one.
        newDeformer = "{}__{}".format(mesh, deformer)
        if deformer not in hist and not createNew:
            mc.sets(mc.ls("{}.cp[*]".format(mesh))[0], e=True, add="{}Set".format(deformer))
            newDeformer = deformer
        elif createNew:
            if not newDeformer in hist:
                if handle:
                    clsHandle = mc.cluster(deformer, q=True, wn=True)
                    mc.cluster(mesh, name=newDeformer, wn=[clsHandle, clsHandle], bs=True)
                else:
                    mc.cluster(mesh, name=newDeformer, bs=True)
        else:
            newDeformer = deformer

        clusterList.append(newDeformer)

        # now we will transfer the wts
        mc.copyDeformerWeights(ss=source, ds=mesh, sd=deformer, dd=newDeformer,
                                sa=surfaceAssociation, noMirror=True)

    return clusterList


def mirror():
    pass
