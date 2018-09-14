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
import maya.cmds as mc
from rigrepo.libs.fileIO import joinPath 
import os
import inspect

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

        loadNode.addChildren([modelFileNode, skeletonFileNode, jointDataNode])

        # postBuild
        postBuild = pubs.pNode.PNode("postBuild")

        controlDataNode = rigrepo.nodes.importDataNode.ImportDataNode('controlPositions', 
                dataFile=self.resolveDataFilePath('control_positions.data', self.variant), 
                dataType='curve', 
                apply=True)

        controlDataNode.getAttributeByName("Nodes").setValue("rigrepo.libs.control.getControls()")

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
        #skinWtsFileNode.disable()
        applyNode.addChild(deformersNode)
        deformersNode.addChildren([skinWtsFileNode])

        animRigNode.addChildren([newSceneNode, loadNode, postBuild, applyNode, frameNode])

        # Workflow
        workflow = pubs.pNode.PNode('workflow')
        workflow.disable()
        self.addNode(workflow)
        # Model toggle
        modelToggleNode = rigrepo.nodes.modelOverrideToggleNode.ModelOverrideToggleNode('modelOverrideToggle')
        goToRigPoseToggleNode = rigrepo.nodes.goToRigPoseToggleNode.GoToRigPoseToggleNode('goToRigPoseToggle')
        workflow.addChildren([modelToggleNode, goToRigPoseToggleNode])
        # Exporters
        exporters = pubs.pNode.PNode('exporters')
        jointExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('jointPositions', 
            dataFile= self.buildExportPath('joint_positions.data', self.variant), 
            dataType='joint')
        curveExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('curvePositions', 
            dataFile=self.buildExportPath('curve_positions.data', self.variant), 
            dataType='curve')
        controlCurveExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('controlCurvePositions', 
            dataFile=self.buildExportPath('control_positions.data', self.variant), 
            dataType='controlCurve')
        skinClusterExportWtsNode = rigrepo.nodes.exportWtsDirNode.ExportWtsDirNode('skinCluster', 
            dirPath=self.buildExportPath('skin_wts', self.variant))
        skinClusterExportWtsSelectedNode = rigrepo.nodes.exportWtsSelectedNode.ExportWtsSelectedNode('skinClusterSelected', 
            dirPath=self.buildExportPath('skin_wts', self.variant))

        workflow.addChild(exporters)
        exporters.addChildren([jointExportDataNode, curveExportDataNode, controlCurveExportDataNode,
                               skinClusterExportWtsNode, skinClusterExportWtsSelectedNode])

        # Mirroring
        mirroring = pubs.pNode.PNode('mirror')
        workflow.addChild(mirroring)
        mirrorControlCurveNode = rigrepo.nodes.mirrorControlCurveNode.MirrorControlCurveNode('controlCurves')
        mirrorJointsNode = rigrepo.nodes.mirrorJointsNode.MirrorJointsNode('joints')
        mirrorSkinClusterNode = rigrepo.nodes.mirrorSkinClusterNode.MirrorSkinClusterNode('skinClusterSelected')

        mirroring.addChildren([mirrorControlCurveNode, mirrorJointsNode, mirrorSkinClusterNode])
    
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
