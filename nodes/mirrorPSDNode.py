import inspect
'''
This is a node for mirroring skinClusters
'''

import rigrepo.nodes.commandNode as commandNode

class MirrorPSDNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(MirrorPSDNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import maya.mel as mm
import traceback
import rigrepo.libs.data.psd_data
import rigrepo.libs.control
import rigrepo.libs.psd as psd
import rigrepo.libs.common as common

mc.undoInfo(openChunk=1)
try:
    nodes = mm.eval('getPoseEditorTreeviewSelection(1)')
    controls = rigrepo.libs.control.getControls()
    if controls:
        rigrepo.libs.control.setPoseAttr(controls, 6)
        # Got to bind pose
        rigrepo.libs.control.toPoseAttr(controls, 0)
    
    for node in nodes:
        node = psd.getPoseInterp(node)
        mirrorToken = common.getSideToken(node)
        if mirrorToken == 'r':
            print('mirror only works for left to right'),
            continue
        
        mirNode = common.getMirrorName(node)

        # Remove existing pose controls before mirror. They cause mirror errors
        if mc.objExists(mirNode):
            mirPoseControls = psd.getPoseControls(mirNode)
            for poseControl in mirPoseControls:
                psd.removePoseControl(mirNode, poseControl)
                
        poses = common.pyListToMelArray(psd.getPoses(node))
        try:
            mm.eval('poseInterpolatorMirror {} {} _l_ _r_ 1 1 1'.format(node, poses))
        except:
            traceback.print_exc()
        
        # Attr settings
        attrs = ['outputSmoothing', 'regularization']
        for attr in attrs:
            value = mc.getAttr(node+'.'+attr)
            mc.setAttr(mirNode+'.'+attr, value)
        
        # Mirror deltas 
        bs = psd.getDeformer(mirNode)
        for pose in psd.getPoses(mirNode):
            index = psd.getPoseShapeIndex(mirNode, pose)
            print('index', index)
            #if index:
            #    mc.blendShape(bs, e=1, ft=(0, index), ss=1, sa='x')

        poseControls = psd.getPoseControls(node)
        
        interpolation = mc.getAttr(node+'.interpolation')
        mc.setAttr(mirNode+'.interpolation', interpolation)

        for pc in poseControls:
            con = mc.listConnections(pc, p=1)
            for c in con:
                conNode = c.split('.')[0]
                if conNode == node:
                    mirPoseControl = common.getMirrorName(pc)
                    if not mirPoseControl in psd.getPoseControls(mirNode):
                        if mc.objExists(mirPoseControl):
                            psd.addPoseControl(mirNode, mirPoseControl)          

        dataObj = rigrepo.libs.data.psd_data.PSDData()
        dataObj.gatherDataIterate(nodes)
        dataObj.applyData(nodes, mirror=True)
        
        print('*'*100)
        print('mirrored ' + node)
        
    # restore pose
    if controls:
        rigrepo.libs.control.toPoseAttr(controls, 6)

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
