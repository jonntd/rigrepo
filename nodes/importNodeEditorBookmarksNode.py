
'''
This is a node for importing PSD data

TODO:

'''

import rigrepo.nodes.commandNode as commandNode

class ImportNodeEditorBookmarksNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp",
                 fileName='node_editor_bookmarks',
                 nodes='mc.ls(type="nodeGraphEditorBookmarkInfo")'):
        super(ImportNodeEditorBookmarksNode, self).__init__(name, parent)
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

fileData = '{dirPath}/{fileName}.data'
fileMaya = '{dirPath}/{fileName}.ma'

if os.path.isfile(fileData):
    print('Loading Bookmark File: [ '+fileData + ' ]')
    
    dataObj = rigrepo.libs.data.node_editor_bookmark_data.NodeEditorBookmarkData()
    
    dataObj.read(fileData)
    data = dataObj.getData()
    mc.file(fileMaya, i=1)
    dataObj.applyData(None)
    
else:
    print('Warning: Bookmark File does not exist [ '+fileData + ' ]')

'''
        # command 
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        dirPath = self.getAttributeByName("dirPath").getValue()
        nodes = self.getAttributeByName("nodes").getValue()
        fileName = self.getAttributeByName("fileName").getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath, nodes=nodes, fileName=fileName))

        

        
