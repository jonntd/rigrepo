'''
This module will rename controls based off a json mapping file if 
it exists. 

Keys are the current control name
Value are the name you wish to convert the control to.

'''
import rigrepo.nodes.commandNode as commandNode

class RenameMappingNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None, filepath=str()):
        '''
        This node is used to set the defaults. Currently it's set to use biped controls. 
        the user has the ability to make changes to it. 
        '''
        super(RenameMappingNode, self).__init__(name, parent)
        # add the attributes on the node.

        commandAttribute = self.getAttributeByName('command')

        # these are the list attributes that will be used and replaced in the command.
        self.addAttribute('filepath', filepath, attrType=str, index=0)
        commandAttribute = self.getAttributeByName('command')
        cmd='''
import os
import json
import maya.cmds as mc
filepath = "{filepath}"
if os.path.isfile(filepath):
    f = open(filepath, 'r')
    data = json.loads(f.read())
    f.close()
    for node in mc.ls(data.keys()):
        mc.rename(node, data[node])
else:
    mc.warning("{filepath} doesn't exist on disk. Please make sure you're passing in the correct filepath.")
'''
        commandAttribute.setValue(cmd)


    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        filepath = self.getAttributeByName("filepath").getValue()
        exec(self.getAttributeByName('command').getValue().format(filepath=filepath))