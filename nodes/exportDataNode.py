'''
This is the base data node 
'''
import pubs.pNode
import rigrepo.libs.data.joint_data
import maya.cmds as mc
import os


class ExportDataNode(pubs.pNode.PNode):
    def __init__(self, name, dataFile=None, dataType=None):
        super(ExportDataNode, self).__init__(name)
        self.addAttribute('filepath', dataFile, attrType='file')
        nodesAttr = self.addAttribute('Nodes', 'mc.ls(type="joint")', attrType='str')

        self._dataType = dataType
        if dataType == 'joint':
            self.dataObj = rigrepo.libs.data.joint_data.JointData()
        elif dataType == 'curve':
            self.dataObj = rigrepo.libs.data.curve_data.CurveData()
            nodesAttr.setValue('mc.ls(type="nurbsCurve")')
        elif dataType == 'controlCurve':
            self.dataObj = rigrepo.libs.data.curve_data.CurveData()

            nodesAttr.setValue('mc.listRelatives(mc.listRelatives(mc.ls("*.__control__", o=1), s=1, ni=1, type="nurbsCurve"), p=1)')

    def execute(self, **kwargs):
        dataFile = self.getAttributeByName('filepath').getValue()
        nodes = eval(self.getAttributeByName('Nodes').getValue())
        if nodes: 
            self.dataObj.gatherDataIterate(nodes)
            self.dataObj.write(dataFile)
            print('Writing: {}'.format(dataFile))
        else:
            mc.warning('No nodes found to write')


