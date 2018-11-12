'''
This is the module that will house functions and classes that have to do with clusters.
'''
import maya.cmds as mc

def create(mesh,suffix,parent=None,contraintTypes=['point','orient','scale']):
    '''
    This will create a localized cluster.

    :param mesh: mesh to create cluster on.
    :type mesh: str

    :param suffix: The suffix you wish to use for the cluster when naming it.
    :type suffix: str

    :param parent: The parent of the cluster
    :type parent: str

    :param constraintTypes: The different type of constraints you want the cluster to have.
    :type constraintTypes: list

    :return: The cluster which was created by this function
    :rtype: str 
    '''
    for name in [suffix+'_nul',suffix+'_ort',suffix+'_auto',suffix+'_hdl',suffix+'_cls_hdl']:
        node = mc.createNode('transform',n=name)
        mc.parent(node,parent)
        parent = node
    
    parent = suffix+'_auto'
    for name in [suffix+'_def_auto',suffix+'_ctrl']:
        node = mc.createNode('transform',n=name)
        mc.parent(node,parent)
        parent = node
    
    mc.select(mesh,r=True)
    cls = mc.cluster(wn=[suffix+'_cls_hdl',suffix+'_cls_hdl'],bs=1)[0]
    mc.connectAttr(suffix+'_hdl'+'.inverseMatrix',cls+'.weightedCompensationMatrix',f=True)
    mc.connectAttr(suffix+'_def_auto'+'.parentInverseMatrix',cls+'.bindPreMatrix',f=True)
    
    if 'orient' in contraintTypes:
        mc.orientConstraint(suffix+'_ctrl',suffix+'_hdl')
    if 'point' in contraintTypes:
        mc.pointConstraint(suffix+'_ctrl',suffix+'_hdl')
    if 'scale' in contraintTypes:
        mc.scaleConstraint(suffix+'_ctrl',suffix+'_hdl')
        
    return cls
    
def localize(cluster, transform):
    mc.connectAttr(transform+'.worldMatrix', cluster+'.geomMatrix[0]', f=True)
    mc.connectAttr(transform+'.worldInverseMatrix', cluster+'.weightedCompensationMatrix', f=True)
    mc.connectAttr(transform+'.worldInverseMatrix', cluster+'.bindPreMatrix', f=True)
