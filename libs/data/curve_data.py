'''
'''

import rigrepo.libs.data.node_data as node_data
import rigrepo.libs.curve as curve
from collections import OrderedDict
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
            data['cvPositions'].append(mc.xform(cv,q=True,ws=True,t=True))

        data['degree'] = mc.getAttr('{0}.degree'.format(node))

        self._data[node].update(data)

    