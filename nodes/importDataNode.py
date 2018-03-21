'''
This is the base data node 
'''
import pubs.pNode
import rigrepo.libs.data.joint_data
import maya.cmds as mc
import os

class ImportDataNode(pubs.pNode.PNode):
    def __init__(self, name, dataFile=None, dataType=None, apply=False):
        super(ImportDataNode, self).__init__(name)
        self.addAttribute('filepath', dataFile, attrType='file')
        self.addAttribute('Apply', apply, attrType='bool')
        nodesAttr = self.addAttribute('Nodes', 'mc.ls(type="joint")', attrType='str')
        self._dataType = dataType
        if dataType == 'joint':
            self.dataObj = rigrepo.libs.data.joint_data.JointData()
        elif dataType == 'curve':
            self.dataObj = rigrepo.libs.data.curve_data.CurveData()
            nodesAttr.setValue('mc.ls("*_curve", type="transform")')

    def execute(self, **kwargs):
        dataFile = self.getAttributeByName('filepath').getValue()
        if os.path.isfile(dataFile):
            self.dataObj.read(dataFile)
        else:
            mc.warning('{} does not exist'.format(dataFile)) 
            return

        if self.getAttributeByName('Apply').getValue():
             nodes = eval(self.getAttributeByName('Nodes').getValue())
             self.dataObj.applyData(nodes)

