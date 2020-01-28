'''
This is a node for mirroring deformers (wires, clusters, blendshapes...)
SkinCluster and PSD have their own mirror nodes
'''

import rigrepo.nodes.commandNode as commandNode

class MirrorDeformerNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, deformerType=''):
        super(MirrorDeformerNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('deformerType', deformerType, attrType='str')
        cmd = '''
import maya.cmds as mc
import traceback
import rigrepo.libs.control
import rigrepo.libs.common 
import rigrepo.libs.skinCluster
import rigrepo.libs.cluster

mc.undoInfo(openChunk=1)
try:
    deformerType = '{deformerType}'
    
    # Go to bind pose
    #
    controls = rigrepo.libs.control.getControls()
    if controls:
        # Store current pose
        rigrepo.libs.control.setPoseAttr(controls, 5)
        # Got to bind pose
        rigrepo.libs.control.toPoseAttr(controls, 0)
        
    # Get Selection or highlighted
    #
    sel = mc.ls(sl=1, dag=1, s=1, ni=1)
    if not sel:
        sel = mc.ls(hl=1, dag=1, s=1, ni=1)
        
    # Mirror
    #
    mirrorInfo = ''
    for shape in sel:
        deformers = mc.ls(mc.listHistory(shape, pdo=1, il=1), type=deformerType)
        for deformer in deformers:
            sideToken = rigrepo.libs.common.getSideToken(deformer)
            # Center mirror (Same deformer)
            #
            if sideToken == None:
                mc.copyDeformerWeights(sourceDeformer=deformer,
                                       destinationDeformer=deformer,
                                       sourceShape=shape,
                                       destinationShape=shape,
                                       surfaceAssociation='closestComponent',
                                       mirrorMode='YZ')
                mirrorInfo += '\\nMirrored: ' + deformer
            # Side mirror  (Left/Right deformer)
            #
            if sideToken == 'l':
                deformerMirror = rigrepo.libs.common.getMirrorName(deformer)
                if deformer != deformerMirror:
                    mc.copyDeformerWeights(sourceDeformer=deformer,
                                           destinationDeformer=deformerMirror,
                                           sourceShape=shape,
                                           destinationShape=shape,
                                           surfaceAssociation='closestComponent',
                                           mirrorMode='YZ')
                mirrorInfo += '\\nMirrored: ' + deformer
    if mirrorInfo:
        print(mirrorInfo)
            
    # Restore pose
    #
    if controls:
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
        deformerType = self.getAttributeByName('deformerType').getValue()
        exec(self.getAttributeByName('command').getValue().format(deformerType=deformerType))
