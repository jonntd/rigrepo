'''
'''

import rigrepo.libs.data.node_data as node_data
import rigrepo.libs.curve as curve
from collections import OrderedDict
from pxr import Usd, UsdGeom
import maya.cmds as mc

class CurveData(node_data.NodeData):
    def __init__(self):
        '''
        '''
        super(CurveData, self).__init__()

    def gatherData(self,node):
        '''
        '''
        super(CurveData, self).gatherData(node)

        data = OrderedDict()
        data['cvPositions'] = list()

        for i,cv in enumerate(mc.ls("{0}.cv[*]".format(node),fl=True)):
            data['cvPositions'].append(mc.getAttr("{}.controlPoints[{}]".format(node,i))[0])

        data['degree'] = mc.getAttr('{0}.degree'.format(node))

        self._data[node].update(data)

    def applyData(self, nodes, attributes=None):
        '''
        '''
        super(CurveData, self).applyData(nodes, attributes)
        for node in nodes:
            if not node in self._data:
                continue
            if not attributes:
                attributes = self._data[node].keys()

            for attribute in attributes:
                if not self._data[node].has_key(attribute):
                    continue

                if attribute == 'cvPositions':
                    for i,position in enumerate(self._data[node][attribute]):
                        mc.setAttr("{}.controlPoints[{}]".format(node,i), *position)