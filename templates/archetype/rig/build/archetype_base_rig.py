'''
'''
import traceback
import pubs.pGraph
import pubs.pNode
import rigrepo.nodes.newSceneNode
import rigrepo.nodes.commandNode 
import rigrepo.nodes.exportDataNode
import rigrepo.nodes.exportWtsDirNode
import rigrepo.nodes.mirrorControlCurveNode
import rigrepo.nodes.transferDeformer
import rigrepo.nodes.mirrorWiresNode
import rigrepo.nodes.zeroJointsNode
import rigrepo.nodes.labelJointsForMirroringNode
import maya.cmds as mc
from rigrepo.libs.fileIO import joinPath 
import os
import inspect
import copy
import rigrepo.tests as tests

class ArchetypeBaseRig(pubs.pGraph.PGraph):
    def __init__(self,name, variant='base'):
        super(ArchetypeBaseRig, self).__init__(name)

        self.element = self._name
        self.variant = variant

        buildPath = joinPath(os.path.dirname(inspect.getfile(self.__class__)), self.variant)
        animRigNode = self.addNode("animRig")

        # New Scene
        newSceneNode = rigrepo.nodes.newSceneNode.NewSceneNode('newScene')
        
        # Load
        loadNode = pubs.pNode.PNode('load')

        modelFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("model", 
            filePath=self.resolveModelFilePath(self.variant))
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

        controlOrientDataNode = rigrepo.nodes.importDataNode.ImportDataNode('controlOrients', 
                dataFile=self.resolveDataFilePath('control_orients.data', self.variant), 
                dataType='node', 
                apply=True)

        controlDataNode = rigrepo.nodes.importDataNode.ImportDataNode('controlPositions', 
                dataFile=self.resolveDataFilePath('control_positions.data', self.variant), 
                dataType='curve',
                attributes="['cvPositions']",
                apply=True)

        controlOrientDataNode.getAttributeByName("Nodes").setValue("mc.ls('*_ort',type='transform')")
        controlDataNode.getAttributeByName("Nodes").setValue("rigrepo.libs.control.getControls()")

        postBuild.addChild(controlOrientDataNode)
        postBuild.addChild(controlDataNode)

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
            dirPath=self.resolveDirPath('skin_wts', self.variant))

        deltaMushWtsFileNode = rigrepo.nodes.loadWtsDirNode.LoadWtsDirNode("deltaMush", 
            dirPath=self.resolveDirPath('deltaMush_wts', self.variant))
        applyNode.addChildren([deformersNode, importDeformerDataNode, importSdkDataNode])
        deformersNode.addChildren([skinWtsFileNode, wireWtsFileNode, clusterWtsFileNode, importPSDSystemNode, deltaMushWtsFileNode])

        importNodeEditorBookmarsNode = rigrepo.nodes.importNodeEditorBookmarksNode.ImportNodeEditorBookmarksNode("bookmarks",
            dirPath=self.resolveDirPath('bookmarks', self.variant))

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
        rigrepo.libs.attribute.lock(ctrl, ['jointOrient', 'rotateAxis'])
    
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

        deliveryNode.addChildren([localizeNode, lockNode, hideHistoryNode])

        animRigNode.addChildren([newSceneNode, loadNode, postBuild, applyNode, deliveryNode, importNodeEditorBookmarsNode, frameNode])


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
            excludeNodes='mc.ls("lip*",type="cluster")')
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
        mirroring.addChildren([mirrorControlCurveNode, mirrorWireCurveNode, mirrorJointsNode, mirrorSkinClusterNode, mirrorOrients, mirrorPSDNode, mirrorSDKNode])

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
