'''
This is the base data node 
'''
import pubs.pNode
import rigrepo.libs.data.joint_data
import maya.cmds as mc


class DataNode(pubs.pNode.PNode):
    def __init__(self, name, dataFile=None, dataType=None, apply=False):
        super(DataNode, self).__init__(name)
        self.addAttribute('filepath', dataFile, attrType='file')
        self.addAttribute('Apply', apply, attrType='bool')
        self.addAttribute('Nodes', 'mc.ls(type="joint")', attrType='str')

        self._dataType = dataType
        if dataType == 'joint':
            self.dataObj = rigrepo.libs.data.joint_data.JointData()

    def execute(self, **kwargs):
        dataFile = self.getAttributeByName('filepath').getValue()
        self.dataObj.read(dataFile)

        if self.getAttributeByName('Apply').getValue():
             nodes = eval(self.getAttributeByName('Nodes').getValue())
             self.dataObj.applyData(nodes)

