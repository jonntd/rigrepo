'''
'''
import pubs.pGraph as pGraph
import pubs.pNode as pNode
import rigrepo.nodes.NewSceneNode
import rigrepo.nodes.Node
import maya.cmds as mc
import os

class Archetype(pGraph.PGraph):
    def __init__(self,name):
        super(Base, self).__init__(name)

        self.element = self._name
        self.variant = "base"

        newSceneNode = rigrepo.nodes.newSceneNode.NewSceneNode()
        loadFileNode = rigrepo.nodes.loadFileNode.LoadFileNode()
        self.addNode(newSceneNode)
        self.addNode(newSceneNode)
