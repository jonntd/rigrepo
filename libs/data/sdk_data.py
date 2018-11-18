'''
This is going to work on SDK's in the scene.
'''
from collections import OrderedDict

import maya.cmds as mc

import rigrepo.libs.data.abstract_data as abstract_data
import rigrepo.libs.sdk

class SdkData(abstract_data.AbstractData):
    '''
    This class is created to store and apply data for setDrivenKeyframes.
    '''
    def __init__(self):
        '''
        The constructor for the sdk class.
        '''
        super(SdkData, self).__init__()

    def gatherData(self, node):
        '''
        This method will gather data for the node that is passed in as an argument. It will
        store this data on the self._data member/attribute on the class.

        :param node: Node you wish to gather the data for.
        :type node: str
        '''
        super(SdkData, self).gatherData(node)

        data = OrderedDict()

        if not mc.ls(node, type=['animCurveUU', 'animCurveUA', 'animCurveUL', 'animCurveUT']):
            raise RuntimeError("{} is not an animCurve that is used for SDK.".format(node))

        # gather the driver and driven for the sdk
        driver = rigrepo.libs.sdk.getSDKdriver(node)
        driven = rigrepo.libs.sdk.getSDKdriven(node)

        # get the pre and post infinity for the sdk
        preInfinity = mc.getAttr('{}.preInfinity'.format(node))
        postInfinity = mc.getAttr('{}.postInfinity'.format(node))

        # update the data dictionary
        data.update({'driver':driver, 
                    'driven':driven, 
                    'preInfinity':preInfinity, 
                    'postInfinity':postInfinity, 
                    'keyframes':[]})

        # loop through the keyframe data for the sdk and store the data.
        for i in xrange(mc.keyframe(node, q=True, keyframeCount=True)):
            driverValue=mc.keyframe(node, index=(i,i), q=True, floatChange=True)[0]
            drivenValue=mc.keyframe(node, index=(i,i), q=True, valueChange=True)[0]

            inTangent=mc.keyTangent(node, index=(i,i), q=True, itt=True)[0]
            outTangent=mc.keyTangent(node, index=(i,i), q=True, ott=True)[0]
            inAngle=mc.keyTangent(node, index=(i,i), q=True, ia=True)[0]
            outAngle=mc.keyTangent(node, index=(i,i), q=True, oa=True)[0]
            lockTangents=mc.keyTangent(node, index=(i,i), q=True, lock=True)[0]
            weightedTangents=mc.keyTangent(node, index=(i,i), q=True, wt=True)[0]
            inWeight=mc.keyTangent(node, index=(i,i), q=True, iw=True)[0]
            outWeight=mc.keyTangent(node, index=(i,i), q=True, ow=True)[0]
            weightLock=mc.keyTangent(node, index=(i,i), q=True, wl=True)[0]

            keyframeValues={'dv':driverValue, 
                            'v':drivenValue, 
                            'itt':inTangent, 
                            'ott':outTangent, 
                            'ia':inAngle, 
                            'oa':outAngle, 
                            'l':lockTangents}

            if weightedTangents:
                keyframeValues.update({'wt':weightedTangents, 
                                        'iw':inWeight, 
                                        'ow':outWeight, 
                                        'wl':weightLock})

            data['keyframes'].append(keyframeValues)

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
                rigrepo.libs.sdk.setSDK(node, 
                                        self._data[node]["keyframes"], 
                                        preInfinity=self._data[node]["preInfinity"], 
                                        postInfinity=self._data[node]["postInfinity"])


