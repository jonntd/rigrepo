def nodes(variant='base', buildNow=False):
    # import pubs
    import time
    import pubs.pObject
    reload(pubs.pObject)
    import pubs.pAttribute
    reload(pubs.pAttribute)
    import pubs.pNode
    reload(pubs.pNode)
    import pubs.pDict
    reload(pubs.pDict)
    import pubs.pGraph
    reload(pubs.pGraph)
    
    #import pubs UI
    import pubs.ui.fields
    reload(pubs.ui.fields)
    import pubs.ui.models
    reload(pubs.ui.models)
    import pubs.ui.widgets
    reload(pubs.ui.widgets)
    #import pubs.ui.browser
    #reload(pubs.ui.browser)
    import pubs.ui.centralWidget
    reload(pubs.ui.centralWidget)
    import pubs.ui.mainWindow
    reload(pubs.ui.mainWindow)
    
    #reload libs
    import rigrepo.libs.data.abstract_data
    reload(rigrepo.libs.data.abstract_data)
    import rigrepo.libs.data.node_data
    reload(rigrepo.libs.data.node_data)
    import rigrepo.libs.data.joint_data
    reload(rigrepo.libs.data.joint_data)
    import rigrepo.libs.data.curve_data
    reload(rigrepo.libs.data.curve_data)
    import rigrepo.libs.data.deformer_order_data
    reload(rigrepo.libs.data.deformer_order_data)

    import rigrepo.libs.data.psd_data
    reload(rigrepo.libs.data.psd_data)
    import rigrepo.libs.common
    reload(rigrepo.libs.common)
    import rigrepo.libs.transform
    reload(rigrepo.libs.transform)
    import rigrepo.libs.attribute
    reload(rigrepo.libs.attribute)
    import rigrepo.libs.ikfk
    reload(rigrepo.libs.ikfk)
    import rigrepo.libs.spline
    reload(rigrepo.libs.spline)
    import rigrepo.libs.skinCluster
    reload(rigrepo.libs.skinCluster)
    import rigrepo.libs.curve
    reload(rigrepo.libs.curve)
    import rigrepo.libs.control
    reload(rigrepo.libs.control)
    import rigrepo.libs.joint
    reload(rigrepo.libs.joint)
    import rigrepo.libs.sdk
    reload(rigrepo.libs.sdk)
    import rigrepo.libs.shape
    reload(rigrepo.libs.shape)
    import rigrepo.libs.weightObject
    reload(rigrepo.libs.weightObject)
    import rigrepo.libs.weights
    reload(rigrepo.libs.weights)
    import rigrepo.libs.psd
    reload(rigrepo.libs.psd)
    import rigrepo.libs.cluster
    reload(rigrepo.libs.cluster)
    import rigrepo.libs.bindmesh
    reload(rigrepo.libs.bindmesh)
    import rigrepo.libs.deformer
    reload(rigrepo.libs.deformer)

    import rigrepo.libs.data.sdk_data
    reload(rigrepo.libs.data.sdk_data)
    
    #reload nodes
    import rigrepo.nodes.commandNode
    reload(rigrepo.nodes.commandNode)
    import rigrepo.nodes.newSceneNode
    reload(rigrepo.nodes.newSceneNode)
    import rigrepo.nodes.loadFileNode
    reload(rigrepo.nodes.loadFileNode)
    import rigrepo.nodes.importDataNode
    reload(rigrepo.nodes.importDataNode)
    import rigrepo.nodes.exportDataNode
    reload(rigrepo.nodes.exportDataNode)
    import rigrepo.nodes.controlDefaultsNode
    reload(rigrepo.nodes.controlDefaultsNode)
    import rigrepo.nodes.loadWtsDirNode
    reload(rigrepo.nodes.loadWtsDirNode)
    import rigrepo.nodes.exportWtsDirNode
    reload(rigrepo.nodes.exportWtsDirNode)
    import rigrepo.nodes.exportWtsSelectedNode
    reload(rigrepo.nodes.exportWtsSelectedNode)
    import rigrepo.nodes.mirrorControlCurveNode
    reload(rigrepo.nodes.mirrorControlCurveNode)
    import rigrepo.nodes.modelOverrideToggleNode
    reload(rigrepo.nodes.modelOverrideToggleNode)
    import rigrepo.nodes.mirrorJointsNode
    reload(rigrepo.nodes.mirrorJointsNode)
    import rigrepo.nodes.mirrorSkinClusterNode
    reload(rigrepo.nodes.mirrorSkinClusterNode)
    import rigrepo.nodes.goToRigPoseNode
    reload(rigrepo.nodes.goToRigPoseNode)
    import rigrepo.nodes.yankSkinClusterNode
    reload(rigrepo.nodes.yankSkinClusterNode)
    import rigrepo.nodes.yankClusterNode
    reload(rigrepo.nodes.yankClusterNode)
    import rigrepo.nodes.labelJointsForMirroringNode
    reload(rigrepo.nodes.labelJointsForMirroringNode)
    import rigrepo.nodes.importPSDNode
    reload(rigrepo.nodes.importPSDNode)
    import rigrepo.nodes.exportPSDNode
    reload(rigrepo.nodes.exportPSDNode)
    import rigrepo.nodes.mirrorPSDNode
    reload(rigrepo.nodes.mirrorPSDNode)
    import rigrepo.nodes.addPosePSDNode
    reload(rigrepo.nodes.addPosePSDNode)
    import rigrepo.nodes.gpuSpeedKey
    reload(rigrepo.nodes.gpuSpeedKey)
    import rigrepo.nodes.transferDeformer
    reload(rigrepo.nodes.transferDeformer)
    import rigrepo.nodes.mirrorWiresNode
    reload(rigrepo.nodes.mirrorWiresNode)

    # reload parts
    import rigrepo.parts.part
    reload(rigrepo.parts.part)
    import rigrepo.parts.limb
    reload(rigrepo.parts.limb)
    import rigrepo.parts.arm
    reload(rigrepo.parts.arm)
    import rigrepo.parts.leg
    reload(rigrepo.parts.leg)
    import rigrepo.parts.spine
    reload(rigrepo.parts.spine)
    import rigrepo.parts.neck
    reload(rigrepo.parts.neck)
    import rigrepo.parts.blink
    reload(rigrepo.parts.blink)
    import rigrepo.parts.mouth
    reload(rigrepo.parts.mouth)
    import rigrepo.parts.face
    reload(rigrepo.parts.face)
    import rigrepo.parts.brow
    reload(rigrepo.parts.brow)
    import rigrepo.parts.hand
    reload(rigrepo.parts.hand)
    import rigrepo.parts.foot
    reload(rigrepo.parts.foot)
    import rigrepo.parts.autoParent
    reload(rigrepo.parts.autoParent)

    #reload templates
    import rigrepo.templates.archetype.rig.build.archetype_base_rig
    reload(rigrepo.templates.archetype.rig.build.archetype_base_rig)
    import rigrepo.templates.biped.rig.build.biped_base_rig
    reload(rigrepo.templates.biped.rig.build.biped_base_rig)
    import rigrepo.templates.biped.rig.build.biped_female_rig
    reload(rigrepo.templates.biped.rig.build.biped_female_rig)
    
    #regular imports
    import os
    import maya.cmds as mc

    # the right arm is all messed up and we have to fix it. Also, you can't run nodes more than once
    # in the same scene at th moment. We will have to fix this.
    if variant == 'base':
        biped_graph = rigrepo.templates.biped.rig.build.biped_base_rig.BipedBaseRig(name='Biped_base')
    elif variant == 'female':
        biped_graph = rigrepo.templates.biped.rig.build.biped_female_rig.BipedFemaleRig(name='Biped_female')

    if buildNow:
        nodeList = biped_graph.getNodes()

        for node in nodeList:
            if not node.isActive():
                nodeIndex = nodeList.index(node)
                childList = node.descendants()
                for child in childList:
                    nodeList.pop(nodeIndex+1)
                nodeList.pop(nodeIndex)
            if node.isActive():
                name = node.getName()
                print('-'*100)
                print(name + ' - executing')
                t0 = time.time()
                node.execute()
                t1 = time.time()
                print('{} - time: {} sec'.format(name, round(t1-t0, 5)))
    else:
        pubs.ui.mainWindow.launch(graph=biped_graph)
