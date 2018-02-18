
'''
This is a node for creating a new scene.
'''

import rigrepo.nodes.commandNode as commandNode

class LoadFileNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, *args, **kwargs):
        super(LoadFileNode, self).__init__(*args, **kwargs)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('filepath', "/disk1/temp", attrType='file')
        commandAttribute.setValue('import maya.cmds as mc; import os;\\nif os.path.isfile("{filepath}"):mc.file("{filepath}", i=True, f=True);')

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        filepath = self.getAttributeByName("filepath").getValue()
        exec(self.getAttributeByName('command').getValue().format(filepath=filepath))
        
