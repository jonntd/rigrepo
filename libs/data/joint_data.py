'''
'''
import rigrepo.libs.data.node_data as node_data
from collections import OrderedDict
import maya.cmds as mc

class JointData(node_data.NodeData):
    '''
    This class will handle the storing and applying of data for joints.
    '''
    def __init__(self):
        '''
        Constructor for the joint data class
        '''
        super(JointData, self).__init__()

    def gatherData(self,node):
        '''
        This method will gather data for the node that is passed in as an argument. It will
        store this data on the self._data member/attribute on the class.

        :param node: Node you wish to gather the data for.
        :type node: str
        '''
        super(JointData, self).gatherData(node)

        data = OrderedDict()
        data['jointOrient'] = [round(value, 4) for value in mc.getAttr("{0}.jo".format(node))[0]]
        data['preferredAngle'] = [round(value, 4) for value in mc.getAttr("{0}.preferredAngle".format(node))[0]]
        data['drawStyle'] = mc.getAttr("{0}.drawStyle".format(node))

        self._data[node].update(data)



    