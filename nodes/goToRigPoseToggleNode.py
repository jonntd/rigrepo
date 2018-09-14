import inspect
'''
This is a node for going to the rig pose (bind pose)
'''

import rigrepo.nodes.commandNode as commandNode

class GoToRigPoseToggleNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(GoToRigPoseToggleNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        global rigPoseSetState
        rigPoseSetState = False
        cmd = '''
import maya.cmds as mc
import traceback
import rigrepo.libs.control
from rigrepo.libs.common import getSideToken
global rigPoseSetState

mc.undoInfo(openChunk=1)
try:
    controls = rigrepo.libs.control.getControls()
    if controls:
        if not rigPoseSetState:
            # Store current pose
            rigrepo.libs.control.setPoseAttr(controls, 5)
            # Got to bind pose
            rigrepo.libs.control.toPoseAttr(controls, 0)
            print("\\nGo to rig pose: [ "+str(rigPoseSetState)+" ]"),
            rigPoseSetState = True
        else:
            # Restore pose
            rigrepo.libs.control.toPoseAttr(controls, 5)
            print("\\nGo to rig pose: [ "+str(rigPoseSetState)+" ]"),
            rigPoseSetState = False

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
