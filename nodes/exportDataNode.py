'''
This is the base data node 
'''
import pubs.pNode
import rigrepo.libs.data.joint_data
import maya.cmds as mc
import os


class ExportDataNode(pubs.pNode.PNode):
    def __init__(self, name, dataFile=None, dataType=None, apply=False):
        super(ExportDataNode, self).__init__(name)
        self.addAttribute('filepath', dataFile, attrType='file')
        self.addAttribute('Nodes', 'mc.ls(type="joint")', attrType='str')

        self._dataType = dataType
        if dataType == 'joint':
            self.dataObj = rigrepo.libs.data.joint_data.JointData()

    def execute(self, **kwargs):
        dataFile = self.getAttributeByName('filepath').getValue()
        nodes = eval(self.getAttributeByName('Nodes').getValue())
        if nodes: 
            self.dataObj.gatherDataIterate(nodes)
            self.dataObj.write(dataFile)
            print('Writing: {}'.format(dataFile))
        else:
            mc.warning('No nodes found to write')


