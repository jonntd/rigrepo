'''
'''
import maya.cmds as mc
import numpy
import rigrepo.libs.weights
import rigrepo.libs.shape
import rigrepo.libs.skinCluster
import rigrepo.libs.transform
import rigrepo.libs.bindmesh

def convertWiresToSkinCluster(newSkinName, targetGeometry, wireDeformerList, keepWires=False, 
    rootParentNode="rig", rootPreMatrixNode="trs_aux", jointDepth=2):
    '''
    This function will take in a wire deformer list and create a new skinCluster

    :param newSkinName: This is the name we will use for the new skinCluster we're creating.
    :type newSkinName: str

    :param targetGeometry: This is the geometry we will be putting the skinCluster onto.
    :type targetGeometry: str
    '''
    target = targetGeometry
    base = mc.duplicate(target)[0]
    # Get existing wire deformers from the wireDeformerList
    convertWireList = mc.ls(wireDeformerList, type="wire")

    # Store the connection to the shape
    geo_input = mc.listConnections(targetGeometry+'.inMesh', p=1)[0]

    # Store deformation order
    deformer_order = mc.listHistory(target, pdo=1, il=2)
    reorder_deformer = None
    for deformer in wireDeformerList:
        orderIndex = deformer_order.index(deformer)
        if orderIndex:
            if not deformer_order[orderIndex-1] in wireDeformerList:
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

    # get the influences to be used for the target skinCluster
    preMatrixNodeList = list()
    influenceList = list()
    weightList = list()
    curveList = list()

    for wireDeformer in convertWireList:
        # get the curve
        curve = mc.wire(wireDeformer, q=True, wire=True)[0]
        curveList.append(curve)
        # get the skinCluster associated with that curve
        curveSkin = mc.ls(mc.listHistory(curve, il=1, pdo=True), type="skinCluster")[0]
        # get the influences associated with the skinCluster
        curveSkinInfluenceList = mc.skinCluster(curveSkin, q=True, inf=True)
        # get the nuls to use as bindPreMatrix nodes
        curveSkinPreMatrixNodes = list()
        for jnt in curveSkinInfluenceList:
            # Travel up the ancestry of the joint, jointDepth number of times to find
            # the transform to be used for the preMatrix connection
            preMatrixNode = jnt
            for i in xrange(jointDepth):
                parent = mc.listRelatives(preMatrixNode, p=True)[0]
                if i == (jointDepth - 1):
                    curveSkinPreMatrixNodes.append(parent)
                preMatrixNode = parent

        # Compile the influences and preMatrix nodes for all curves
        influenceList.extend(curveSkinInfluenceList)
        preMatrixNodeList.extend(curveSkinPreMatrixNodes)

        # connect the influences to the matrices and the nuls as the bind preMatrix
        # YANK IT!!!!!!
        for jnt, preMatrixNode in zip(curveSkinInfluenceList, curveSkinPreMatrixNodes):
            # create a temp influence we will use to connect the curveSkin to
            tempInf = mc.duplicate(jnt, po=1)[0]
            # get the connections through the worldMatrix connection
            matrixCon = mc.listConnections(jnt+'.worldMatrix[0]', p=1, d=1, s=0)
            # Get inf index
            # TODO: This should just use
            # TODO: rigrepo.libs.skinCluster.getInfIndex(targetSkinCluster, jnt)
            infIndex = None
            for con in matrixCon:
                node = con.split('.')[0]
                if node == curveSkin:
                    infIndex = con.split('[')[1].split(']')[0]
            # Yank
            if infIndex:
                # connect the temp influence
                mc.connectAttr(tempInf+'.worldMatrix[0]', curveSkin+'.matrix[{}]'.format(infIndex), f=1)
                # move the influence
                mc.move( 1, 0, 0, tempInf, r=1, worldSpaceDistance=1) 
                # get the delta to put into weightList
                weightList.append(rigrepo.libs.shape.getDeltas(base, target))
                # recconect the joint and delete the temp influence.
                mc.connectAttr(jnt+'.worldMatrix[0]', curveSkin+'.matrix[{}]'.format(infIndex), f=1) 
                mc.delete(tempInf)

    # Add curve joints as influces to targetSkinCluster and hook up bindPreMatrix nuls
    # TODO: i var is not doing anything here
    i=0
    for jnt, preMatrixNode in zip(influenceList,preMatrixNodeList):
        # Add jnt as influnce
        mc.skinCluster(targetSkinCluster, e=1, ai=jnt)
        # Get index
        index = rigrepo.libs.skinCluster.getInfIndex(targetSkinCluster, jnt)
        # Connect bindPreMatrixNode
        mc.connectAttr("{}.worldInverseMatrix[0]".format(preMatrixNode), "{}.bindPreMatrix[{}]".format(targetSkinCluster, index), f=True)
        i += 1
        
    # connect the base joint so we have somewhere to put the weights not being used.
    # Hook up the bind preMatrix node for the root joint
    index = rigrepo.libs.skinCluster.getInfIndex(targetSkinCluster, baseJnt)
    mc.connectAttr("{}.worldInverseMatrix[0]".format(rootPreMatrixNode), "{}.bindPreMatrix[{}]".format(targetSkinCluster, index), f=True)

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

    # delete the base that we were using to compare deltas from
    mc.delete(base)

    # delete the wire deformers
    if not keepWires:

        # If the curve is being used for multiple wire deforms we need to disconnect it first
        # or maya will delete it
        delete_curves = True
        for wire in convertWireList:
            # wire
            curve = mc.listConnections(wire+'.deformedWire[0]', p=1)
            curveOutputs = mc.listConnections(curve[0])
            if len(curveOutputs) > 1:
                delete_curves = False
                mc.disconnectAttr(curve[0], wire+'.deformedWire[0]')
            # base wire
            curve = mc.listConnections(wire+'.baseWire[0]', p=1)
            curveOutputs = mc.listConnections(curve[0])
            if len(curveOutputs) > 1:
                mc.disconnectAttr(curve[0], wire+'.baseWire[0]')

        # Delete the wire and curves
        mc.delete(convertWireList)
        if delete_curves:
            mc.delete(curveList)

    # Reorder deformers
    if reorder_deformer:
        mc.reorderDeformers(reorder_deformer, targetSkinCluster, target)


