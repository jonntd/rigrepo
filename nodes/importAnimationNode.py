'''
This is a node for importing animation
'''

import rigrepo.nodes.commandNode as commandNode

class ImportAnimationNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None, filePath='temp', remapFile=""):
        super(ImportAnimationNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('remapFile', remapFile, attrType='file', index=0)
        self.addAttribute('filePath', filePath, attrType='file', index=0)
        cmd='''
import maya.cmds as mc
import os
import traceback
import maya.mel as mm

mc.undoInfo(openChunk=1)
try:
    #if os.path.isfile("{filePath}"):
    #    mc.file("{filePath}", i=True, f=True)

    if not mc.pluginInfo('atomImportExport', q=1, l=1):  
        mc.loadPlugin('atomImportExport')

    filePath = "{filePath}"
    mm.eval("select -r ac_cn_baseParent ac_cn_base ac_rt_toe ac_rt_leg_settings ac_rt_footIK ac_rt_footIK_gimbal ac_rt_legPole ac_lf_toe ac_lf_leg_settings ac_lf_footIK ac_lf_footIK_gimbal ac_rt_pinky0 ac_rt_pinky1 ac_rt_pinky2 ac_rt_pinky3 ac_lf_legPole ac_rt_thumbCup ac_rt_thumb1 ac_rt_thumb2 ac_rt_thumb3 ac_rt_index0 ac_rt_index1 ac_rt_index2 ac_rt_index3 ac_rt_middle0 ac_rt_middle1 ac_rt_middle2 ac_rt_middle3 ac_rt_ring0 ac_rt_ring1 ac_rt_ring2 ac_rt_ring3 ac_rt_arm_settings ac_lf_thumbCup ac_lf_thumb1 ac_lf_thumb2 ac_lf_thumb3 ac_lf_pinky0 ac_lf_index0 ac_lf_index1 ac_lf_index2 ac_lf_index3 ac_lf_pinky1 ac_lf_pinky2 ac_lf_pinky3 ac_lf_middle0 ac_lf_middle1 ac_lf_middle2 ac_lf_middle3 ac_lf_ring0 ac_lf_ring1 ac_lf_ring2 ac_lf_ring3 ac_lf_arm_settings ac_cn_neck ac_cn_head ac_cn_head_gimbal ac_rt_shoulder ac_lf_armFK ac_lf_armFK_gimbal ac_cn_root ac_cn_root_gimbal ac_cn_torso ac_cn_topChest ac_rt_armFK ac_rt_armFK_gimbal ac_rt_elbowFK ac_rt_handFK ac_rt_handFK_gimbal ac_lf_elbowFK ac_lf_handFK ac_lf_handFK_gimbal ac_lf_shoulder ac_cn_chest ac_lf_hipFK ac_cn_hips ac_rt_hipFK ; ")
    mm.eval("file -import -type \\"atomImport\\" -ra true -namespace \\"body_calisthenics_1\\" -options \\";;targetTime=1;srcTime=1:400;dstTime=1:400;option=scaleInsert;match=hierarchy;;selected=;search=;replace=;prefix=;suffix=;mapFile={remapFile};\\" \\""+filePath+"\\";")
    #mm.eval("file -import -type \\"atomImport\\" -ra true -namespace \\"body_calisthenics_1\\" -options \\";;targetTime=1;srcTime=0.8:194.4;dstTime=0.8:194.4;option=scaleInsert;match=hierarchy;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile=;\\" \\""+filePath+"\\";")
        
except:
    traceback.print_exc()
mc.undoInfo(closeChunk=1)

 '''
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        filePath = self.getAttributeByName("filePath").getValue()
        remapFile = self.getAttributeByName("remapFile").getValue()
        exec(self.getAttributeByName('command').getValue().format(remapFile=remapFile, filePath=filePath))
        
