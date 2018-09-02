'''
'''
import pubs.pGraph
import pubs.pNode
import rigrepo.nodes.newSceneNode
import rigrepo.nodes.commandNode 
import rigrepo.nodes.exportDataNode
import rigrepo.nodes.exportWtsDirNode
import maya.cmds as mc
from rigrepo.libs.fileIO import joinPath 
import os
import inspect

class ArchetypeRig(pubs.pGraph.PGraph):
    def __init__(self,name, variant='base'):
        super(ArchetypeRig, self).__init__(name)

        self.element = self._name
        self.variant = variant

        buildPath = joinPath(os.path.dirname(inspect.getfile(self.__class__)), self.variant)
        animRigNode = self.addNode("animRig")

        # New Scene
        newSceneNode = rigrepo.nodes.newSceneNode.NewSceneNode('newScene')
        
        # Load
        loadNode = pubs.pNode.PNode('load')

        modelFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("model", 
            filePath=self.resolveModelFilePath('{}_{}_model.ma'.format(self.element, self.variant)))
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
        frameNode.getAttributeByName('command').setValue('import maya.cmds as mc\nmc.viewFit("persp")')

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
        exporters = pubs.pNode.PNode('exporters')
        jointExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('jointPositions', 
            dataFile= self.resolveDataFilePath('joint_positions.data', self.variant), 
            dataType='joint')
        curveExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('curvePositions', 
            dataFile=self.resolveDataFilePath('curve_positions.data', self.variant), 
            dataType='curve')
        skinClusterExportWtsNode = rigrepo.nodes.exportWtsDirNode.ExportWtsDirNode('skinCluster', 
            dirPath=self.resolveDirPath('skin_wts', self.variant))
        skinClusterExportWtsSelectedNode = rigrepo.nodes.exportWtsSelectedNode.ExportWtsSelectedNode('skinClusterSelected', 
            dirPath=self.resolveDirPath('skin_wts', self.variant))

        self.addNode(workflow)
        workflow.addChild(exporters)
        exporters.addChildren([jointExportDataNode, curveExportDataNode, skinClusterExportWtsNode, skinClusterExportWtsSelectedNode])
    
    @classmethod
    def resolveDataFilePath(cls, filename, variant):
        '''
        '''
        filepath = joinPath(os.path.dirname(inspect.getfile(cls)), variant, filename)
        if not os.path.isfile(filepath):
            filepath = ""
            try:
                return cls.__bases__[0].resolveDataFilePath(filename, variant)
            except:
                pass

        return filepath

    @classmethod
    def resolveModelFilePath(cls, filename):
        '''
        '''
        modelPath = joinPath(os.path.dirname(os.path.dirname(os.path.dirname(inspect.getfile(cls)))), 'model')
        filepath = joinPath(modelPath, filename)
        if not os.path.isfile(filepath):
            filepath = ""
            try:
                return cls.__bases__[0].resolveDataFilePath(filename)
            except:
                pass

        return filepath

    @classmethod
    def resolveDirPath(cls, dirname, variant):
        '''
        :pararm: cls: Class
        '''
        dirpath = joinPath(os.path.dirname(inspect.getfile(cls)), variant, dirname)
        if not os.path.isdir(dirpath):
            dirpath = ""
            try:
                return cls.__bases__[0].resolveDirPath(dirname, variant)
            except:
                pass

        return dirpath
