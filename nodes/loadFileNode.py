
'''
This is a node for creating a new scene.
'''

import rigrepo.nodes.commandNode as commandNode

class LoadFileNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None, filePath="/disk1/temp"):
        super(LoadFileNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('filepath', filePath, attrType='file', index=0)
        cmd='''
import maya.cmds as mc
import os
if os.path.isfile("{filepath}"):
    mc.file("{filepath}", i=True, f=True)
 '''
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        filepath = self.getAttributeByName("filepath").getValue()
        exec(self.getAttributeByName('command').getValue().format(filepath=filepath))
        
