'''
'''
import rigrepo.libs.data.abstract_data as abstract_data
import rigrepo.libs.common as common
from collections import OrderedDict
import maya.cmds as mc

class PSDData(abstract_data.AbstractData):
    def __init__(self):
        '''
        '''
        super(PSDData, self).__init__()

    def gatherData(self, node):
        '''
        '''
        super(PSDData, self).gatherData(node)

        data = OrderedDict()
        data['drivers'] = OrderedDict()
        for driver in mc.ls('%s.driver[*]' % node):
            data['drivers'][driver] = dict()
            data['drivers'][driver]['controllers'] = []
            controllers = mc.listAttr(driver + '.driverController', m=1)
            if not controllers:
                continue
            for ctrl in controllers:
                plug = mc.listConnections(node + '.%s' % ctrl, p=1)
                plug = plug[0]
                plug = str(plug)
                data['drivers'][driver]['controllers'].append(plug)

        data['poses'] = OrderedDict()
        for pose in mc.ls('%s.pose[*]' % node):
            data['poses'][pose] = OrderedDict()
            data['poses'][pose]['controllers'] = dict()
            drivers = mc.ls(pose + '.poseControllerData[*]')
            for drvr in drivers:
                dataItems = mc.ls(drvr + '.poseControllerDataItem[*]')
                for di in dataItems:
                    diDict = OrderedDict()
                    diDict['name'] = mc.getAttr(di + '.poseControllerDataItemName')
                    diDict['type'] = mc.getAttr(di + '.poseControllerDataItemType')
                    diDict['value'] = mc.getAttr(di + '.poseControllerDataItemValue')
                    data['poses'][pose]['controllers'][di] = diDict

        self._data[node].update(data)

    def applyData(self, nodes, mirror=False):
        '''
        '''
        for poseInterp in nodes:
            if not poseInterp in self._data:
                print('psd load: missing poseInterp', poseInterp)
                continue
            for pose in self._data[poseInterp]['poses'].keys():
                dataItems = self._data[poseInterp]['poses'][pose]['controllers'].keys()
                for item in dataItems:
                    name = self._data[poseInterp]['poses'][pose]['controllers'][item]['name']
                    if mirror:
                        name = common.getMirrorName(name)
                    type = self._data[poseInterp]['poses'][pose]['controllers'][item]['type']
                    value = self._data[poseInterp]['poses'][pose]['controllers'][item]['value']
                    if isinstance(value, list):
                        value = value[0]
                    try:
                        if mirror:
                            item = common.getMirrorName(item)
                        mc.setAttr(item + '.poseControllerDataItemName', name, type='string')
                        mc.setAttr(item + '.poseControllerDataItemType', type)
                        if isinstance(value, tuple) or isinstance(value, list):
                            mc.setAttr(item + '.poseControllerDataItemValue', *value, type='float3')
                        else:
                            mc.setAttr(item + '.poseControllerDataItemValue', value)
                    except:
                        pass

            for drvr in self._data[poseInterp]['drivers'].keys():
                ctrlrs = self._data[poseInterp]['drivers'][drvr]['controllers']
                for ctrl in ctrlrs:
                    index = ctrlrs.index(ctrl)
                    try:
                        if mirror:
                            ctrl = common.getMirrorName(ctrl)
                            drvr = common.getMirrorName(drvr)
                        mc.connectAttr(ctrl, drvr + '.driverController[%s]' % index, f=1)
                        pass
                    except:
                        pass
