
'''
This is a node for exporting PSD data
'''

import rigrepo.nodes.commandNode as commandNode

class ExportPSDNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp", fileName="skin_psd.pose", nodes='mc.ls(type="poseInterpolator")'):
        super(ExportPSDNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('dirPath', dirPath, attrType='dir', index=0)
        self.addAttribute('fileName', fileName, attrType='str', index=0)
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
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath, fileName=fileName, nodes=nodes))
        

        
