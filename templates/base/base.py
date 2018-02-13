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

class LoadFile(pNode.PNode):
    def __init__(self, *args, **kwargs):
        '''
        This is the constructor for the loaf file class. Here we will add an attribute
        that we can access later in the execute  and we be available to the interface.
        '''
        super(LoadFile, self).__init__(*args, **kwargs)
        self.addAttribute('filepath', "/disk1/temp", attrType='file')

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        filepath = self.getAttributeByName("filepath").getValue()
        if os.path.isfile(filepath):
            mc.file(filepath, i=True, f=True)
