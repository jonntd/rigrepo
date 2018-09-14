import inspect
'''
This is a node for mirroring skinClusters
'''

import rigrepo.nodes.commandNode as commandNode

class MirrorSkinClusterNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(MirrorSkinClusterNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import traceback
import rigrepo.libs.control
from rigrepo.libs.common import getSideToken

mc.undoInfo(openChunk=1)
try:
    controls = rigrepo.libs.control.getControls()
    if controls:
        # Store current pose
        rigrepo.libs.control.setPoseAttr(controls, 5)
        # Got to bind pose
        rigrepo.libs.control.toPoseAttr(controls, 0)
    # Mirror
    sel = mc.ls(sl=1, dag=1, s=1, ni=1)
    if not sel:
        sel = mc.ls(hl=1, dag=1, s=1, ni=1)
    for s in sel:
        sc = mc.ls(mc.listHistory(s, pdo=1, il=1), type='skinCluster')
        if sc:
            sc = sc[0]
            mc.copySkinWeights(ss=sc, ds=sc, mirrorMode='YZ', 
                               surfaceAssociation='closestComponent', 
                               influenceAssociation=('label', 'closestJoint'))
            print("mirrored " + sc),
    if controls:
        # Restore pose
        rigrepo.libs.control.toPoseAttr(controls, 5)

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
