'''
This is going to work on SDK's in the scene.
'''
from collections import OrderedDict

import maya.cmds as mc

import rigrepo.libs.data.abstract_data as abstract_data

class DeformerOrderData(abstract_data.AbstractData):
    '''
    This class is created to store and apply data for deformer order.
    '''
    def __init__(self):
        '''
        The constructor for the sdk class.
        '''
        super(DeformerOrderData, self).__init__()

    def gatherData(self, node):
        '''
        This method will gather data for the node that is passed in as an argument. It will
        store this data on the self._data member/attribute on the class.

        :param node: Node you wish to gather the data for.
        :type node: str
        '''
        super(DeformerOrderData, self).gatherData(node)

        data = OrderedDict()
        data["deformerOrder"] = mc.listHistory(node, pdo=True, interestLevel=1) or list()

        self._data[node].update(data)

    def applyData(self, nodes):
        '''
        Applies the data for the given nodes. There is an optional arguments so you 
        can apply data only to specific attributes.

        :param nodes: Array of nodes you want to apply the data to.
        :type nodes: list | tuple
        '''
        # loop through the nodes and apply the data.
        for node in nodes:
            if self._data.has_key(node):
                if len(self._data[node]["deformerOrder"]) > 1:
                    try:
                        for index, deformer in enumerate(self._data[node]["deformerOrder"]):
                            if index == len(self._data[node]["deformerOrder"]):
                                break
                            mc.reorderDeformers(deformer, self._data[node]["deformerOrder"][index+1], [node])
                    except:
                        mc.warning("couldn't apply data: {} -------> {}".format(node, self._data[node]["deformerOrder"]))


