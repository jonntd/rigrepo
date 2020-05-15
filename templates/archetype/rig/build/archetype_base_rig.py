'''
'''
import traceback
import pubs.pGraph
import pubs.pNode
import maya.cmds as mc
from rigrepo.libs.fileIO import joinPath 
import os
import inspect
import copy
import rigrepo.tests as tests

# import nodes
import rigrepo.nodes.newSceneNode
import rigrepo.nodes.commandNode 
import rigrepo.nodes.exportDataNode
import rigrepo.nodes.exportWtsDirNode
import rigrepo.nodes.mirrorControlCurveNode
import rigrepo.nodes.transferDeformer
import rigrepo.nodes.mirrorWiresNode
import rigrepo.nodes.zeroJointsNode
import rigrepo.nodes.labelJointsForMirroringNode
import rigrepo.nodes.loadFileNode
import rigrepo.nodes.mirrorDeformerNode
import rigrepo.nodes.importPSDNode
import rigrepo.nodes.loadWtsDirNode
import rigrepo.nodes.importNodeEditorBookmarksNode
import rigrepo.nodes.modelOverrideToggleNode
import rigrepo.nodes.goToRigPoseNode
import rigrepo.nodes.gpuSpeedKey
import rigrepo.nodes.shapeAuthoringNode
import rigrepo.nodes.updateTopologyNode
import rigrepo.nodes.importAnimationNode
import rigrepo.nodes.zeroJointsNode
import rigrepo.nodes.addPosePSDNode
import rigrepo.nodes.mirrorPSDNode
import rigrepo.nodes.yankSkinClusterNode
import rigrepo.nodes.mirrorSkinClusterNode
import rigrepo.nodes.mirrorJointsNode
import rigrepo.nodes.exportWtsSelectedNode
import rigrepo.nodes.exportPSDNode
import rigrepo.nodes.exportNodeEditorBookmarksNode


