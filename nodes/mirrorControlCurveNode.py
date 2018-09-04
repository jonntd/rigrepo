
'''
This is a node for mirroring curves
'''

import rigrepo.nodes.commandNode as commandNode

class MirrorControlCurveNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(MirrorControlCurveNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import rigrepo.libs.curve
import traceback
from rigrepo.libs.common import getSideToken

mc.undoInfo(openChunk=1)
try:
    controlCurves = mc.listRelatives(mc.listRelatives(mc.ls("*.__control__", o=1), s=1, ni=1, type='nurbsCurve'), p=1)
    for c in controlCurves:
        if getSideToken(c) is 'l':
            rigrepo.libs.curve.mirror(c)
except:
    mc.undoInfo(closeChunk=1)
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
        

        
