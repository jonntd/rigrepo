'''
This is our json module.
'''
import rigrepo.libs.data.abstract_data as abstract_data
from collections import OrderedDict
import maya.cmds as mc
import maya.mel as mm

class NodeEditorBookmarkData(abstract_data.AbstractData):
    '''
    Stores data for bookmarks that exist in the node editor
    '''
    def __init__(self):
        '''
        Constructor for the node data class
        '''
        # set class attributes defaults
        super(NodeEditorBookmarkData, self).__init__()

    def gatherData(self,node):
        '''
        This method will gather data for the node that is passed in as an argument. It will
        store this data on the self._data member/attribute on the class.

        :param node: Node you wish to gather the data for.
        :type node: str
        '''
        super(NodeEditorBookmarkData, self).gatherData(node)

        data = OrderedDict()
        data['name'] = mc.getAttr("{0}.{1}".format(node, 'name'))
        # Nodeinfo (compound attr)
        data['nodeInfo'] = list()
        nodeInfoLength = len(mc.ls("{0}.{1}[*]".format(node, 'nodeInfo')))
        for i in xrange(nodeInfoLength):
            data['nodeInfo'].append(OrderedDict())
            x = mc.getAttr('{}.nodeInfo[{}].positionX'.format(node, i))
            y = mc.getAttr('{}.nodeInfo[{}].positionY'.format(node, i))
            nodeVisualState = mc.getAttr('{}.nodeInfo[{}].nodeVisualState '.format(node, i))
            dependNode = mc.listConnections('{}.nodeInfo[{}].dependNode'.format(node, i))[0]

            data['nodeInfo'][i]['positionX'] = x
            data['nodeInfo'][i]['positionY'] = y
            data['nodeInfo'][i]['nodeVisualState'] = nodeVisualState
            data['nodeInfo'][i]['dependNode'] = dependNode

        rect = mc.getAttr(node + '.viewRectHigh')[0]
        data['viewRectHigh'] = rect

        rect = mc.getAttr(node + '.viewRectLow')[0]
        data['viewRectLow'] = rect

        self._data[node].update(data)

    def applyData(self, nodes, attributes=None):
        '''
        Applies the data for the given nodes. There is an optional arguments so you 
        can apply data only to specific attributes.

        :param nodes: Array of nodes you want to apply the data to.
        :type nodes: list | tuple

            nodes = self._data
        :param attributes: Array of attributes you want to apply the data to.
        :type attributes: list | tuple
        '''

        validManager = 'MayaNodeEditorBookmarks'
        if not mc.objExists(validManager):
            mc.createNode('nodeGraphEditorBookmarks', n=validManager)

        # If no nodes are passed load all nodes
        if not nodes:
            nodes = self._data
        for node in nodes:

            if not self._data.has_key(node):
                continue

            if not mc.objExists(node):
                mc.createNode('nodeGraphEditorBookmarkInfo', n=node)

            # Connect bookmark node to manager
            index = mm.eval('getNextFreeMultiIndex "{}.bookmarks" 0'.format(validManager))
            if not mc.listConnections(node+'.message'):
                mc.connectAttr(node+'.message', '{}.bookmarks[{}]'.format(validManager, index))

            data = self._data[node]
            nodeInfo = data['nodeInfo']

            data = self._data[node]
            nodeInfo = data['nodeInfo']
            for i in xrange(len(nodeInfo)):
                index = '{}.nodeInfo[{}]'.format(node, i)
                mc.setAttr(index+'.positionX', nodeInfo[i]['positionX'])
                mc.setAttr(index+'.positionY', nodeInfo[i]['positionY'])
                mc.setAttr(index+'.nodeVisualState', nodeInfo[i]['nodeVisualState'])
                dependNode = nodeInfo[i]['dependNode']
                if mc.objExists(dependNode):
                    mc.connectAttr(dependNode+'.message', index+'.dependNode', f=1)

            mc.setAttr(node + '.viewRectHigh', *data['viewRectHigh'])
            mc.setAttr(node + '.viewRectLow', *data['viewRectLow'])

        # Remove any extra managers that might have been imported
        allManagers = mc.ls(type='nodeGraphEditorBookmarks')
        if len(allManagers) > 1:
            for managerItem in allManagers:
                if managerItem != validManager:
                    mc.delete(managerItem)

