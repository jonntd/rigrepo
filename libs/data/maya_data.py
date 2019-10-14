'''
This is our maya data module.
'''
from collections import OrderedDict
from rigrepo.libs.data import abstract_data
import maya.cmds as mc

class MayaData(abstract_data.AbstractData):
    def gatherData(self,node):
        '''
        This method will gather data for the node that is passed in as an argument. It will
        store this data on the self._data member/attribute on the class.

        :param node: Node you wish to gather the data for.
        :type node: str
        '''
        if not mc.objExists(node):
            mc.warning("{0} does not exists in the current Maya session.".format(node))
        
        self._data[node] = OrderedDict(dagPath=mc.ls(node,l=True)[0])


