'''
'''
import pubs.pGraph as pGraph
import pubs.pNode as pNode
import rigrepo.nodes.newSceneNode
import maya.cmds as mc
import os

class ArchetypeRig(pGraph.PGraph):
    def __init__(self,name):
        super(ArchetypeRig, self).__init__(name)

        self.element = self._name
        self.variant = "base"

        #newSceneNode = rigrepo.nodes.newSceneNode.NewSceneNode("NewScene")
        #self.addNode(newSceneNode)
