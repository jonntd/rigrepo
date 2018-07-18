def nodes():
    # import pubs
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
    import rigrepo.libs.shape
    reload(rigrepo.libs.shape)
    
    
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
    import rigrepo.parts.hand
    reload(rigrepo.parts.hand)
    import rigrepo.parts.foot
    reload(rigrepo.parts.foot)
    
    #reload templates
    import rigrepo.templates.archetype.rig.build.archetypeRig
    reload(rigrepo.templates.archetype.rig.build.archetypeRig)
    import rigrepo.templates.biped.rig.build.bipedRig
    reload(rigrepo.templates.biped.rig.build.bipedRig)
    
    #regular imports
    import os
    import maya.cmds as mc
    
    
    # the right arm is all messed up and we have to fix it. Also, you can't run nodes more than once
    # in the same scene at th moment. We will have to fix this.
    biped_graph = rigrepo.templates.biped.rig.build.bipedRig.BipedRig('biped')
    pubs.ui.mainWindow.launch(graph=biped_graph)
    
