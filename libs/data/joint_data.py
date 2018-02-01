'''
'''
import rigrepo.libs.data.node_data as node_data
from collections import OrderedDict
import maya.cmds as mc

class JointData(node_data.NodeData):
    def __init__(self):
        '''
        '''
        super(JointData, self).__init__()

    def gatherData(self,node):
        '''
        '''
        super(JointData, self).gatherData(node)

        data = OrderedDict()
        data['jointOrient'] = mc.getAttr("{0}.jo".format(node))[0]
        data['preferredAngle'] = mc.getAttr("{0}.preferredAngle".format(node))[0]
        data['drawStyle'] = mc.getAttr("{0}.drawStyle".format(node))

        self._data[node].update(data)



    