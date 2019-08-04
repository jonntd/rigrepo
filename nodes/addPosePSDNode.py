import inspect
'''
This is a node for adding poses to a pose interpolator
'''

import rigrepo.nodes.commandNode as commandNode

class AddPosePSDNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, action='addPose'):
        super(AddPosePSDNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('action', action, attrType='str', index=0)
        cmd = '''
import maya.cmds as mc
import maya.mel as mm
import traceback
from rigrepo.libs import psd, blendShape, common
import math

mc.undoInfo(openChunk=1)
try:

    # ------------------------------------------------------------------------
    # Get selection
    # ------------------------------------------------------------------------
    
    # Interps
    interps = mm.eval('getPoseEditorTreeviewSelection(1)')
    
    # Poses
    poses = list()
    poseConnections = mm.eval('getPoseEditorTreeviewSelection(2)') 
    for poseConnection in poseConnections:
        interp, index = poseConnection.split('.')
        interp = psd.getPoseInterp(interp)
        if index:
            bs = psd.getDeformer(interp)
            
            pose = mc.getAttr(interp+'.pose['+str(index)+'].poseName')
            #pose = mc.listConnections(interp+'.output['+str(index)+']', p=1)
            if pose:
                poses.append((interp, pose, bs))
                
    # ------------------------------------------------------------------------
    # Add pose 
    # ------------------------------------------------------------------------
    
    if '{action}' == 'addPose':
        poseName = 'NEW_POSE'
        
        for interp in interps:
            interp = psd.getPoseInterp(interp)
            psd.addPose(interp, poseName, type='swing')
            bs = psd.getDeformer(interp)
            if not bs:
                if mc.objExists('skin_psd'):
                    bs = 'skin_psd'
                else:
                    print('could not find blendShape associated with '+interp)
                    continue
            psd.addShape(interp, poseName, bs=bs)
            
    # ------------------------------------------------------------------------
    # Update pose 
    # ------------------------------------------------------------------------
    
    if '{action}' == 'updatePose':
    
        for pose in poses:
            interp, pose, bs = pose
            
            # Update pose
            psd.updatePose(interp, pose)
            
            # Update pose control data
            #
            poseControlData = psd.getPoseControlData(interp, pose)
            if not poseControlData:
                continue
            for data in poseControlData:
                name, type, value = data
                value = mc.getAttr(name)
                
                # Rotate
                if type == 8:
                    # Convert degrees to radians
                    value = [math.radians(value[0][0]), math.radians(value[0][1]), math.radians(value[0][2])]
                    psd.setPoseControlData(interp, pose, name, type, value)
                    
    # ------------------------------------------------------------------------
    # Update pose 
    # ------------------------------------------------------------------------
                    
    if '{action}' == 'deleteDeltas':
        for pose in poses:
            interp, pose, bs = pose
            blendShape.clearTargetDeltas(bs, pose)

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
        action = self.getAttributeByName("action").getValue()
        exec(self.getAttributeByName('command').getValue().format(action=action))
