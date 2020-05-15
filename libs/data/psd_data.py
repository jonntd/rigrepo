'''
'''
import rigrepo.libs.data.maya_data as maya_data
import rigrepo.libs.common as common
from collections import OrderedDict
import maya.cmds as mc

class PSDData(maya_data.MayaData):
    def __init__(self):
        '''
        '''
        super(PSDData, self).__init__()

    def gatherData(self, node):
        '''

        interpolator
            regularization
                float
            outputSmoothing
                float
            interpolation
                enum
            allowNegativeWeights
                bool
            trackRotation
                bool
            trackTranslation
                bool
            poses
                type
                    enum
                enabled
                    bool
                drivenShapes
                    numpyArrayIndex
                        numpy file
                            weights
                            deltas
            drivers
                twistAxis
                    enum
                eulerTwist
                    bool
                controllers
                    array

        '''
        super(PSDData, self).gatherData(node)

        data = OrderedDict()


        # Interpolator settings
        #
        data['regularization'] = mc.getAttr('{}.regularization'.format(node))
        data['outputSmoothing'] = mc.getAttr('{}.outputSmoothing'.format(node))
        data['interpolation'] = mc.getAttr('{}.interpolation'.format(node))
        data['allowNegativeWeights'] = mc.getAttr('{}.allowNegativeWeights'.format(node))
        data['enableRotation'] = mc.getAttr('{}.enableRotation'.format(node))
        data['enableTranslation'] = mc.getAttr('{}.enableTranslation'.format(node))

        # Drivers
        data['drivers'] = OrderedDict()
        for driver in mc.ls('%s.driver[*]' % node):
            data['drivers'][driver] = dict()

            # Controllers
            data['drivers'][driver]['controllers'] = []
            controllers = mc.listAttr(driver + '.driverController', m=1)
            if controllers:
                for ctrl in controllers:
                    plug = mc.listConnections(node + '.%s' % ctrl, p=1)
                    if not plug:
                        continue
                    plug = plug[0]
                    plug = str(plug)
                    data['drivers'][driver]['controllers'].append(plug)
            # twistAxis
            value = mc.getAttr(driver+'.driverTwistAxis')
            data['drivers'][driver]['driverTwistAxis'] = value
            # eulerTwist
            value = mc.getAttr(driver+'.driverEulerTwist')
            data['drivers'][driver]['driverEulerTwist'] = value

        # Poses
        data['poses'] = OrderedDict()
        for pose in mc.ls('%s.pose[*]' % node):
            data['poses'][pose] = OrderedDict()

            # Controllers
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

            # Settings
            attrs = [
                'poseName',
                'isEnabled',
                'poseType',
                #'poseRotation',
                #'poseTranslation',
                'isIndependent',
                'poseFalloff',
                'poseRotationFalloff',
                'poseTranslationFalloff',
                ]
            for attr in attrs:
                value = mc.getAttr(pose+'.'+attr)
                data['poses'][pose][attr] = value

            # Drivens
            poseIndex = common.getIndex(pose)
            attr = '{}.output[{}]'.format(node, poseIndex)
            if mc.objExists(attr):
                drivens = mc.listConnections(attr, p=1)
                data['poses'][pose]['drivens'] = drivens

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
