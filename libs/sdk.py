'''
This module is for handle sdk's in Maya
'''
import maya.cmds as mc
import rigrepo.libs.common


# GET
def getSdk(driver, driven, typeList =['animCurveUU', 'animCurveUA', 'animCurveUL', 'animCurveUT']):
    '''
    This will return the sdk between a driver and driven
    
    :param driver: The driver for the sdk we're looking for.
    :type driver: str
    
    :param driven: The driven for the sdk we're looking for.
    :type driven: str
    
    :return: This will return all sdk's between this driver and driven
    :rtype: list
    '''
    # create an empty set
    sdkSet = set()

    # loop through the driver and driven and check connections
    for obj in [driver, driven]:
        # make sure that the object we're going to check connections on exist in the scene.
        if not mc.objExists(obj):
            raise RuntimeError("{} doesn't exist in the current Maya session".format(obj))
        # get the connections of the driver and driven that are of the type
        connectionList = mc.ls(mc.listConnections(obj, scn=True) , type=typeList)
        # loop through each connection and add it to the sdk list if it's an animCurve.
        for each in connectionList:
            connectionList.extend(mc.ls(mc.listConnections(each, scn=True) , type=typeList))
            sdkSet.update(set(connectionList))

    return list(sdkSet)

def getSDKdriver(sdk):
    '''
    This will return the driver for the sdk that was passed in.

    :param sdk: The setDrivenKeyframe you wish to get the driver from
    :type sdk:  str

    :return: This will return the driver for the setDrivenKeyframe passed in as an argument
    :rtype: str
    '''
    # make sure that the sdk exist in the scene and is an animCurve
    if not mc.ls(sdk, type=['animCurveUU', 'animCurveUA', 'animCurveUL', 'animCurveUT']):
        raise RuntimeError("{} is not an animCurve that is used for SDK's.".format(sdk))

    # get the list of connections from the sdk
    connectionList = mc.listConnections(sdk, s=True, d=False, p=True, scn=True)

    # if there is a connection we will return the connection which should be the driver.
    if connectionList:
        return connectionList[0]
    else:
        return str()

def getSDKdriven(sdk, plug=True):
    '''
    This will return the driven for the sdk that was passed in.

    :param sdk: The setDrivenKeyframe you wish to get the driver from
    :type sdk:  str

    :return: This will return the driven for the setDrivenKeyframe passed in as an argument
    :rtype: str
    '''
    # make sure that the sdk exist in the scene and is an animCurve
    if not mc.ls(sdk, type=['animCurveUU', 'animCurveUA', 'animCurveUL', 'animCurveUT']):
        raise RuntimeError("{} is not an animCurve that is used for SDK's.".format(sdk))

    # get the connection list from the output of the setDrivenKeyframe
    connectionList = mc.listConnections(sdk+'.output', s=False, d=True, p=True, scn=True) or list()

    # if there is a connection and it's a blendWeighted node we will continue and get driven from it
    if connectionList and mc.nodeType(connectionList)=='blendWeighted':
        connectionList=mc.ls(mc.listConnections(connectionList[0].rsplit('.',1)[0], 
                                s=False, d=True, p=plug, scn=True))
    # If there is a connetion list then use it to return the driven
    if connectionList:
        return connectionList[0]
    else:
        return str()


# SET
def setSDK( sdk, keyList, preInfinity=False, postInfinity=False, insert=False):
    '''
    This will set the data on the setDrivenKeyframe. Most of this information is gathered
    using the data.

    :param keyList: Array containing the key information for each key.
    :type keyList: list | tuple

    :param preInfinity: Whether postInfinity is on the curve for the sdk
    :type preInfinity: bool

    :param postInfinity: Whether preInfinity is on the curve for the sdk
    :type postInfinity: bool

    :param insert: If insert is True then insert into existing sdk, otherwise replace it
    :type insert: bool
    '''
    # if we're replacing the sdk and a name isn't provided, use the name of the existing sdk
    if not mc.objExists(sdk):
        raise RuntimeError("{} doesn't exist in the current Maya session.".format())

    # Get the driver and driven
    driver = getSDKdriver(sdk)
    driven = getSDKdriven(sdk)

    if not insert:
        # create the key frame at a rediculous number to preserve the animCurve node.
        mc.setKeyframe(sdk, insert=True, float=1000001)
        mc.cutKey(sdk,f=(-100000,100000), clear=True)

    # Create keys 
    for keyData in keyList:
       mc.setDrivenKeyframe(driven, cd=driver, dv=keyData['dv'], v=keyData['v'])

    # cut the key at a ridiculous number
    mc.cutKey(sdk,f=(1000001,1000001), clear=True)

    if preInfinity:
        mc.setAttr('{}.preInfinity'.format(sdk), preInfinity)

    if postInfinity:
        mc.setAttr('{}.postInfinity'.format(sdk), postInfinity)

    # then loop to set tangents.  this doesn't work if done in the same loop that the keys are created

    for i, keyData in enumerate(keyList):
        args=keyData.copy()
        args.pop('dv', None)
        args.pop('v', None)
        
        # Make sure the absolute value is set on the curve
        mc.keyframe(sdk,index=(i,i),absolute=True, valueChange= keyData['v'])

        if args:
            # weighted tangets must be applied separately or else other args are ignored
            if keyData.has_key('wt'):
                mc.keyTangent(sdk, f=(keyData['dv'], keyData['dv']), wt=keyData['wt'])
                args.pop('wt', None)
            # if the tangents aren't set to fixed we will take them out and not apply them.
            # reson for this is that if you apply tangents they will automatically be set to fixed.
            if args['itt']!='fixed':
                args.pop('ia', None)
            if args['ott']!='fixed':
                args.pop('oa', None)

            args = rigrepo.libs.common.convertDictKeys(args)
            mc.keyTangent(sdk, f=(keyData['dv'], keyData['dv']), **args)

    return sdk