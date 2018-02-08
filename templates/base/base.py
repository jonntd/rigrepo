'''
'''
import pubs.pGraph as pGraph
import pubs.pNode as pNode
import maya.cmds as mc

class Base(pGraph.PGraph):
    def __init__(self,name):
        super(Base, self).__init__(name)

        newScene = NewScene("new scene")
        self.addNode(newScene)


class NewScene(pNode.PNode):        
    def execute(self, *args, **kwargs):
        '''
        This is just going to start a new scene.
        '''
        mc.file(new=True, f=True)