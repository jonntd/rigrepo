'''
This is a node for going to the rig pose (bind pose)
'''

import rigrepo.nodes.commandNode as commandNode

class GpuSpeedKeyNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(GpuSpeedKeyNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import traceback
import rigrepo.libs.control

mc.undoInfo(openChunk=1)
try:
    controls = rigrepo.libs.control.getControls()
    sel = mc.ls(sl=1)
    mc.select(controls)
    curTime = mc.currentTime(q=1)

    mc.currentTime(1)
    mc.setKeyframe()

    mc.currentTime(0)
    mc.rotate(0.01, 0.01, 0.01, r=1, os=1, fo=1)
    mc.move(0.01, 0.01, 0.01, r=1, os=1, wd=1)
    mc.setKeyframe()

    if sel:
        mc.select(cl=1)
        mc.select(sel)
        
    skinClusters = mc.ls(type='skinCluster')
    for sc in skinClusters:
        mc.setAttr(sc+'.deformUserNormals', )

    mc.currentTime(-10)
    mc.currentTime(curTime)

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
