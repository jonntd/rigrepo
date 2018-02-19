'''
This is a node for creating a new scene.
'''

import rigrepo.nodes.commandNode as commandNode

class NewSceneNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, *args, **kwargs):
        super(NewSceneNode, self).__init__(*args, **kwargs)
        commandAttribute = self.getAttributeByName('command')
        commandAttribute.setValue('import maya.cmds as mc\nmc.file(new=True, f=True)')