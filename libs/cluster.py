'''
This is the module that will house functions and classes that have to do with clusters.
'''
import maya.cmds as mc

def create(mesh,name,parent=None,contraintTypes=['point','orient','scale'], 
    parallel=False, modelTransform="model", local=True):
    '''
    This will create a localized cluster.

    :param mesh: mesh to create cluster on.
    :type mesh: str

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
    
    mc.select(mesh,r=True)
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

def localize(cluster, transform, modelTransform):
    mc.connectAttr(modelTransform+'.worldMatrix', cluster+'.geomMatrix[0]', f=True)
    mc.connectAttr(transform+'.worldInverseMatrix', cluster+'.bindPreMatrix', f=True)
    #mc.connectAttr(transform+'.worldInverseMatrix', cluster+'.weightedCompensationMatrix', f=True)