def buildCurveRig(curve, name='limb_bend', ctrl_names=[], parent=None):
    '''
    This will build a rig setup based on the curve that is passed in.

    :param curve: NurbsCurve name you want to build the rig on.
    :type curve: str

    :param name: This will be used to name the control hierachy and joints in the rig.
    :type name: str

    :return: This method will return the data needed to make adjustments to rig.
    :rtype: tuple
    '''

    # If the name passed in doesn't exist, we will create a transform as the parent group
    # for the rig.
    if not mc.objExists(name):
        mc.createNode("transform", n=name)

    # create the bindmesh
    bindmeshGeometry, follicleList = rigrepo.libs.bindmesh.createFromCurve(name, curve, cv_names=ctrl_names)

    # emptry list to append controls to in the loop
    controlHieracrchyList = list()
    # Joints built for each curve cv
    jointList = list()

    # loop through and create controls on the follicles so we have controls to deform the wire.
    for follicle in follicleList:
        # get the follicle transform so we can use it to parent the control to it.
        follicleIndex = follicleList.index(follicle)

        # ctrl names: default name is used if ctrl_names list is not passed
        ctrl_name = "{}_{}".format(name, follicleIndex)
        if ctrl_names:
            ctrl_name = ctrl_names[follicleIndex]
        # create the control with a large enough hierarchy to create proper SDK's
        ctrlHierarchy = rigrepo.libs.control.create(name=ctrl_name,
                                                    controlType="circle",
                                                    hierarchy=['nul','ort','def_auto'],
                                                    parent=follicle)

        # create the joint that will drive the curve.
        jnt_name = "{}_{}_jnt".format(name, follicleIndex)
        if ctrl_names:
            jnt_name = ctrl_names[follicleIndex]+'_jnt'
        jnt = mc.joint(n=jnt_name)
        # make sure the joint is in the correct space
        mc.setAttr("{}.translate".format(jnt), 0,0,0)
        mc.setAttr("{}.rotate".format(jnt), 0,0,0)
        mc.setAttr("{}.drawStyle".format(jnt),2)
        mc.setAttr("{}.displayHandle".format(ctrlHierarchy[-1]), 1)

        # zero out the nul for the control hierarchy so it's in the correct position.
        mc.setAttr("{}.translate".format(ctrlHierarchy[0]), 0,0,0)
        # set the visibility of the shape node for the follicle to be off.
        # append the control and the follicle transform to their lists
        controlHieracrchyList.append(ctrlHierarchy)
        jointList.append(jnt)

    # This will parent all of the data for the rig to the system group "name"
    for data in (bindmeshGeometry, follicleList):
        mc.parent(data, name)

    # AIM CONSTRRAINTS
    ##
    ## This is dumb but the most consitent way for me to get the right behavior
    ## parenting the last joint to the first on to grab the axis I want to use for aiming
    #mc.parent(jointList[-1], jointList[0])
    ## get the axis we want to use to aim.
    #aimDistance = mc.getAttr("{}.t".format(jointList[-1]))[0]
    #aimAttr, aimVector = rigrepo.libs.transform.getDistanceVector(aimDistance)
    ## parent the joint back to the control
    #mc.parent(jointList[-1], controlHieracrchyList[-1][-1])
    #mc.pointConstraint(controlHieracrchyList[0][-1],controlHieracrchyList[2][-1], controlHieracrchyList[1][2], mo=True)
    #mc.aimConstraint(jointList[2], controlHieracrchyList[1][2], mo=True, w=1, upVector=(0,0,0), aimVector=aimVector, wut="none")
    #mc.aimConstraint(jointList[1], jointList[0], upVector=(0,0,0), mo=True, w=1, aimVector=aimVector, wut="none")


    ## This is dumb but the most consitent way for me to get the right behavior
    ## parenting the last joint to the first on to grab the axis I want to use for aiming
    #mc.parent(jointList[0], jointList[-1])
    #aimDistance = mc.getAttr("{}.t".format(jointList[0]))[0]
    #aimAttr, aimVector = rigrepo.libs.transform.getDistanceVector(aimDistance)
    ## parent the joint back to the control
    #mc.parent(jointList[0], controlHieracrchyList[0][-1])
    #mc.pointConstraint(controlHieracrchyList[2][-1],controlHieracrchyList[4][-1], controlHieracrchyList[3][2], mo=True)
    #mc.aimConstraint(jointList[2], controlHieracrchyList[3][2], mo=True, w=1, upVector=(0,0,0), aimVector=aimVector, wut="none")
    #mc.aimConstraint(jointList[-2], jointList[-1], upVector=(0,0,0), mo=True, w=1, aimVector=aimVector, wut="none")


    # If parent the parent is passed in we will parent the system to the parent.
    if parent:
        if not mc.objExists(parent):
            mc.warning('Created the system but the current parent "{}" does not exist in the \
                current Maya session.'.format(parent))
        else:
            mc.parent(name, parent)

    # create the skinCluster for the curve
    mc.skinCluster(*jointList + [curve], tsb=True, name="{}_skinCluster".format(curve))

    # set the visibility of the bindmesh.
    mc.setAttr("{}.v".format(bindmeshGeometry), 0 )
    mc.setAttr("{}.v".format(curve), 0 )
    return bindmeshGeometry, follicleList, controlHieracrchyList, jointList

