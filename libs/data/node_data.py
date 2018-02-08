'''
This is our json module.
'''
import rigrepo.libs.data.abstract_data as abstract_data
from collections import OrderedDict
import maya.cmds as mc

class NodeData(abstract_data.AbstractData):
    '''
    '''
    def __init__(self):
        '''
        '''
        # set class attributes defaults
        super(NodeData, self).__init__()

    def gatherData(self,node):
        '''
        '''
        super(NodeData, self).gatherData(node)

        data = OrderedDict()
        for attr in ['translate','rotate','scale']:
            data[attr] = mc.getAttr("{0}.{1}".format(node,attr))[0]

        data['rotateOrder'] = mc.getAttr("{0}.rotateOrder".format(node))

        self._data[node].update(data)


    def applyData(self, nodes, attributes=None):
        '''
        '''
        for node in nodes:
            if not attributes:
                attributes = self._data[node].keys()

            for attribute in attributes:
                if self._data[node].has_key(attribute) and attribute in mc.listAttr(node):
                    if mc.listConnections('{0}.{1}'.format(node,attribute), d=False, s=True) or \
                        mc.getAttr('{0}.{1}'.format(node,attribute),l=True):
                        continue
                    value = self._data[node][attribute]
                    if isinstance(value, (list,tuple)):
                        mc.setAttr('{0}.{1}'.format(node,attribute),*value)    
                    elif isinstance(value,basestring):
                        mc.setAttr('{0}.{1}'.format(node,attribute),value, type="string")
                    else:
                        mc.setAttr('{0}.{1}'.format(node,attribute),value)




