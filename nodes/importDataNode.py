'''
This is the base data node 
'''
import pubs.pNode
import rigrepo.libs.data.joint_data
import maya.cmds as mc


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
            nodesAttr.setValue('mc.ls(type="nurbsCurve")')

    def execute(self, **kwargs):
        dataFile = self.getAttributeByName('filepath').getValue()
        self.dataObj.read(dataFile)

        if self.getAttributeByName('Apply').getValue():
             nodes = eval(self.getAttributeByName('Nodes').getValue())
             print nodes
             print self.dataObj
             self.dataObj.applyData(nodes)

