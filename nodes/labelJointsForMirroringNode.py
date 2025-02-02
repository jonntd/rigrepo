import inspect
'''
Set joint side lables so the skinCluster mirror will work correctly for 
joints that are in the same location.
'''

import rigrepo.nodes.commandNode as commandNode

class LabelJointsForMirroringNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(LabelJointsForMirroringNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import traceback
from rigrepo.libs.common import getSideToken

mc.undoInfo(openChunk=1)
try:
    nodes = mc.ls('*_bind', type='joint')
    for n in nodes:
        if getSideToken(n) is 'l':
            mc.setAttr(n+'.side', 1)
            mc.setAttr(n+'.type', 18)
            mc.setAttr(n+'.otherType', n.split('_')[0], type='string')
        if getSideToken(n) is 'r':
            mc.setAttr(n+'.side', 2)
            mc.setAttr(n+'.type', 18)
            mc.setAttr(n+'.otherType', n.split('_')[0], type='string')
               
except:
    traceback.print_exc()
mc.undoInfo(closeChunk=1)
'''
        # command 
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        exec(self.getAttributeByName('command').getValue())
