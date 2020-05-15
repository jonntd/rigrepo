import inspect
'''
This is a node for mirroring skinClusters
'''

import rigrepo.nodes.commandNode as commandNode

class MirrorPSDNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, action='system'):
        super(MirrorPSDNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('action', action, attrType='str', index=0)
        cmd = '''
import maya.cmds as mc
import maya.mel as mm
import traceback
import rigrepo.libs.data.psd_data
import rigrepo.libs.control
import rigrepo.libs.psd as psd
import rigrepo.libs.common as common
import rigrepo.libs.blendShape as blendShape
import time

start = time.time()

mc.undoInfo(openChunk=1)
try:
    # Store Global symmetry setting, something is changing this during the mirror
    globalMirrorState = mc.symmetricModelling(symmetry=1, q=1)
    
    # ------------------------------------
    # Get Selection
    # ------------------------------------
    
    # Targets and their blendshapes
    #
    if '{action}' == 'deltas':
        targetConnections = mm.eval('getPoseEditorTreeviewSelection(2)') 
        targets = list()
        blendShapes = list()
        for targ in targetConnections:
            node, index = targ.split('.')
            if index:
                bs = psd.getDeformer(node)
                target = mc.listConnections(node+'.output['+str(index)+']', p=1)
                if target:
                    target = target[0].split('.')[1]
                    targets.append(target)
                    blendShapes.append(bs) 
            
    # Interpolators
    # 
    nodes = mm.eval('getPoseEditorTreeviewSelection(1)')
    
    # ------------------------------------
    # Store pose
    # ------------------------------------
    
    #if '{action}' == 'system':
    #    controls = rigrepo.libs.control.getControls()
    #    if controls:
    #        rigrepo.libs.control.setPoseAttr(controls, 6)
    #        # Got to bind pose
    #        rigrepo.libs.control.toPoseAttr(controls, 0)
    
    # ------------------------------------
    # Main Loop
    # ------------------------------------
    
    for node in nodes:
        node = psd.getInterp(node)
        mirrorToken = common.getSideToken(node)
        if mirrorToken == 'r':
            print('mirror only works for left to right'),
            continue
        
        mirNode = common.getMirrorName(node)
        
        if not mirNode:
            print('PSD Mirror: Warning [ '+node+' ] has no mirror system')
            continue
        
        # -------------------------------
        # MIRROR SYSTEM
        # -------------------------------
        
        if '{action}' == 'system':
        
            # Remove existing pose controls before mirror. They cause mirror errors
            if mc.objExists(mirNode):
                mirPoseControls = psd.getPoseControls(mirNode)
                for poseControl in mirPoseControls:
                    psd.removePoseControl(mirNode, poseControl)
                    
            poses = common.pyListToMelArray(psd.getPoseNames(node))
            try:
                mm.eval('poseInterpolatorMirror '+node+' '+poses+' _l_ _r_ 1 1 1')
            except:
                traceback.print_exc()
            
            # Attr settings
            attrs = ['outputSmoothing', 'regularization']
            for attr in attrs:
                value = mc.getAttr(node+'.'+attr)
                mc.setAttr(mirNode+'.'+attr, value)
            
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
            
            print('Mirrored Interpolator: ' + node)
       
            
        # -------------------------------
        # MIRROR ONLY DELTAS
        # -------------------------------
        
        if '{action}' == 'deltas':
            
            bs = psd.getDeformer(node)
            mir_bs = psd.getDeformer(mirNode)
            deltas_list = list()
            
            # Get Deltas
            for pose in psd.getPoseNames(node):
                if pose not in targets:
                    continue
                index = psd.getPoseShapeIndex(node, pose)
                endGetIndex = time.time()
                mirPose = common.getMirrorName(pose)
                mir_index = psd.getPoseShapeIndex(mirNode, mirPose)
                
                if index != None and mir_index != None:
                    targetName = blendShape.getTargetName(mir_bs, mir_index)
                    deltas, indices = blendShape.getTargetDeltas(bs, index)
                    if not deltas:
                        continue
                    
                    # Center Mirror
                    if node == mirNode and index == mir_index:
                        blendShape.setTargetDeltas(mir_bs, deltas, indices, mir_index) 
                        mc.blendShape(bs, e=1, mt=(0, mir_index), ss=1, sa='x')
                        print('Mirrored deltas: ' + pose)
                    # Side Flip    
                    else:
                        blendShape.clearTargetDeltas(mir_bs, mir_index)
                        blendShape.setTargetDeltas(mir_bs, deltas, indices, mir_index) 
                        mc.blendShape(mir_bs, e=1, ft=(0, mir_index), ss=1, sa='x')
                        print('flipped deltas: ' + pose)
                    
    # restore pose
    #if '{action}' == 'system':
    #    if controls:
    #        rigrepo.libs.control.toPoseAttr(controls, 6)
            
    finish = time.time()
    total_time = str(finish-start)[0:5]
    print(total_time+' mirror total time ')

except:
    traceback.print_exc()
mc.undoInfo(closeChunk=1)

# GLOBAL MIRROR SETTINGS
#   Setting the global mirror state is going into the undo stack
#   so undoing the mirror action is turning it back on if it was changed.
#   This shuts off undo so the mirror setting doesn't get added to 
#   the undo stack.
try:
    mc.undoInfo(stateWithoutFlush=0)
    # Restore global mirror state
    mc.symmetricModelling(symmetry=globalMirrorState)
    mc.undoInfo(stateWithoutFlush=1)
except:
    mc.undoInfo(stateWithoutFlush=1)
                
'''
        # command 
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        action = self.getAttributeByName("action").getValue()
        exec(self.getAttributeByName('command').getValue().format(action=action))
