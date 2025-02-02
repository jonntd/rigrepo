import inspect
'''
This is a node for mirroring joints
'''

import rigrepo.nodes.commandNode as commandNode

class MirrorJointsNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(MirrorJointsNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import rigrepo.libs.joint
from rigrepo.libs.common import getSideToken
import traceback

mc.undoInfo(openChunk=1)
try:
    nodes = mc.ls('*_bind', type='joint')
    for n in nodes:
        if getSideToken(n) is 'l':
            path = mc.ls(n, l=1)[0]
            if '|skull_bind|' in path:
                rigrepo.libs.joint.mirror(n, mode='translate')
            else:
                rigrepo.libs.joint.mirror(n, mode='rotate')

    # Freeze rotations
    mc.makeIdentity(nodes, apply=1, t=0, r=1, s=0, pn=1)
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