class ArchetypeBaseRig(pubs.pGraph.PGraph):
    def __init__(self,name, element='archetype', variant='base'):
        super(ArchetypeBaseRig, self).__init__(name)

        self.element = element
        self.variant = variant

        buildPath = joinPath(os.path.dirname(inspect.getfile(self.__class__)), self.variant)
        animRigNode = self.addNode("animRig")

        # New Scene
        newSceneNode = rigrepo.nodes.newSceneNode.NewSceneNode('newScene')

        # Rig Sets
        rigSetsNode = rigrepo.nodes.commandNode.CommandNode('rigSets')
        cmd = """
import maya.cmds as mc
mc.sets(empty=1, n='RigSets')
        """
        rigSetsNode.getAttributeByName('command').setValue(cmd)

        # Load
        loadNode = pubs.pNode.PNode('load')

        # Load Model
        modelFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("model", 
            filePath=self.resolveModelFilePath(self.variant))
        # Add model geo to RigSets
        modelFileCMD = modelFileNode.getAttributeByName('command').getValue()
        cmd = '''
if mc.objExists('RigSets') & mc.objExists('model'):
    mc.sets('model', add='RigSets')
        '''
        modelFileNode.getAttributeByName('command').setValue(modelFileCMD+cmd)

        skeletonFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("skeleton",
                filePath=self.resolveDataFilePath('skeleton.ma', self.variant))
        jointDataNode = rigrepo.nodes.importDataNode.ImportDataNode('jointPositions', 
                dataFile=self.resolveDataFilePath('joint_positions.data', self.variant), 
                dataType='joint', 
                apply=True)
        labelJointsForMirroringNode = rigrepo.nodes.labelJointsForMirroringNode.LabelJointsForMirroringNode('labelJointsForMirroring')

        jointDataNode.addChild(labelJointsForMirroringNode)

        # Curve
        curveFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("curves",
                                                                filePath=self.resolveDataFilePath('curves.ma', self.variant))
        curveDataNode = rigrepo.nodes.importDataNode.ImportDataNode('curvePosition',
                                                                    dataFile=self.resolveDataFilePath('curve_positions.data', self.variant),
                                                                    dataType='curve',
                                                                    apply=True)

        # Bind meshes
        bindMeshes = pubs.pNode.PNode('bindMeshes')

        importPSDDeltaNode = rigrepo.nodes.importPSDNode.ImportPSDDirNode("psdDeltas",
                                  dirPath=self.resolveDirPath('psd', self.variant),
                                  loadDeltas=True,
                                  psdNames='["blinks", "skin"]')
        loadNode.addChildren([modelFileNode, skeletonFileNode, jointDataNode, curveFileNode, curveDataNode, bindMeshes, importPSDDeltaNode])

        # postBuild
        postBuild = pubs.pNode.PNode("postBuild")

        # Create curve for the trs_shot
        trsCurve = rigrepo.nodes.commandNode.CommandNode('trsCurve')
        trsCurveCMD = """
import maya.cmds as mc
import rigrepo.libs.control  
if mc.objExists('trs_shot'):
    rigrepo.libs.control.create(name='trs_shot', controlType='circle', hierarchy=None)
        """
        trsCurve.getAttributeByName('command').setValue(trsCurveCMD)

        controlOrientDataNode = rigrepo.nodes.importDataNode.ImportDataNode('controlOrients', 
                dataFile=self.resolveDataFilePath('control_orients.data', self.variant), 
                dataType='node', 
                apply=True)

        controlDataNode = rigrepo.nodes.importDataNode.ImportDataNode('controlPositions', 
                dataFile=self.resolveDataFilePath('control_positions.data', self.variant), 
                dataType='curve',
                attributes="['cvPositions', 'rotateOrder', 'color']",
                apply=True)

        controlOrientDataNode.getAttributeByName("Nodes").setValue("mc.ls('*_ort',type='transform')")
        controlDataNode.getAttributeByName("Nodes").setValue("rigrepo.libs.control.getControls()")

        tagControllersNode= rigrepo.nodes.commandNode.CommandNode('tagControllers')
        tagControllersCmd = '''
import maya.cmds as mc
import maya.mel as mm

import rigrepo.libs.control

controls = rigrepo.libs.control.getControls()

mc.select(controls)
mm.eval('TagAsController')

# --------------------------------------------------
# Pickwalking
# --------------------------------------------------

# Face upper children - note: excluding 'eyeSocket_l', 'eyeSocket_r' because it is making the lide tweakers not go all the way around
children = ['face_lower', 'head_tip',  'cheek_r', 'cheek_l', 'nose_bridge']
parent = 'head'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Lid Tweakers

children = [u'lid_up_3_l', u'lid_up_4_l', u'lid_up_5_l', u'lid_corner_outer_l', u'lid_low_6_l', u'lid_low_5_l', u'lid_low_4_l', u'lid_low_3_l', u'lid_low_2_l', u'lid_corner_inner_l', u'lid_up_1_l', u'lid_up_2_l']
parent = 'lidLower_l'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

children = [u'lid_up_3_r', u'lid_up_2_r', u'lid_up_1_r', u'lid_corner_inner_r', u'lid_low_2_r', u'lid_low_3_r', u'lid_low_4_r', u'lid_low_5_r', u'lid_low_6_r', u'lid_corner_outer_r', u'lid_up_5_r', u'lid_up_4_r']
parent = 'lidLower_r'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Upper lids
children = ['lidLower_l']
parent = 'lidUpper_l'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

children = ['lidLower_r']
parent = 'lidUpper_r'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Lower lids
children = ['lidUpper_l']
parent = 'eyeSocket_l'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

children = ['lidUpper_r']
parent = 'eyeSocket_r'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Brows

children = [u'brow_peak_r', u'brow_main_r', u'brow_corrugator_r', u'brow_inner_r', u'brow_inner_l', u'brow_corrugator_l', 'brow_main_l', u'brow_peak_l']
parent = 'head_tip'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# lip tweakers
children = [u'lip_center_up', u'lip_up_2_l', u'lip_up_1_l', u'lip_up_0_l', u'lip_corner_l', u'lip_low_0_l', u'lip_low_1_l', u'lip_low_2_l', u'lip_center_low', u'lip_low_2_r', u'lip_low_1_r', u'lip_low_0_r', u'lip_corner_r', u'lip_up_0_r', u'lip_up_1_r', u'lip_up_2_r']
parent = 'lip_lower'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Lip lower
children = ['lip_lower']
parent = 'lip_upper'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Lip upper and mouth corners
children = ['mouth_corner_r', 'mouth_corner_l']
parent = 'mouthMain'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Mouth main and tongue base - 'lip_upper' removed 
children = ['mouthMain', 'tongue_base', 'teeth_upper']
parent = 'jaw'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Tongue mid
children = ['tongue_mid']
parent = 'tongue_base'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Tongue tip
children = ['tongue_tip']
parent = 'tongue_mid'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Lower teeth
children = ['teeth_lower']
parent = 'teeth_upper'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Nose and sneers
children = ['sneer_r', 'sneer_l', 'nose', ]
parent = 'nose_bridge'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Cheek puff
children = ['cheekPuff_l']
parent = 'cheek_l'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

children = ['cheekPuff_r']
parent = 'cheek_r'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Head wire mid
children = ['headwire_mid']
parent = 'headwire_top'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# Head wire low
children = ['headwire_low']
parent = 'headwire_mid'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# jaw
children = ['jaw']
parent = 'face_lower'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

# face upper and head wire top
children = ['headwire_top', 'face_upper']
parent = 'head'
if mc.objExists(parent):
    mc.select(mc.ls(children), parent)
    mm.eval('TagAsControllerParent')

pickwalk = [

# Hands
[u'thumbCup_l',   u'thumb_001_l',  u'thumb_002_l',  u'thumb_003_l'],
[u'index_001_l',  u'index_002_l',  u'index_003_l',  u'index_004_l'],
[u'middle_001_l', u'middle_002_l', u'middle_003_l', u'middle_004_l'],
[u'ring_001_l',   u'ring_002_l',   u'ring_003_l',   u'ring_004_l'],
[u'pinky_001_l',  u'pinky_002_l',  u'pinky_003_l', u'pinky_004_l'],
['wrist_fk_gimbal_l', ['thumbCup_l', 'index_001_l', 'middle_001_l', 'ring_001_l', 'pinky_001_l']],

[u'thumbCup_r',   u'thumb_001_r',  u'thumb_002_r',  u'thumb_003_r'],
[u'index_001_r',  u'index_002_r',  u'index_003_r',  u'index_004_r'],
[u'middle_001_r', u'middle_002_r', u'middle_003_r', u'middle_004_r'],
[u'ring_001_r',   u'ring_002_r',   u'ring_003_r',   u'ring_004_r'],
[u'pinky_001_r',  u'pinky_002_r',  u'pinky_003_r', u'pinky_004_r'],
['wrist_fk_gimbal_r', ['thumbCup_r', 'index_001_r', 'middle_001_r', 'ring_001_r', 'pinky_001_r']],

# Arms
[u'clavicle_l', u'shoulderSwing_l', u'shoulder_fk_l', u'elbow_fk_l', u'wrist_fk_l', u'wrist_fk_gimbal_l'],
[u'clavicle_r', u'shoulderSwing_r', u'shoulder_fk_r', u'elbow_fk_r', u'wrist_fk_r', u'wrist_fk_gimbal_r'],

# Arm Bend bows
[u'arm_bend_0_l', u'arm_bend_1_l', u'arm_bend_2_l', u'arm_bend_3_l', u'arm_bend_4_l'],
[u'arm_bend_0_r', u'arm_bend_1_r', u'arm_bend_2_r', u'arm_bend_3_r', u'arm_bend_4_r'],

# Legs
[ u'thighSwing_l', u'leg_pv_l', u'leg_ik_l', u'leg_ik_gimbal_l', u'heel_l', u'ballRoll_l', u'ball_l_fk', u'toe_l'],
[ u'thighSwing_r', u'leg_pv_r', u'leg_ik_r', u'leg_ik_gimbal_r', u'heel_r', u'ballRoll_r', u'ball_r_fk', u'toe_r'],

# Leg bendbows
[u'leg_bend_0_l', u'leg_bend_1_l', u'leg_bend_2_l', u'leg_bend_3_l', u'leg_bend_4_l'],
[u'leg_bend_0_r', u'leg_bend_1_r', u'leg_bend_2_r', u'leg_bend_3_r', u'leg_bend_4_r'],

# Spine
[u'head', u'neck', u'chest_top', u'chest', u'torso', u'hip_swivel', u'hips'],

# Clavs to chest
['chest', ['clavicle_r', 'clavicle_l']],

# pelvis to hips
['hips', ['thighSwing_r', 'thighSwing_l']],

]

for data in pickwalk:
    if not isinstance(data[0], str): 
        for i in range(len(data)):
            if i < len(data)-1:
                parent = data[i]
                child = data[i+1]  
                if mc.objExists(parent):
                    mc.select(mc.ls(children), parent)
                    mm.eval('TagAsControllerParent')
    else:
        parent = data[0]
        children = data[1]
        if mc.objExists(parent):
            mc.select(mc.ls(children), parent)
            mm.eval('TagAsControllerParent')
        
'''
        tagControllersNode.getAttributeByName('command').setValue(tagControllersCmd)
        postBuild.addChild(trsCurve)
        postBuild.addChild(controlOrientDataNode)
        postBuild.addChild(controlDataNode)
        postBuild.addChild(tagControllersNode)

        #perspective frame
        frameNode = rigrepo.nodes.commandNode.CommandNode('frameCamera')
        frameNode.getAttributeByName('command').setValue('import maya.cmds as mc\nmc.select(cl=1)\nmc.viewFit("persp")')

        # apply data
        applyNode = pubs.pNode.PNode("apply")
        deformersNode = pubs.pNode.PNode("deformers")

        # apply
        skinWtsFileNode = rigrepo.nodes.loadWtsDirNode.LoadWtsDirNode("skinCluster", 
            dirPath=self.resolveDirPath('skin_wts', self.variant))
        wireWtsFileNode = rigrepo.nodes.loadWtsDirNode.LoadWtsDirNode("wire", 
            dirPath=self.resolveDirPath('wire_wts', self.variant))
        clusterWtsFileNode = rigrepo.nodes.loadWtsDirNode.LoadWtsDirNode("cluster", 
            dirPath=self.resolveDirPath('cluster_wts', self.variant))
        importPSDSystemNode = rigrepo.nodes.importPSDNode.ImportPSDDirNode("psd",
            dirPath=self.resolveDirPath('psd', self.variant),
            psdNames='["blinks", "skin"]')
        importSdkDataNode = rigrepo.nodes.importDataNode.ImportDataNode('sdk', 
                dataFile=self.resolveDataFilePath('sdk.data', self.variant), 
                dataType='sdk', 
                apply=True)
        importDeformerDataNode = rigrepo.nodes.importDataNode.ImportDataNode('deformerOrder', 
                dataFile=self.resolveDataFilePath('deformer_order.data', self.variant), 
                dataType='deformerOrder', 
                apply=True)

        skinWtsFileNode = rigrepo.nodes.loadWtsDirNode.LoadWtsDirNode("skinCluster", 
            dirPath=self.resolveDirPath('skin_wts', self.variant), excludeFilter='_bindmesh')

        bindmeshWtsFileNode = rigrepo.nodes.loadWtsDirNode.LoadWtsDirNode("bindmeshLoad",
                                                                      dirPath=self.resolveDirPath('skin_wts', self.variant), includeFilter='_bindmesh')

        deltaMushWtsFileNode = rigrepo.nodes.loadWtsDirNode.LoadWtsDirNode("deltaMush", 
            dirPath=self.resolveDirPath('deltaMush_wts', self.variant))
        applyNode.addChildren([deformersNode, importDeformerDataNode, importSdkDataNode])
        deformersNode.addChildren([skinWtsFileNode, wireWtsFileNode, clusterWtsFileNode, importPSDSystemNode, deltaMushWtsFileNode, bindmeshWtsFileNode])

        importNodeEditorBookmarsNode = rigrepo.nodes.importNodeEditorBookmarksNode.ImportNodeEditorBookmarksNode("bookmarks",
            dirPath=self.resolveDirPath('bookmarks', self.variant))
        importNodeEditorBookmarsNode.disable()

        # this will make sure that if the skinCluster is DQ it will support nonRigidScale
        setDqScaleNode = rigrepo.nodes.commandNode.CommandNode('NonRigidScale')
        setDqScaleNodeCmd = '''
import maya.cmds as mc        
for skinCluster in mc.ls(type="skinCluster"):
    mc.setAttr("%s.dqsSupportNonRigid" % skinCluster, 1)
'''
        setDqScaleNode.getAttributeByName("command").setValue(setDqScaleNodeCmd)
        skinWtsFileNode.addChild(setDqScaleNode)

        # --------------------------------------------------------------------------------------------------------------
        # Delivery
        # --------------------------------------------------------------------------------------------------------------
        deliveryNode = pubs.pNode.PNode("delivery")
        deliveryNode.disable()

        localizeNode = rigrepo.nodes.commandNode.CommandNode('localize')
        localizeNodeCmd = '''
import rigrepo.libs.skinCluster
import rigrepo.libs.cluster
import maya.cmds as mc

rigrepo.libs.skinCluster.localize(mc.ls(type="skinCluster"), "model")

# localize lid blink clusters
# This is hard coded, may want to take a look at this later.
lidClusters = mc.ls("lid*blink*cluster")
for cluster in lidClusters:
    clusterName = cluster.split("__")[-1]
    rigrepo.libs.cluster.localize(cluster, "{}_auto".format(clusterName), "model")
'''
        localizeNode.getAttributeByName('command').setValue(localizeNodeCmd)

        lockNode = rigrepo.nodes.commandNode.CommandNode('lockNodes')
        lockNodeCmd = '''
import rigrepo.libs.control
import rigrepo.libs.attribute
import maya.cmds as mc

# we shouldn't be locking translates of joints effected by ikHandles
ikJointList = list()
for hdl in mc.ls(type="ikHandle"):
    ikJointList.extend(mc.ikHandle(hdl, q=True, jl=True))
    
controls = rigrepo.libs.control.getControls()
lockNodes = set(mc.ls(type="transform")).difference(controls + [mc.listRelatives(shape, p=True)[0] for shape in mc.ls(type="camera")] + ikJointList)
for node in lockNodes:
    rigrepo.libs.attribute.lock(node, ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz','t','r','s'])
    
for ctrl in controls:
    if mc.objExists(ctrl+'.jointOrient'):
        rigrepo.libs.attribute.lock(ctrl, ['jointOrient', 'rotateAxis', 'radius'])

for ctrl in mc.ls("mouth_corner_?"):
    rigrepo.libs.attribute.lockAndHide(ctrl, ['r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz'])

for ctrl in mc.ls(("trs_master", "trs_shot", "trs_aux")):
    rigrepo.libs.attribute.lockAndHide(ctrl, ['v'])

rigrepo.libs.attribute.lockAndHide(mc.listRelatives("trs_master", p=True), ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz','t','r','s','v'])
'''
        lockNode.getAttributeByName('command').setValue(lockNodeCmd)        

        hideHistoryNode = rigrepo.nodes.commandNode.CommandNode('hideHistory')
        hideHistoryNodeCmd = '''
import maya.cmds as mc    
excludeType = ("skinCluster","wire", "blendShape", "deltaMush", "cluster", "mesh", "nurbsCurve", "nurbsSurface")
exclude = []
for node in mc.ls("*"):
    if node not in exclude:
        mc.setAttr(node + '.isHistoricallyInteresting', 0)
        if mc.objectType(node) in excludeType:
            mc.setAttr(node + '.isHistoricallyInteresting', 1)
'''
        hideHistoryNode.getAttributeByName('command').setValue(hideHistoryNodeCmd)    

        removeNodesNode = rigrepo.nodes.commandNode.CommandNode('removeNodes')
        removeNodesNodeCmd = '''
import maya.cmds as mc    
removeNodes = mc.ls(("poseFreeze", "lip_up_*cluster", "lip_low_*cluster", "lip_corner_*cluster", "lip_center_*cluster", "?_leg_*wire", "?_arm_*wire","brow*wire", "brow*curve"))

mc.delete(removeNodes)       
'''

        modelOverrideNode = rigrepo.nodes.commandNode.CommandNode('modelOverride')
        modelOverrideCmd = '''
import maya.cmds as mc
mc.setAttr("{0}.overrideModel".format('model'), 1)
        '''
        modelOverrideNode.getAttributeByName('command').setValue(modelOverrideCmd)

        removeNodesNode.getAttributeByName('command').setValue(removeNodesNodeCmd)

        deliveryNode.addChildren([removeNodesNode, localizeNode, lockNode, hideHistoryNode, modelOverrideNode])

        animRigNode.addChildren([newSceneNode, rigSetsNode, loadNode, postBuild, applyNode, deliveryNode, importNodeEditorBookmarsNode, frameNode])


        # --------------------------------------------------------------------------------------------------------------
        # Workflow
        # --------------------------------------------------------------------------------------------------------------
        workflowNode = pubs.pNode.PNode('workflow')
        workflowNode.disable()
        self.addNode(workflowNode)
        
        # --------------------------------------------------------------------------------------------------------------
        # Workflow nodes Un-categorized
        # --------------------------------------------------------------------------------------------------------------

        # Model toggle
        modelToggleNode = rigrepo.nodes.modelOverrideToggleNode.ModelOverrideToggleNode('modelOverride')
        # Rig Pose
        goToRigPoseNode = rigrepo.nodes.goToRigPoseNode.GoToRigPoseNode('goToRigPose')
        workflowNode.addChildren([modelToggleNode, goToRigPoseNode])
        # Gpu Speed Key
        gpuSpeedKey = rigrepo.nodes.gpuSpeedKey.GpuSpeedKeyNode('addGpuKeyframes')
        workflowNode.addChildren([modelToggleNode, goToRigPoseNode, gpuSpeedKey])

        # Shape Authoring
        sculptingNode = pubs.pNode.PNode('sculpting')
        workflowNode.addChildren([sculptingNode])

        duplicateSubdivideNode = rigrepo.nodes.shapeAuthoringNode.ShapeAuthoringNode('subdivide', action='duplicate')
        duplicateSubdivideToggleNode = rigrepo.nodes.shapeAuthoringNode.ShapeAuthoringNode('subdivideToggle', action='toggle')
        duplicateSubdivideCommitNode = rigrepo.nodes.shapeAuthoringNode.ShapeAuthoringNode('subdivideCommit', action='commit')
        extractFacesNode = rigrepo.nodes.shapeAuthoringNode.ShapeAuthoringNode('extractFaces', action='extract')
        extractFacesCommitNode = rigrepo.nodes.shapeAuthoringNode.ShapeAuthoringNode('extractFacesCommit', action='extractCommit')
        sculptingNode.addChildren([duplicateSubdivideNode, duplicateSubdivideToggleNode, duplicateSubdivideCommitNode,
                                   extractFacesNode, extractFacesCommitNode])

        # Update Topology
        updateTopologyNode = pubs.pNode.PNode('updateTopology')
        workflowNode.addChildren([updateTopologyNode])

        updateTopologyRenameNode = rigrepo.nodes.updateTopologyNode.UpdateTopologyNode('renameOld', action='rename')
        updateTopologyImportModelNode = rigrepo.nodes.loadFileNode.LoadFileNode("importModel",
                                                                filePath=self.resolveModelFilePath(self.variant))
        updateTopologyDeformersNode= pubs.pNode.PNode('transferDeformers')
        updateTopologySkinClusterNode = rigrepo.nodes.updateTopologyNode.UpdateTopologyNode('skinCluster', action='skinCluster')
        updateTopologyClusterNode = rigrepo.nodes.updateTopologyNode.UpdateTopologyNode('cluster', action='cluster')
        updateTopologyBlendShapeNode = rigrepo.nodes.updateTopologyNode.UpdateTopologyNode('blendShape', action='blendShape')
        updateTopologyDeformersNode.addChildren([updateTopologyBlendShapeNode,
                                                 updateTopologySkinClusterNode,
                                                 updateTopologyClusterNode, ])
        updateTopologyReplaceNode = rigrepo.nodes.updateTopologyNode.UpdateTopologyNode('replace', action='replace')

        updateTopologyNode.addChildren([updateTopologyRenameNode,
                                        updateTopologyImportModelNode,
                                        updateTopologyDeformersNode,
                                        updateTopologyReplaceNode])
        # --------------------------------------------------------------------------------------------------------------
        # Workflow nodes grouped by action
        # --------------------------------------------------------------------------------------------------------------

        # EXPORTERS #
        exporters = pubs.pNode.PNode('exporters')
        # --------------------------------------------------------------------------------------------------------------
        jointExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('jointPositions',
            dataFile= self.buildExportPath('joint_positions.data', self.variant), 
            dataType='joint')
        controlOrientsExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('controlOrients', 
            dataFile= self.buildExportPath('control_orients.data', self.variant), 
            dataType='node')
        controlOrientsExportDataNode.getAttributeByName("Nodes").setValue('mc.ls("*_ort", type="transform")')
        curveExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('curvePositions', 
            dataFile=self.buildExportPath('curve_positions.data', self.variant), 
            dataType='curve')
        controlCurveExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('controlCurvePositions', 
            dataFile=self.buildExportPath('control_positions.data', self.variant), 
            dataType='controlCurve')
        sdkExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('sdk', 
            dataFile=self.buildExportPath('sdk.data', self.variant), 
            dataType='sdk')
        deformerOrderExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('deformerOrder', 
            dataFile=self.buildExportPath('deformer_order.data', self.variant), 
            dataType='deformerOrder')
        skinClusterExportWtsNode = rigrepo.nodes.exportWtsDirNode.ExportSkinWtsDirNode('skinCluster', 
            dirPath=self.buildExportPath('skin_wts', self.variant))
        wireExportWtsNode = rigrepo.nodes.exportWtsDirNode.ExportWtsDirNode('wire',
            dirPath=self.buildExportPath('wire_wts', self.variant), 
            deformerType="wire")
        clusterExportWtsNode = rigrepo.nodes.exportWtsDirNode.ExportWtsDirNode('cluster',
            dirPath=self.buildExportPath('cluster_wts', self.variant), 
            deformerType="cluster", 
            excludeNodes='mc.ls(["lip_*_?_?_*", "lip_corner_?_cluster", "lip_center_*_cluster", "lip*bindmesh*"],type="cluster")')
        skinClusterExportWtsSelectedNode = rigrepo.nodes.exportWtsSelectedNode.ExportWtsSelectedNode(
            'skinClusterSelected', dirPath=self.buildExportPath('skin_wts', self.variant))
        #exportPSDNode = rigrepo.nodes.exportPSDNode.ExportPSDNode('psd',
        #                                                          dirPath=self.buildExportPath('psd', self.variant),
        #                                                          nodesExclude="['clavicle_l_auto_poseInterpolatorShape','clavicle_r_auto_poseInterpolatorShape']",
        #                                                          fileName='skin_psd')
        exportPSDByGroupsNode = rigrepo.nodes.exportPSDNode.ExportPSDByGroupNode('psd',
                                                                  dirPath=self.buildExportPath('psd', self.variant),
                                                                  groups='rigrepo.libs.psd.getAllGroups()')
        nodeEditorBookmarks = rigrepo.nodes.exportNodeEditorBookmarksNode.ExportNodeEditorBookmarsNode('NodeEditorBookmarks',
                                                                  dirPath=self.buildExportPath('bookmarks', self.variant))
        nodeEditorBookmarks.disable()
        # --------------------------------------------------------------------------------------------------------------
        exporters.addChildren([controlOrientsExportDataNode, jointExportDataNode, 
                                curveExportDataNode, controlCurveExportDataNode, sdkExportDataNode,
                                skinClusterExportWtsNode, skinClusterExportWtsSelectedNode, 
                                wireExportWtsNode, clusterExportWtsNode, exportPSDByGroupsNode,
                                deformerOrderExportDataNode, nodeEditorBookmarks])
                                

        # Mirroring #
        mirroring = pubs.pNode.PNode('mirror')
        # --------------------------------------------------------------------------------------------------------------
        mirrorControlCurveNode = rigrepo.nodes.mirrorControlCurveNode.MirrorControlCurveNode('controlCurves')
        mirrorWireCurveNode = rigrepo.nodes.mirrorWiresNode.MirrorWiresNode('wireCurves')
        mirrorJointsNode = rigrepo.nodes.mirrorJointsNode.MirrorJointsNode('joints')
        mirrorSkinClusterNode = rigrepo.nodes.mirrorSkinClusterNode.MirrorSkinClusterNode('skinClusterSelected')
        mirrorWireDeformerNode = rigrepo.nodes.mirrorDeformerNode.MirrorDeformerNode('wireDeformer', deformerType='wire')
        mirrorClusterNode = rigrepo.nodes.mirrorDeformerNode.MirrorDeformerNode('clusters', deformerType='cluster')
        #mirrorBlendShapeNode = rigrepo.nodes.mirrorDeformerNode.MirrorDeformerNode('blendShapes', deformerType='blendShape')
        mirrorPSDNode = rigrepo.nodes.mirrorPSDNode.MirrorPSDNode('psdSystems', action='system')
        mirrorOrients = rigrepo.nodes.commandNode.CommandNode('orients')
        mirrorOrientsCmd = '''
import maya.cmds as mc
import rigrepo.libs.transform
rigrepo.libs.transform.mirror (mc.ls(["lip*_l_ort"], type="transform"), search='_l_', replace='_r_', axis="x")
'''
        mirrorOrients.getAttributeByName('command').setValue(mirrorOrientsCmd)
        mirrorSDKNode = rigrepo.nodes.commandNode.CommandNode('sdk')
        mirrorSDKCmd = '''
import maya.cmds as mc
import rigrepo.libs.data.sdk_data as sdk_data
currentData = sdk_data.SdkData()
currentData.gatherDataIterate(mc.ls("*_l_def_auto*", type=["animCurveUU", "animCurveUA", "animCurveUL", "animCurveUT"]))
data = currentData.getData()
for k in data.keys():
    data[k.replace('_l_','_r_')] = data[k]

currentData.applyData(data.keys())
'''
        mirrorSDKNode.getAttributeByName('command').setValue(mirrorSDKCmd)
        #mirrorOrients = rigrepo.nodes.mirrorPSDNode.MirrorPSDNode('psd')
        # --------------------------------------------------------------------------------------------------------------
        mirroring.addChildren([mirrorControlCurveNode,
                               mirrorWireCurveNode,
                               mirrorJointsNode,
                               mirrorSkinClusterNode,
                               mirrorWireDeformerNode,
                               mirrorClusterNode,
                               mirrorOrients,
                               mirrorPSDNode,
                               mirrorSDKNode])

        # --------------------------------------------------------------------------------------------------------------
        # Workflow nodes grouped by type
        # --------------------------------------------------------------------------------------------------------------

        # SkinCluster #
        skinClusterNode = pubs.pNode.PNode('skinCluster')
        # --------------------------------------------------------------------------------------------------------------
        yankSkinClusterNode = rigrepo.nodes.yankSkinClusterNode.YankSkinClusterNode('yank')
        sc_mirrorSkinClusterNode = rigrepo.nodes.mirrorSkinClusterNode.MirrorSkinClusterNode('mirror')
        sc_transferSkinClusterNode = rigrepo.nodes.transferDeformer.TransferDeformer('transfer', 
                                                                source="body_geo",
                                                                target=["gum_upper_geo"],
                                                                deformerTypes = ["skinCluster"],
                                                                surfaceAssociation="closestPoint")
        sc_skinClusterExportWtsNode = copy.deepcopy(skinClusterExportWtsNode)
        sc_skinClusterExportWtsNode.setNiceName('export')
        sc_skinClusterExportSelectedWtsNode = copy.deepcopy(skinClusterExportWtsSelectedNode)
        sc_skinClusterExportSelectedWtsNode.setNiceName('exportSel')

        sc_removeLocalizeNode = rigrepo.nodes.commandNode.CommandNode('removeLocalize')
        sc_removeLocalizeCmd = '''
import rigrepo.libs.skinCluster
import rigrepo.libs.cluster
import maya.cmds as mc

rigrepo.libs.skinCluster.removeLocalize(mc.ls(type="skinCluster"))
'''

        sc_removeLocalizeNode.getAttributeByName('command').setValue(sc_removeLocalizeCmd)

        # --------------------------------------------------------------------------------------------------------------
        skinClusterNode.addChildren([yankSkinClusterNode, sc_mirrorSkinClusterNode, sc_skinClusterExportWtsNode,
                                     sc_skinClusterExportSelectedWtsNode, sc_transferSkinClusterNode, sc_removeLocalizeNode])

        # SDK #
        sdkNode = pubs.pNode.PNode('SDK')
        # --------------------------------------------------------------------------------------------------------------
        sdk_selectNode = rigrepo.nodes.commandNode.CommandNode('selectSDKs')
        sdk_selectCmd = '''
import maya.cmds as mc
mc.select(mc.ls("*_def_auto*", type=["animCurveUU", "animCurveUA", "animCurveUL", "animCurveUT"]))
        '''
        sdk_selectNode.getAttributeByName('command').setValue(sdk_selectCmd)
        sdk_mirrorNode =  rigrepo.nodes.commandNode.CommandNode('mirror')
        sdk_mirrorNode.getAttributeByName('command').setValue(mirrorSDKCmd)
        sdk_exportNode = copy.deepcopy(sdkExportDataNode)
        sdk_exportNode.setNiceName('export')
        # --------------------------------------------------------------------------------------------------------------
        sdkNode.addChildren([sdk_selectNode, sdk_mirrorNode, sdk_exportNode])

        # --------------------------------------------------------------------------------------------------------------
        # PSD
        # --------------------------------------------------------------------------------------------------------------
        psdNode = pubs.pNode.PNode('psd')

        # --------------------------------------------------------------------------------------------------------------
        addPosePSDNode = rigrepo.nodes.addPosePSDNode.AddPosePSDNode('addPose')
        addUpdatePSDNode = rigrepo.nodes.addPosePSDNode.AddPosePSDNode('updatePose', action='updatePose')
        psd_mirrorPSDNodes = rigrepo.nodes.mirrorPSDNode.MirrorPSDNode('mirrorSystem', action='system')
        psd_mirrorPSDDeltaNode = rigrepo.nodes.mirrorPSDNode.MirrorPSDNode('mirrorDeltas', action='deltas')
        psd_deletePSDDeltaNode = rigrepo.nodes.addPosePSDNode.AddPosePSDNode('deleteDeltas', action='deleteDeltas')
        psd_exportPSDNode = copy.deepcopy(exportPSDByGroupsNode)
        psd_exportPSDNode.setNiceName('export')
        # --------------------------------------------------------------------------------------------------------------
        psdNode.addChildren([addPosePSDNode,
                             addUpdatePSDNode,
                             psd_mirrorPSDNodes,
                             psd_mirrorPSDDeltaNode,
                             psd_deletePSDDeltaNode,
                             psd_exportPSDNode])

        # joints
        jointsNode = pubs.pNode.PNode('joints')
        zeroJointsNode = rigrepo.nodes.zeroJointsNode.ZeroJointsNode('zeroJoints')
        jnt_mirrorJointsNode = copy.deepcopy(mirrorJointsNode)
        jnt_mirrorJointsNode.setNiceName('mirror')
        jnt_jointExportDataNode = copy.deepcopy(jointExportDataNode)
        jnt_jointExportDataNode.setNiceName('export')
        jointsNode.addChildren([zeroJointsNode, jnt_mirrorJointsNode, jnt_jointExportDataNode])

        # anim
        testPath = os.path.dirname(tests.__file__).replace("\\", "/")
        animNode = pubs.pNode.PNode('anim')

        # Clear anim
        clearAnimNode = rigrepo.nodes.commandNode.CommandNode('clearAnimation')
        clearAnimNodeCMd = '''
import maya.cmds as mc
import rigrepo.libs.control

controls = rigrepo.libs.control.getControls()
mc.cutKey(controls)
        '''
        clearAnimNode.getAttributeByName('command').setValue(clearAnimNodeCMd)
        animNode.addChildren([clearAnimNode])

        # Anim Tests
        animTestsNode = pubs.pNode.PNode('tests')
        animNode.addChildren([animTestsNode])

        # Dance Flip
        animTestDanceFlip2Node = rigrepo.nodes.importAnimationNode.ImportAnimationNode('danceFlip',
                    filePath=self.resolveDataFilePath('anim/dance_flip_2.atom', self.variant),
                    remapFile=self.resolveDataFilePath('control.map', self.variant))
        animTestsNode.addChildren([animTestDanceFlip2Node])

        # Body Cali
        animTestBodyCaliNode = rigrepo.nodes.importAnimationNode.ImportAnimationNode('bodyCali',
                    filePath=self.resolveDataFilePath('anim/body_calisthenics_2.atom', self.variant),
                    remapFile=self.resolveDataFilePath('control.map', self.variant))
        animTestsNode.addChildren([animTestBodyCaliNode])

        # add all of the nodes in order to the workflow node.
        workflowNode.addChildren([exporters, mirroring, skinClusterNode, psdNode, sdkNode, jointsNode, animNode])

    @classmethod
    def resolveDataFilePath(cls, filename, variant):
        '''
        This will search for a given directory using the variant you pass. It will recursively
        go through all inherited classes until it finds a directory.

        .. example::
            ArchetypeBaseRig.resolveDataFilePath('control_positions.data', 'base')

        :param dirname: Name of the directory you're looking for.
        :type dirname: str

        :param variant: Name of the the variant you wish to search for.
        type variant: str
        '''
        filepath = joinPath(os.path.dirname(inspect.getfile(cls)), variant, filename)
        if not os.path.isfile(filepath):
            filepath = ""
            try:
                variant = cls.__bases__[0].__module__.split('.')[-1].split('_')[1]
                return cls.__bases__[0].resolveDataFilePath(filename, variant)
            except:
                pass

        return filepath

    @classmethod
    def resolveModelFilePath(cls, variant):
        '''
        This recursively searches for a model filepath given a proper folder structure and filename

        .. note:: 
            file names should be save in the model directory as follows: 
                "elementName_variant_model.ma"

        . example::
            ArchetypeBaseRig.resolveModelFilePath('base')

        :param variant: Name of the the variant you wish to search for.
        type variant: str
        '''
        elementDir = os.path.dirname(os.path.dirname(os.path.dirname(inspect.getfile(cls))))
        element = os.path.basename(elementDir)
        modelPath = joinPath(elementDir, 'model')
        filepath = joinPath(modelPath, '{}_{}_model.ma'.format(element, variant))

        if not os.path.isfile(filepath):
            filepath = ""
            try:
                variant = cls.__bases__[0].__module__.split('.')[-1].split('_')[1]
                print variant
                return cls.__bases__[0].resolveModelFilePath(variant)
            except:
                traceback.print_exc()

        return filepath

    @classmethod
    def resolveDirPath(cls, dirname, variant):
        '''
        This will search for a given directory using the variant you pass. It will recursively
        go through all inherited classes until it finds a directory.

        .. example::
            ArchetypeBaseRig.resolveDirPath('skind_wts', 'base')

        :param dirname: Name of the directory you're looking for.
        :type dirname: str

        :param variant: Name of the the variant you wish to search for.
        type variant: str
        '''
        dirpath = joinPath(os.path.dirname(inspect.getfile(cls)), variant, dirname)
        if not os.path.isdir(dirpath):
            dirpath = ""
            try:
                variant = cls.__bases__[0].__module__.split('.')[-1].split('_')[1]
                return cls.__bases__[0].resolveDirPath(dirname, variant)
            except:
                pass

        return dirpath

    @classmethod
    def buildExportPath(cls, dirname, variant):
        '''
        This will search for a given directory using the variant you pass. 

        .. example::
            ArchetypeBaseRig.buildExportPath('skind_wts', 'base')

        :param dirname: Name of the directory you're looking for.
        :type dirname: str

        :param variant: Name of the the variant you wish to search for.
        type variant: str
        '''
        dirpath = joinPath(os.path.dirname(inspect.getfile(cls)), variant, dirname)
        return dirpath
