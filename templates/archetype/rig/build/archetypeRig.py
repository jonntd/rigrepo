'''
'''
import pubs.pGraph
import pubs.pNode
import rigrepo.nodes.newSceneNode
import rigrepo.nodes.commandNode 
import maya.cmds as mc
import os

class ArchetypeRig(pubs.pGraph.PGraph):
    def __init__(self,name):
        super(ArchetypeRig, self).__init__(name)

        self.element = self._name
        self.variant = "base"


        animRigNode = self.addNode("animRig")

        # New Scene
        newSceneNode = rigrepo.nodes.newSceneNode.NewSceneNode('newScene')
        
        # Load
        loadNode = pubs.pNode.PNode('load')

        #perspective frame
        frameNode = rigrepo.nodes.commandNode.CommandNode('frameCamera')
        frameNode.getAttributeByName('command').setValue('import maya.cmds as mc; mc.viewFit("persp")')

        animRigNode.addChild(newSceneNode)
        animRigNode.addChild(loadNode)
        animRigNode.addChild(frameNode)

        # add the nodes to the graph
        self.addNode(animRigNode)



