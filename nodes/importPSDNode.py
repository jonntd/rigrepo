
'''
This is a node for importing PSD data

TODO:

'''

import rigrepo.nodes.commandNode as commandNode

class ImportPSDNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp", fileName=None, nodes='mc.ls(type="poseInterpolator")'):
        super(ImportPSDNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('dirPath', dirPath, attrType='dir', index=0)
        self.addAttribute('fileName', fileName, attrType='str', index=0)
        self.addAttribute('nodes', nodes, attrType='str', index=0)
        cmd = '''
import maya.cmds as mc
import maya.mel as mm
import rigrepo.libs.psd as psd
import rigrepo.libs.data.psd_data
import os

import traceback

mc.undoInfo(openChunk=1)
try:
    if not mc.pluginInfo('poseInterpolator', q=1, l=1):  
        mc.loadPlugin('poseInterpolator')
    
    # Re-sync procedurally built poseInterpolators 
    # Note: Not sure why this can't be done when the procedural system is built
    #       but it is not working when I do it at the same time.
    for poseInterp in {nodes}:
        poses = psd.getPoses(poseInterp)
        for pose in poses:
            psd.syncPose(poseInterp, pose)
        for pose in poses:
            psd.setPoseKernalFalloff(poseInterp, pose)
        psd.goToNeutralPose(poseInterp)
        
    file = '{dirPath}/{fileName}.pose'
    if os.path.isfile(file):
        mm.eval('poseInterpolatorImportPoses("'+file+'", 1)')
    
        # Pose Control Data
        nodes = {nodes}
        dataObj = rigrepo.libs.data.psd_data.PSDData()
        dataFile = '{dirPath}/{fileName}_poseControls.data'
        dataObj.read(dataFile)
        dataObj.applyData(nodes)
    else:
        print('Warning: PSD File does not exist [ '+file + ' ]')
    
    # Move nodes into a group
    nodes = {nodes}
    if nodes:
        group = 'psd_grp'
        if not mc.objExists(group):
            mc.group(empty=1, n=group)
        if mc.objExists('rig'):
            mc.parent(group, 'rig')
        mc.parent(nodes, group)
        if mc.objExists('numericPSD_geo'):
            mc.parent('numericPSD_geo', group)

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
        dirPath = self.getAttributeByName("dirPath").getValue()
        fileName = self.getAttributeByName("fileName").getValue()
        nodes = self.getAttributeByName("nodes").getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath, fileName=fileName, nodes=nodes))

        

        
