'''
This is the base data node 
'''
import pubs.pNode
import rigrepo.libs.data.joint_data
import rigrepo.libs.data.node_data
import rigrepo.libs.data.curve_data
import rigrepo.libs.data.sdk_data
import rigrepo.libs.data.deformer_order_data
import maya.cmds as mc
import os

class ImportDataNode(pubs.pNode.PNode):
    def __init__(self, name, dataFile=None, dataType="node", attributes="[]", apply=False):
        super(ImportDataNode, self).__init__(name)
        self.addAttribute('filepath', dataFile, attrType='file')
        self.addAttribute('Apply', apply, attrType='bool')
        nodesAttr = self.addAttribute('Nodes', 'mc.ls(type="joint")', attrType='str')
        self.addAttribute('attributes', attributes, attrType='str')
        self._dataType = dataType
        self.dataObj = rigrepo.libs.data.node_data.NodeData()
        if dataType == 'joint':
            self.dataObj = rigrepo.libs.data.joint_data.JointData()
        elif dataType == 'curve':
            self.dataObj = rigrepo.libs.data.curve_data.CurveData()
            nodesAttr.setValue('mc.ls("*_curve", type="transform")')
        elif dataType == 'psd':
            self.dataObj = rigrepo.libs.data.psd_data.PSDData()
            nodesAttr.setValue('mc.ls(type="poseInterpolator")')
        elif dataType == 'sdk':
            self.dataObj = rigrepo.libs.data.sdk_data.SdkData()
            nodesAttr.setValue('mc.ls("*_def_auto*", type=["animCurveUU", "animCurveUA", "animCurveUL", "animCurveUT"])')
        elif dataType == 'deformerOrder':
            self.dataObj = rigrepo.libs.data.deformer_order_data.DeformerOrderData()
            nodesAttr.setValue('[mc.listRelatives(node, p=True)[0] for node in mc.ls(type="mesh")+mc.ls(type="nurbsCurve")]')
        elif dataType == 'nodeEditorBookmarks':
            self.dataObj = rigrepo.libs.data.node_editor_bookmark_data.NodeEditorBookmarkData()
            nodesAttr.setValue('None')


    def execute(self, **kwargs):
        dataFile = self.getAttributeByName('filepath').getValue()
        if os.path.isfile(dataFile):
            self.dataObj.read(dataFile)
        else:
            mc.warning('{} does not exist'.format(dataFile)) 
            return

        if self.getAttributeByName('Apply').getValue():
            nodes = eval(self.getAttributeByName('Nodes').getValue())
            attributes = eval(self.getAttributeByName('attributes').getValue())
            if attributes:
                self.dataObj.applyData(nodes, attributes=attributes)
            else:
                self.dataObj.applyData(nodes)
