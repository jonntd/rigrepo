'''
This is the module that will house functions and classes that have to do with clusters.
'''
import maya.cmds as mc
import rigrepo.libs.common
import rigrepo.libs.weights
import numpy

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


def convertClustersToSkinCluster(newSkinName, targetGeometry, clusterDeformerList, keepClusters=False, 
    rootParentNode="rig", rootPreMatrixNode="trs_aux", jointDepth=2):
    '''
    This function will take in a wire deformer list and create a new skinCluster

    :param newSkinName: This is the name we will use for the new skinCluster we're creating.
    :type newSkinName: str

    :param targetGeometry: This is the geometry we will be putting the skinCluster onto.
    :type targetGeometry: str
    '''
    target = targetGeometry
    # Get existing wire deformers from the wireDeformerList
    convertClusterList = mc.ls(clusterDeformerList, type="cluster")

    # Store the connection to the shape
    geo_input = mc.listConnections(targetGeometry+'.inMesh', p=1)[0]

    # Store deformation order
    deformer_order = mc.listHistory(target, pdo=1, il=2)
    reorder_deformer = None
    for deformer in clusterDeformerList:
        orderIndex = deformer_order.index(deformer)
        if orderIndex:
            if not deformer_order[orderIndex-1] in clusterDeformerList:
                reorder_deformer = deformer_order[orderIndex-1]

    # Delete current skinCluster connections
    #     TODO: What should be done when multiple skinClusters already exist?
    #     TODO: Make a function for activating and deactiviing skinClusters
    #     1. Disconnect all the existing skinClusters and storing their
    #        connections.
    #     2. Build the new skinCluster
    #     3. Reconnect all the skinClusters in reverse order
    sc_hist_list = mc.ls(mc.listHistory(target, pdo=1, il=2),  type='skinCluster')
    sc_list = []

    for sc in sc_hist_list:
        # OUTGOING
        #
        # Get the outgoing geom connection of the skinCluster
        sc_data = [sc]
        sc_out = mc.listConnections(sc+'.outputGeometry[0]', p=1)[0]
        sc_data.append(sc_out)

        # INCOMING
        # Get the group parts node of the skinCluster (incoming connection)
        sc_gp = mc.listConnections(sc+'.input[0].inputGeometry')[0]
        sc_data.append(sc_gp)

        # Get the connection coming into the group parts node
        sc_pre_dfmr = mc.listConnections(sc_gp+'.inputGeometry', p=1)[0]
        sc_data.append(sc_pre_dfmr)
        # Remove the connection
        mc.disconnectAttr(sc_pre_dfmr, sc_gp+'.inputGeometry')

        # Store connection information
        sc_list.append(sc_data)

        # Disconnect the incoming connection
        # Bypass the skinCluster by connecting the incoming group parts connection
        # into the outgoing skinCluster destination connection
        mc.connectAttr(sc_pre_dfmr, sc_out, f=1)

    # create a base joint that we can put weights on.
    baseJnt = "root_preMatrix_jnt"
    if not mc.objExists(baseJnt):
        jnt = mc.createNode("joint",name="root_preMatrix_jnt")
        mc.setAttr("{}.v".format(jnt), 0)
        mc.parent(baseJnt,rootParentNode)

    # create a target skinCluster that will replace the wire defomer
    targetSkinCluster = mc.skinCluster(target, baseJnt, tsb=1, name=newSkinName)[0]
    # Hook up the bind preMatrix node for the root joint
    index = rigrepo.libs.skinCluster.getInfIndex(targetSkinCluster, baseJnt)
    mc.connectAttr("{}.worldInverseMatrix[0]".format(rootPreMatrixNode), "{}.bindPreMatrix[{}]".format(targetSkinCluster, index), f=True)
    mc.setAttr('{}.skinningMethod'.format(targetSkinCluster), 1)
    #mc.setAttr('{}.normalizeWeights'.format(targetSkinCluster), 0)
    
    # get the influences to be used for the target skinCluster
    preMatrixNodeList = list()
    influenceList = list()
    weightList = list()

    for clusterDeformer in convertClusterList:
        # get the curve
        handleNode = mc.listConnections('{}.matrix'.format(clusterDeformer), s=True, type='transform')[0]
        preMatrixNode = mc.listConnections('{}.bindPreMatrix'.format(clusterDeformer), s=True, type='transform')[0]
        joint = mc.createNode('joint', n=handleNode.replace('_hdl', '_bind'))
        mc.setAttr('{}.drawStyle'.format(joint), 2)
        mc.xform(joint, ws=True, matrix=mc.xform(handleNode, q=True, ws=True, matrix=True))
        mc.parent(joint, handleNode)
        influenceList.append(joint)
        preMatrixNodeList.extend(preMatrixNode)

        # Add jnt as influnce
        mc.skinCluster(targetSkinCluster, e=1, ai=joint)
        # Get index
        index = rigrepo.libs.skinCluster.getInfIndex(targetSkinCluster, joint)
        # Connect bindPreMatrixNode
        mc.connectAttr("{}.worldInverseMatrix[0]".format(preMatrixNode), "{}.bindPreMatrix[{}]".format(targetSkinCluster, index), f=True)
        weightList.append(rigrepo.libs.weights.getWeights(clusterDeformer, geometry=targetGeometry).getWeights()[0])

    # RECONNECT other skinClusters
    #
    sc_list.reverse()
    for sc_data in sc_list:
        sc, sc_out, sc_gp, sc_pre_dfmr = sc_data
        mc.connectAttr(sc_pre_dfmr, sc_gp+'.inputGeometry', f=1)
        if '.inMesh' in sc_out:
            targ_sc_gp = mc.listConnections(targetSkinCluster+'.input[0].inputGeometry')[0]
            mc.connectAttr(sc+'.outputGeometry[0]', targ_sc_gp+'.inputGeometry', f=1)
        else:
            mc.connectAttr(sc+'.outputGeometry[0]', sc_out, f=1)

    # make sure we have the correct weights for the baseJnt
    # Create a numpy array the length of the number of verts and assigning
    # a value of 1.0 to each index
    # TODO: This can be simplified to baseJntArray = numpy.ones(mc.polyEvaluate(target, v=1))
    baseJntArray = numpy.array([1.0 for id in mc.ls("{}.cp[*]".format(target), fl=True)])

    # Update the base joints weights by subtracting the curve joint weights
    for weights in weightList:
        baseJntArray = baseJntArray - weights

    # add the baseJnt weights first by itself.
    influenceList.insert(0, baseJnt)
    weightList.insert(0, baseJntArray)

    # Set all the weights on the new target skinCluster
    rigrepo.libs.weights.setWeights(targetSkinCluster, rigrepo.libs.weightObject.WeightObject(maps=influenceList, weights=weightList)) 

    if not keepClusters:
        mc.delete(clusterDeformerList)

    # Reorder deformers
    if reorder_deformer:
        mc.reorderDeformers(reorder_deformer, targetSkinCluster, target)
