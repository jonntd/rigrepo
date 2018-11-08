import inspect
'''
This is a node for adding poses to a pose interpolator
'''

import rigrepo.nodes.commandNode as commandNode

class AddPosePSDNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(AddPosePSDNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import maya.mel as mm
import traceback
import rigrepo.libs.psd as psd
import rigrepo.libs.common as common

mc.undoInfo(openChunk=1)
try:
    # Get selected pose interpolator
    nodes = mm.eval('getPoseEditorTreeviewSelection(1)')
    poseName = 'NEW_POSE'
    
    for node in nodes:
        node = psd.getPoseInterp(node)
        psd.addPose(node, poseName, type='swing')
        bs = psd.getDeformer(node)
        if not bs:
            if mc.objExists('skin_psd'):
                bs = 'skin_psd'
            else:
                print('could not find blendShape associated with {}'.format(node))
                continue
        psd.addShape(node, poseName, bs=bs)

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
