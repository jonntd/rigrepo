
'''
This is a node for exporting PSD data
'''

import rigrepo.nodes.commandNode as commandNode

class ExportPSDNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp", fileName="skin_psd.pose", nodes='mc.ls(type="poseInterpolator")', nodesExclude=''):
        super(ExportPSDNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('dirPath', dirPath, attrType='dir', index=0)
        self.addAttribute('fileName', fileName, attrType='str', index=0)
        self.addAttribute('nodesExclude', nodesExclude, attrType='str', index=0)
        self.addAttribute('nodes', nodes, attrType='str', index=0)
        cmd = '''
import maya.cmds as mc
import maya.mel as mm
import rigrepo.libs.psd as psd
import rigrepo.libs.common as common
import rigrepo.libs.data.psd_data

import traceback

mc.undoInfo(openChunk=1)
try:
    if not mc.pluginInfo('poseInterpolator', q=1, l=1):  
        mc.loadPlugin('poseInterpolator')
        
    nodes = {nodes}
    nodesExclude = {nodesExclude}
    nodes = list(set(nodes)-set(nodesExclude))
    nodesMel = common.pyListToMelArray(nodes)
        
    mm.eval('poseInterpolatorExport("{dirPath}/{fileName}.pose", '+nodesMel+', 1)')
    
    dataObj = rigrepo.libs.data.psd_data.PSDData()
    dataObj.gatherDataIterate(nodes)
    dataFile = '{dirPath}/{fileName}_poseControls.data'
    dataObj.write(dataFile)
    print('Writing: ' + dataFile)

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
        nodesExclude = self.getAttributeByName("nodesExclude").getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath, fileName=fileName, nodes=nodes, nodesExclude=nodesExclude))



class ExportPSDByGroupNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp", groups='libs.psd.getAllGroups', groupsExclude=''):
        super(ExportPSDByGroupNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('dirPath', dirPath, attrType='dir', index=0)
        self.addAttribute('groupsExclude', groupsExclude, attrType='str', index=0)
        self.addAttribute('groups', groups, attrType='str', index=0)
        cmd = '''
import maya.cmds as mc
import maya.mel as mm
import rigrepo.libs.psd as psd
import rigrepo.libs.common as common
import rigrepo.libs.data.psd_data

import traceback

mc.undoInfo(openChunk=1)
try:
    if not mc.pluginInfo('poseInterpolator', q=1, l=1):  
        mc.loadPlugin('poseInterpolator')
        
    groups = {groups}
    dirPath = '{dirPath}'
    for group in groups:
        nodes = rigrepo.libs.psd.getGroupChildren(group)
        nodesMel = common.pyListToMelArray(nodes)
            
        print('poseInterpolatorExport("'+dirPath+'/'+group+'.pose", '+nodesMel+', 1)')
        mm.eval('poseInterpolatorExport("'+dirPath+'/'+group+'.pose", '+nodesMel+', 1)')
        
        dataObj = rigrepo.libs.data.psd_data.PSDData()
        dataObj.gatherDataIterate(nodes)
        dataFile = '{dirPath}/'+group+'_poseControls.data'
        dataObj.write(dataFile)
        print('Writing: ' + dataFile)

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
        groups = self.getAttributeByName("groups").getValue()
        groupsExclude = self.getAttributeByName("groupsExclude").getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath, groups=groups, groupsExclude=groupsExclude))


