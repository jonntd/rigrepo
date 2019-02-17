import inspect
'''
This is a node for going to the rig pose (bind pose)
'''

import rigrepo.nodes.commandNode as commandNode

class GoToRigPoseNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(GoToRigPoseNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
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
        # Got to bind pose
        rigrepo.libs.control.toPoseAttr(controls, 0)

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


class GoToFreezePoseNode(GoToRigPoseNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(GoToFreezePoseNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
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
        # Got to bind pose
        rigrepo.libs.control.toPoseAttr(controls, 0)
    mc.setAttr('jaw.rx', -15)

    for deformer in mc.ls(mc.listHistory("body_geo"), type="wire"):
        mc.setAttr(deformer+".freezeGeometry", 1)

    # set poseAttr for freezing when rig is loaded.
    rigrepo.libs.control.setPoseAttr(controls, 9)
    if controls:
        # Got to bind pose
        rigrepo.libs.control.toPoseAttr(controls, 0)

    mc.setAttr('jaw.rx', 0)


except:
    mc.undoInfo(closeChunk=1)
    traceback.print_exc()
mc.undoInfo(closeChunk=1)
'''
        # command 
        commandAttribute.setValue(cmd)