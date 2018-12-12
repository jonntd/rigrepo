
'''
This is a node for exporting PSD data
'''

import rigrepo.nodes.commandNode as commandNode

class ExportNodeEditorBookmarsNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp",
        fileName='node_editor_bookmarks',
        nodes='mc.ls(type="nodeGraphEditorBookmarkInfo")'):

        super(ExportNodeEditorBookmarsNode, self).__init__(name, parent)
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
    nodes = mc.ls(type="nodeGraphEditorBookmarkInfo")
        
    # write .ma file because I can't create these nodes from scratch
    #
    # Remove connections to nodes for export
    connections = list()
    renamedNodes = list()
    
    manager = mc.listConnections(nodes[0]+'.message')[0]

    for node in nodes:
        nodeInfoLength = len(mc.ls(node+'.nodeInfo[*]'))
        for i in xrange(nodeInfoLength):
            name = mc.getAttr(node+'.name')
            node = mc.rename(node, name+'_nodeview')
            renamedNodes.append(node)
            con = mc.listConnections(node+'.nodeInfo['+str(i)+'].dependNode', p=1, c=1)
            connections.append(con)
            mc.disconnectAttr(con[1], con[0])
            
    mc.select(renamedNodes, manager)
    mayaFile = '{dirPath}/{fileName}.ma'

    mc.file(mayaFile, es=1, type='mayaAscii', force=1)
            
    for con in connections:
        mc.connectAttr(con[1], con[0])
        
    dataObj = rigrepo.libs.data.node_editor_bookmark_data.NodeEditorBookmarkData()
    dataObj.gatherDataIterate(renamedNodes)
    dataFile = '{dirPath}/{fileName}.data'
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
        

        
