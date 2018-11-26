'''
This is the base data node 
'''
import pubs.pNode
import rigrepo.libs.data.joint_data
import rigrepo.libs.data.node_data
import rigrepo.libs.data.curve_data
import rigrepo.libs.data.deformer_order_data
import maya.cmds as mc
import os


class ExportDataNode(pubs.pNode.PNode):
    def __init__(self, name, dataFile=None, dataType="node"):
        super(ExportDataNode, self).__init__(name)
        self.addAttribute('filepath', dataFile, attrType='file')
        nodesAttr = self.addAttribute('Nodes', 'mc.ls(type="joint")', attrType='str')

        self._dataType = dataType
        self.dataObj = rigrepo.libs.data.node_data.NodeData()
        if dataType == 'joint':
            self.dataObj = rigrepo.libs.data.joint_data.JointData()
            nodesAttr.setValue('mc.ls(mc.listRelatives("bind", ad=True),type="joint", ni=True) + mc.ls("*_pivot",type="joint", ni=True)')
        elif dataType == 'curve':
            self.dataObj = rigrepo.libs.data.curve_data.CurveData()
            nodesAttr.setValue('[mc.listRelatives(shape, p=True)[0] for shape in mc.ls(type="nurbsCurve", ni=True)]')
        elif dataType == 'controlCurve':
            self.dataObj = rigrepo.libs.data.curve_data.CurveData()
            nodesAttr.setValue('mc.listRelatives(mc.listRelatives(mc.ls("*.__control__", o=1), s=1, ni=1, type="nurbsCurve"), p=1) or []')
        elif dataType == 'psd':
            self.dataObj = rigrepo.libs.data.psd_data.PSDData()
            nodesAttr.setValue('mc.ls(type="poseInterpolator")')
        elif dataType == 'sdk':
            self.dataObj = rigrepo.libs.data.sdk_data.SdkData()
            nodesAttr.setValue('mc.ls("*_def_auto*", type=["animCurveUU", "animCurveUA", "animCurveUL", "animCurveUT"])')
        elif dataType == 'deformerOrder':
            self.dataObj = rigrepo.libs.data.deformer_order_data.DeformerOrderData()
            nodesAttr.setValue('[mc.listRelatives(node, p=True)[0] for node in mc.ls(type="mesh")+mc.ls(type="nurbsCurve")]')

    def execute(self, **kwargs):
        dataFile = self.getAttributeByName('filepath').getValue()
        nodes = eval(self.getAttributeByName('Nodes').getValue())
        if nodes: 
            self.dataObj.gatherDataIterate(nodes)
            self.dataObj.write(dataFile)
            print('Writing: {}'.format(dataFile))
        else:
            mc.warning('No nodes found to write')


