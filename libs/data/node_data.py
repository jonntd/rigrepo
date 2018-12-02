'''
This is our json module.
'''
import rigrepo.libs.data.abstract_data as abstract_data
from collections import OrderedDict
import maya.cmds as mc

class NodeData(abstract_data.AbstractData):
    '''
    handle mostly storing data for transform nodes.
    '''
    def __init__(self):
        '''
        Constructor for the node data class
        '''
        # set class attributes defaults
        super(NodeData, self).__init__()

    def gatherData(self,node):
        '''
        This method will gather data for the node that is passed in as an argument. It will
        store this data on the self._data member/attribute on the class.

        :param node: Node you wish to gather the data for.
        :type node: str
        '''
        super(NodeData, self).gatherData(node)

        data = OrderedDict()
        for attr in ['translate','rotate','scale']:
            data[attr] = [round(value, 4) for value in mc.getAttr("{0}.{1}".format(node,attr))[0]]

        data['rotateOrder'] = mc.getAttr("{0}.rotateOrder".format(node))

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
        for node in nodes:
            if not self._data.has_key(node):
                continue
            if not attributes:
                attributes = self._data[node].keys()

            for attribute in attributes:
                if self._data[node].has_key(attribute) and attribute in mc.listAttr(node):
                    setAttr = True
                    for attr in mc.listAttr("{}.{}".format(node, attribute)):
                        if mc.listConnections('{0}.{1}'.format(node,attr), d=False, s=True) or \
                            mc.getAttr('{0}.{1}'.format(node,attr),l=True):
                                setAttr = False
                                break
                    if not setAttr:
                        continue
                    value = self._data[node][attribute]
                    if isinstance(value, (list,tuple)):
                        mc.setAttr('{0}.{1}'.format(node,attribute),*value)    
                    elif isinstance(value,basestring):
                        mc.setAttr('{0}.{1}'.format(node,attribute),value, type="string")
                    else:
                        mc.setAttr('{0}.{1}'.format(node,attribute),value)