def convertClustersToSkinCluster(newSkinName, targetGeometry, clusterList, keepWires=False,
                                 rootParentNode="rig", rootPreMatrixNode="trs_aux", jointDepth=2):
    '''
    This function will take in a cluster list and create a new skinCluster

    :param newSkinName: This is the name we will use for the new skinCluster we're creating.
    :type newSkinName: str

    :param targetGeometry: This is the geometry we will be putting the skinCluster onto.
    :type targetGeometry: str
    '''
    target = targetGeometry
    base = mc.duplicate(target)[0]
    convertWireList = mc.ls(clusterList, type="wire")

    # Delete current skinCluster connections
    sc = mc.ls(mc.listHistory(target), type='skinCluster')[0]
    if sc:
        sc_out = mc.listConnections(sc+'.outputGeometry[0]', p=1)[0]
        sc_gp = mc.listConnections(sc+'.input[0].inputGeometry')[0]
        sc_pre_dfmr = mc.listConnections(sc_gp+'.inputGeometry', p=1)[0]
        mc.connectAttr(sc_pre_dfmr, sc_out, f=1)

    # create a base joint that we can put weights on.
    baseJnt = "root_preMatrix_jnt"
    if not mc.objExists(baseJnt):
        jnt = mc.createNode("joint",name="root_preMatrix_jnt")
        mc.setAttr("{}.v".format(jnt), 0)
        mc.parent(baseJnt,rootParentNode)

    # create a target skinCluster that will replace the wire defomer
    targetSkinCluster = mc.skinCluster(target, baseJnt, tsb=1, name=newSkinName)[0]

    # get the influences to be used for the target skinCluster
    preMatrixNodeList = list()
    influenceList = list()
    weightList = list()
    curveList = list()

    for wireDeformer in convertWireList:
        # get the curve
        curve = mc.wire(wireDeformer, q=True, wire=True)[0]
        curveList.append(curve)
        # get the skinCluster associated with that curve
        curveSkin = mc.ls(mc.listHistory(curve, il=1, pdo=True), type="skinCluster")[0]
        # get the influences associated with the skinCluster
        curveSkinInfluenceList = mc.skinCluster(curveSkin, q=True, inf=True)
        # get the nuls to use as bindPreMatrix nodes
        curveSkinPreMatrixNodes = list()
        for jnt in curveSkinInfluenceList:
            preMatrixNode = jnt
            for i in xrange(jointDepth):
                parent = mc.listRelatives(preMatrixNode, p=True)[0]
                if i == (jointDepth - 1):
                    curveSkinPreMatrixNodes.append(parent)
                preMatrixNode = parent

        influenceList.extend(curveSkinInfluenceList)
        preMatrixNodeList.extend(curveSkinPreMatrixNodes)

        # connect the influences to the matrices and the nuls as the bind preMatrix
        # YANK IT!!!!!!
        for jnt, preMatrixNode in zip(curveSkinInfluenceList, curveSkinPreMatrixNodes):
            # create a temp influence we will use to connect the curveSkin to
            tempInf = mc.duplicate(jnt, po=1)[0]
            # get the connections through the worldMatrix connection
            matrixCon = mc.listConnections(jnt+'.worldMatrix[0]', p=1, d=1, s=0)
            infIndex = None
            for con in matrixCon:
                node = con.split('.')[0]
                if node == curveSkin:
                    infIndex = con.split('[')[1].split(']')[0]
            if infIndex:
                # connect the temp influence
                mc.connectAttr(tempInf+'.worldMatrix[0]', curveSkin+'.matrix[{}]'.format(infIndex), f=1)
                # move the influence
                mc.move( 1, 0, 0, tempInf, r=1, worldSpaceDistance=1)
                # get the delta to put into weightList
                weightList.append(rigrepo.libs.shape.getDeltas(base, target))
                # recconect the joint and delete the temp influence.
                mc.connectAttr(jnt+'.worldMatrix[0]', curveSkin+'.matrix[{}]'.format(infIndex), f=1)
                mc.delete(tempInf)

    # add in
    i=0
    for jnt, preMatrixNode in zip(influenceList,preMatrixNodeList):
        mc.skinCluster(targetSkinCluster, e=1, ai=jnt)
        index = rigrepo.libs.skinCluster.getInfIndex(targetSkinCluster, jnt)
        mc.connectAttr("{}.worldInverseMatrix[0]".format(preMatrixNode), "{}.bindPreMatrix[{}]".format(targetSkinCluster, index), f=True)
        i += 1

    # connect the base joint so we have somewhere to put the weights not being used.
    index = rigrepo.libs.skinCluster.getInfIndex(targetSkinCluster, baseJnt)
    mc.connectAttr("{}.worldInverseMatrix[0]".format(rootPreMatrixNode), "{}.bindPreMatrix[{}]".format(targetSkinCluster, index), f=True)

    # Rewire skinClusters
    targ_sc_gp = mc.listConnections(targetSkinCluster+'.input[0].inputGeometry')[0]
    mc.connectAttr(sc+'.outputGeometry[0]', targ_sc_gp+'.inputGeometry', f=1)

    # make sure we have the correct weights for the baseJnt
    baseJntArray = numpy.array([1.0 for id in mc.ls("{}.cp[*]".format(target), fl=True)])
    for weights in weightList:
        baseJntArray = baseJntArray - weights

    # add the baseJnt weights first by itself.
    influenceList.insert(0, baseJnt)
    weightList.insert(0, baseJntArray)
    # then add the rest of the weights
    rigrepo.libs.weights.setWeights(targetSkinCluster, rigrepo.libs.weightObject.WeightObject(maps=influenceList, weights=weightList))

    # delete the base that we were using to compare deltas from
    mc.delete(base)

    # delete the wire deformers
    if not keepWires:
        mc.delete(convertWireList+curveList)
