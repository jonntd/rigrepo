'''
'''
import pubs.pGraph
import pubs.pNode
import rigrepo.nodes.newSceneNode
import maya.cmds as mc
import os

class ArchetypeRig(pubs.pGraph.PGraph):
    def __init__(self,name):
        super(ArchetypeRig, self).__init__(name)

        self.element = self._name
        self.variant = "base"

        # New Scene
        newSceneNode = rigrepo.nodes.newSceneNode.NewSceneNode('newScene')
        # Load
        loadNode = pubs.pNode.PNode('load')

        # add the nodes to the graph
        self.addNode(newSceneNode)
        self.addNode(loadNode)

