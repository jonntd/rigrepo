'''
'''

import rigrepo.libs.data.node_data as node_data
import rigrepo.libs.curve as curve
import rigrepo.libs.common as common
from collections import OrderedDict
from pxr import Usd, UsdGeom
import maya.cmds as mc

class CurveData(node_data.NodeData):
    '''
    This class will handle storing and applying curve data.
    '''
    def __init__(self):
        '''
        Constructor for the curve data class
        '''
        super(CurveData, self).__init__()

    def gatherData(self,node):
        '''
        This method will gather data for the node that is passed in as an argument. It will
        store this data on the self._data member/attribute on the class.

        :param node: Node you wish to gather the data for.
        :type node: str
        '''
        if mc.nodeType(node) == "nurbsCurve":
            node = mc.listRelatives(node,p=True)[0]
        super(CurveData, self).gatherData(node)

        data = OrderedDict()
        shapeList = mc.listRelatives(node, c=True, shapes=True, type="nurbsCurve")
        data['shapes'] =OrderedDict()
        for shape in shapeList:
            data['shapes'][shape] = OrderedDict()
            data['shapes'][shape]['cvPositions'] = list()
            for i,cv in enumerate(mc.ls("{0}.cv[*]".format(shape),fl=True)):
                data['shapes'][shape]['cvPositions'].append([round(value, 4) for value in mc.getAttr("{}.controlPoints[{}]".format(shape,i))[0]])

            data['shapes'][shape]['degree'] = mc.getAttr('{0}.degree'.format(shape))
            formNames = mc.attributeQuery("f",node=shape, le=True)[0].split(":")
            data['shapes'][shape]["form"] = formNames[mc.getAttr("{}.f".format(shape))]

            data["color"] = mc.getAttr("{}.overrideColor".format(node))

        self._data[node].update(data)

    def applyData(self, nodes, attributes=None):
        '''
        Applies the data for the given nodes. There is an optional arguments so you 
        can apply data only to specific attributes.

        :param nodes: Array of nodes you want to apply the data to.
        :type nodes: list | tuple

        :param attributes: Array of attributes you want to apply the data to.
        :type attributes: list | tuple
        '''
        mc.undoInfo(openChunk=1)
        super(CurveData, self).applyData(nodes, attributes)
        for node in nodes:
            if not node in self._data:
                continue
            if not attributes:
                attributes = self._data[node].keys() + ["cvPositions"]

            for attribute in attributes:
                if attribute == 'cvPositions':
                    form = "Open"
                    if 'shapes' not in self._data[node]:
                        continue
                    for shape in self._data[node]['shapes'].keys():
                        if not mc.objExists(shape):
                            if self._data[node]['shapes'][shape].has_key("form"):
                                form = self._data[node]['shapes'][shape]["form"]
                            curveTrs = curve.createCurveFromPoints(self._data[node]['shapes'][shape][attribute], 
                                            self._data[node]["shapes"][shape]['degree'], 
                                            name=node+"_temp", 
                                            transformType="transform",
                                            form=form)
                            shapeNode = mc.listRelatives(curveTrs, c=True, shapes=True, type="nurbsCurve")[0]
                            mc.rename(shapeNode, shape)
                            mc.parent(shape, node, r=True, s=True)
                            mc.delete(curveTrs)
                        else:
                            for i,position in enumerate(self._data[node]['shapes'][shape][attribute]):
                                mc.setAttr("{}.controlPoints[{}]".format(shape,i), *position)

            if self._data[node].has_key("color"):
                mc.setAttr("{}.overrideEnabled".format(node), 1)
                mc.setAttr("{}.overrideColor".format(node), self._data[node]["color"])
        mc.undoInfo(closeChunk=1)

                