'''
'''

import rigrepo.libs.data.node_data as node_data
import rigrepo.libs.curve as curve
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
        super(CurveData, self).gatherData(node)

        data = OrderedDict()
        data['cvPositions'] = list()

        for i,cv in enumerate(mc.ls("{0}.cv[*]".format(node),fl=True)):
            data['cvPositions'].append([round(value, 4) for value in mc.getAttr("{}.controlPoints[{}]".format(node,i))[0]])

        data['degree'] = mc.getAttr('{0}.degree'.format(node))

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