
'''
This is a node toggling the model override of the model group
'''

import rigrepo.nodes.commandNode as commandNode

class ModelOverrideToggleNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(ModelOverrideToggleNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import traceback

model = 'model'
if mc.objExists(model):
    state = mc.getAttr(model+'.overrideModel')
    mc.setAttr(model+'.overrideModel', not(state))
    print(not(state)),
'''
        # command 
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        exec(self.getAttributeByName('command').getValue())
        

        
