
'''
This is a node for mirroring curves
'''

import rigrepo.nodes.commandNode as commandNode
import maya.cmds as mc
class ZeroJointsNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(ZeroJointsNode, self).__init__(name, parent)
        self.addAttribute('jointList',  'mc.ls("*_bind", type="joint")', attrType='str', index=0)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import rigrepo.libs.joint
import traceback

mc.undoInfo(openChunk=1)
try:
    rigrepo.libs.joint.rotateToOrient({jointList})
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
        jointList = eval(self.getAttributeByName("jointList").getValue())
        exec(self.getAttributeByName('command').getValue().format(jointList=jointList))

