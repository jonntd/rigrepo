
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
error()

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
    
filePose = '{dirPath}/{fileName}.pose'
fileShape = '{dirPath}/{fileName}.{fileName}.shp'
if os.path.isfile(filePose):
    print('Loading PSD File: [ '+filePose + ' ]')
    # Import shapes
    mc.blendShape(ip=fileShape,  name={fileName}, frontOfChain=1, suppressDialog=1)
    
    # Import pose interpolators - Selection must be cleared for this command to work
    mc.select(cl=1)
    mc.poseInterpolator(im=filePose)

    # Import pose control data
    nodes = {nodes}
    dataObj = rigrepo.libs.data.psd_data.PSDData()
    dataFile = '{dirPath}/{fileName}_poseControls.data'
    dataObj.read(dataFile)
    dataObj.applyData(nodes)
else:
    print('Warning: PSD File does not exist [ '+filePose + ' ]')

# Move nodes into a group
nodes = {nodes}
if nodes:
    group = 'psd_grp'
    if not mc.objExists(group):
        mc.group(empty=1, n=group)
    if mc.objExists('rig'):
        mc.parent(group, 'rig')
    nodes = mc.listRelatives(nodes, p=1)
    mc.parent(nodes, group)
    if mc.objExists('numericPSD_geo'):
        mc.parent('numericPSD_geo', group)
    
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


class ImportPSDDirNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp", psdNames="[]", nodes='mc.ls(type="poseInterpolator")', loadDeltas=False):
        super(ImportPSDDirNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('dirPath', dirPath, attrType='dir', index=0)
        self.addAttribute('psdNames', psdNames, attrType='str', index=0)
        self.addAttribute('nodes', nodes, attrType='str', index=0)
        self.addAttribute('loadDeltas', loadDeltas, attrType='bool')
        cmd = '''
import maya.cmds as mc
import maya.mel as mm
import rigrepo.libs.psd as psd
import rigrepo.libs.data.psd_data
import os

if not mc.pluginInfo('poseInterpolator', q=1, l=1):  
    mc.loadPlugin('poseInterpolator')


for name in {psdNames}:    
    filePose = '{dirPath}/%s.pose' % name
    fileShapeList = [shapeFile for shapeFile in os.listdir('{dirPath}') if ".shp" in shapeFile and name in shapeFile]
    if os.path.isfile(filePose):
        print('Loading PSD File: [ '+filePose + ' ]')
        # DELTAS
        #
        if loadDeltas:
            # Import shapes
            for fileShape in fileShapeList:
                fileName = fileShape.split(".")[1]
                
                #mc.blendShape(fileName, e=1, ip=os.path.join('{dirPath}',fileShape),  name=fileName, frontOfChain=0, suppressDialog=1)
                mc.blendShape(ip=os.path.join('{dirPath}',fileShape),  name=fileName, frontOfChain=0, suppressDialog=1)
        
        # INTERPOLATORS
        #
        else:
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
            
            # Import pose interpolators - Selection must be cleared for this command to work
            mc.select(cl=1)
            mc.poseInterpolator(im=filePose)

            # Import pose control data
            nodes = {nodes}
            dataObj = rigrepo.libs.data.psd_data.PSDData()
            dataFile = '{dirPath}/%s_poseControls.data' % name
            dataObj.read(dataFile)
            dataObj.applyData(nodes)
            
    else:
        print('Warning: PSD File does not exist [ '+filePose + ' ]')

# Move nodes into a group
nodes = {nodes}
if nodes:
    group = 'psd_grp'
    if not mc.objExists(group):
        mc.group(empty=1, n=group)
    if mc.objExists('rig'):
        mc.parent(group, 'rig')
    nodes = mc.listRelatives(nodes, p=1)
    mc.parent(nodes, group)
    if mc.objExists('numericPSD_geo'):
        mc.parent('numericPSD_geo', group)
'''
        # command 
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        dirPath = self.getAttributeByName("dirPath").getValue()
        psdNames = eval(self.getAttributeByName("psdNames").getValue())
        nodes = self.getAttributeByName("nodes").getValue()
        loadDeltas = self.getAttributeByName('loadDeltas').getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath, psdNames=psdNames, nodes=nodes, loadDeltas=loadDeltas))

