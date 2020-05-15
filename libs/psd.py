"""
This is a module for libraries used for psd.

Glossary
group   - A grouping of interpolator nodes.
interp  - Interpolator node that runs the radial basis functions.
driver  - A node giving input to the interpolator calculation.
pose    - A data point of the interpolator. The interpolator interpolates between the stored
          values of each pose's data point. A pose also has a list of stored values for the
          associated pose controls.
poseControl - Attributes whose values are stored for a giving pose. (Maya=driverController)
"""

import maya.cmds as mc
import maya.mel as mm
import rigrepo.libs.common as common
import math

'''     Logging levels
50 CRITICAL
40 ERROR
30 WARNING
20 INFO
10 DEBUG
0  NOTSET
'''
import logging
logger_level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(logger_level)
logger_format = '%(levelname)-6s %(funcName)-25s %(message)s  [%(name)s:%(lineno)s]'
loggger_func_len = 0

if not logger.handlers:
    # create console handler
    handler = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter(logger_format)
    # add formatter to ch
    handler.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(handler)
else:
    handler = logger.handlers[0]
handler.setLevel(logger_level)

# make sure the poseInterpolator plugin is loaded.
mc.loadPlugin("poseInterpolator.so", qt=True)
manager = 'poseInterpolatorManager'

def addInterp(name,
              createNeutralPose=0,
              driver=None,
              regularization=0,
              outputSmoothing=0,
              interpolation=1,
              allowNegativeWeights=1,
              enableRotation=1,
              enableTranslation=0,
              twistAxis=0):
    '''
    :param name: Name of interpolator node
    :param driver: driver name
    :param createNeutralPose: Add swing, twist, and swing/twist neutral pose
    :param twistAxis:
    :return: poseInterpolator
    '''

    if driver:
        mc.select(driver)
    interp = mm.eval('createPoseInterpolatorNode("{}", "{}", "{}")'.format(name, createNeutralPose, twistAxis))

    mc.setAttr(interp+'.regularization', regularization)
    mc.setAttr(interp+'.outputSmoothing', outputSmoothing)
    mc.setAttr(interp+'.interpolation', interpolation)
    mc.setAttr(interp+'.allowNegativeWeights', allowNegativeWeights)
    mc.setAttr(interp+'.enableRotation', enableRotation)
    mc.setAttr(interp+'.enableTranslation', enableTranslation)
    return interp

def getInterp(node):
    '''
    Used to convert a dag node to the interpolator node. If
    a transform is passed a interpoloator shape is returned. If the node is a shape
    and an interpolator, it is just passed through.

    :param node: Any dag node.
    :return: interpoloator node related to the passed node
    '''
    node = common.getFirstIndex(node)
    if mc.nodeType(node) == 'transform':
        shape = common.getFirstIndex(mc.listRelatives(node, s=1, ni=1))
        if shape:
            node = shape

    if mc.nodeType(node) == 'poseInterpolator':
        return(node)

def getInterpData(node):
    '''
    :param node: Pose interpololator
    :return: dictionary of all the data that makes up the inpterpolator

    Data keys

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
def addPose(interp, pose, type='swing'):
    '''

    :param interp: Pose interpolator
    :param pose: Pose name
    :param type: options are: swing, twist, and swingandtwist
    :return: Index of added pose
    '''
    index = mm.eval('poseInterpolatorAddPose("{interp}", "{pose}")'.format(interp=interp,
                                                                               pose=pose))
    mm.eval('poseInterpolatorSetPoseType("{interp}", "{pose}", "{type}")'.format(interp=interp,
                                                                                     pose=pose,
                                                                                     type=type))
    pose_name = getPoseName(interp, index)
    return pose_name

def renamePose(interp, poseName, newName):
    '''

    :param interp: Pose interpolator transform
    :param poseName: Name of pose
    :param newName: New name of pose
    :return: None
    '''
    # api call
    #mm.eval('poseInterpolator -edit -rename {poseName} {newName} {tpl};'.format(tpl=tpl,
    #                                                                            poseName=poseName,
    #                                                                            newName='shoulder_l_down'))
    mm.eval('poseInterpolatorRenamePose {interp} {poseName} {newName}'.format(interp=interp,
                                                                                  poseName=poseName,
                                                                                  newName=newName))
def getPoseNames(interp):
    poses = mc.poseInterpolator(interp, q=1, poseNames=1)
    return(poses)

def getPoseName(interp, index):
    '''
    :param interp: Pose interpolator
    :param index: Index to query pose name from
    :return:
    '''
    interp = getInterp(interp)
    attr = interp+'.pose[{}].poseName'.format(index)
    pose_name = None
    if mc.objExists(attr):
        pose_name = mc.getAttr(interp+'.pose[{}].poseName'.format(index))
    return pose_name

def getPoseIndexes(interp):
    poseIndexes = mc.poseInterpolator(interp, q=1, index=1)
    return(poseIndexes)

def getPoseIndex(interp, pose):
    index = mm.eval('poseInterpolatorPoseIndex("{}", "{}")'.format(interp, pose))
    if index != -1:
        return(int(index))

def getPoseShapeIndex(interp, pose):
    bs = getDeformer(interp)
    if not bs:
        return
    poseIndex = getPoseIndex(interp, pose)
    if not poseIndex:
        return
    connectedTarget = mc.listConnections(interp+'.output[{}]'.format(poseIndex), p=1)
    if connectedTarget:
        targetName = connectedTarget[0].split('.')[1]
        index = getTargetShapeIndex(targetName, bs)
        return(index)

def getTargetShapeIndex(target, bs):
    targetCount = mc.blendShape(bs, q=1, target=1, wc=1)

    i = 0
    n = 0
    while n < targetCount:
        alias = mc.aliasAttr(bs + '.w[{}]'.format(i), q=1)
        if alias == target:
            return i
        if alias:
            n += 1
        i += 1

def getDrivers(interp):
    drivers = mc.poseInterpolator(interp, q=1, drivers=1)
    return(drivers)

def addPoseControl(interp, controlAttr):
    '''
    Maya alls pose controls driver controllers. Each driver has pose controls associated with it.
    Adds anim control as a pose controller (driver controller). When going to a pose this sets up
    what values are set on the driver controllers.

    :param interp: Pose interpolator transform
    :param controlAttr: Anim control and attribute to add to the pose controls for the pose interpolator.
                        Example: shoulder_fk_l.r
    :return: None
    '''

    interp = getInterp(interp)
    poseInterpAttr = interp + '.driver[0].driverController'
    index = mm.eval('getNextFreeMultiIndex("{poseInterpAttr}", 1)'.format(poseInterpAttr=poseInterpAttr))
    mm.eval('connectAttr -f "{controlAttr}" "{poseInterpAttr}[{index}]" '.format(controlAttr=controlAttr,
                                                                                 poseInterpAttr=poseInterpAttr,
                                                                                 index=index))
def removePoseControl(interp, controlAttr):
    controlAttr = common.getFirstIndex(controlAttr)
    interp = getInterp(interp)
    poseInterpAttrs = mc.ls(interp + '.driver[0].driverController[*]')
    control = controlAttr.split('.')[0]
    for attr in poseInterpAttrs:
        conControl = common.getFirstIndex(mc.listConnections(attr))
        if control == conControl:
            logger.info('disconnecting:  %s %s ', controlAttr, attr)
            mc.disconnectAttr(controlAttr, attr)

def getPoseControls(interp):
    driversData = mc.ls(interp + '.driver[*]')
    driverData = driversData[0]
    poseControlData = mc.listAttr(driverData + '.driverController', m=1)
    if not poseControlData:
        return(list())
    poseControls = list()
    for control in poseControlData:
        connectedControls = mc.listConnections(interp + '.%s' % control, p=1)
        if connectedControls:
            poseControls += connectedControls
    return(poseControls)

def getPoseControlIndex(interp, poseControl):
    '''
    Get the index of the passed poseControl
    :param interp: pose interpolator
    :param poseControl: Pose control must be the node and the attribute
    :return:
    '''
    # Get all the drivers
    driversData = mc.ls(interp + '.driver[*]')
    print('driversData', driversData)
    driverData = driversData[0]
    poseControlData = mc.listAttr(driverData + '.driverController', m=1)

    for control in poseControlData:
        print(control, 'control')
        connectedControls = mc.listConnections(interp + '.%s' % control, p=1)
        #if connectedControls:
        if poseControl == connectedControls[0]:
            # The driver controller array is 1 based for some reason, so subtract 1.
            print(int(common.getIndex(control))-1, 'index')
            return int(common.getIndex(control))-1

def getPoseControlData(interp, pose):
    index = getPoseIndex(interp, pose)
    if not index:
        return
    poseControlData = mc.ls('{}.pose[{}].poseControllerData[*]'.format(interp, index))
    poseControlValues = list()
    for data in poseControlData:
        name = mc.getAttr(data + '.poseControllerDataItemName')
        type = mc.getAttr(data + '.poseControllerDataItemType')
        value = mc.getAttr(data + '.poseControllerDataItemValue')
        poseControlValues.append([name, type, value])
    return(poseControlValues)

def getPoseControlValueAttr(interp, pose, poseControl):
    logger.debug("%s", locals())
    pose_index = getPoseIndex(interp, pose)
    pose_control_index = getPoseControlIndex(interp, poseControl)

    if pose_index != None and pose_control_index !=None:
        # Build pose control value attribute name
        attr = '{}.pose[{}].poseControllerData[0]'.format(interp, pose_index)
        attr += '.poseControllerDataItem[{}]'.format(pose_control_index)
        attr += '.poseControllerDataItemValue'
        return attr

def getPoseControlRotate(interp, pose, poseControl):
    logger.debug("%s", locals())
    attr = getPoseControlValueAttr(interp, pose, poseControl)
    if not mc.objExists(attr):
        logger.debug('Attribute does not exist: %s', attr)
        return
    value = mc.getAttr(attr)[0]
    value_in_degrees = [math.degrees(x) for x in value]
    logger.debug('value of attr: %s', value_in_degrees)
    return(value_in_degrees)

def setPoseControlRotate(interp, pose, poseControl, value=[0, 0, 0]):
    attr = getPoseControlValueAttr(interp, pose, poseControl)
    if not mc.objExists(attr):
        logger.debug('Attribute does not exist: %s', attr)
        return
    value_in_radians = [math.radians(x) for x in value]
    mc.setAttr(attr, type='double3', *value_in_radians)

def setPoseControlData(interp, pose, name, type, value):
    """
    :param interp: PoseInterpolator name
    :param pose: Pose name
    :param name: Name of the control attribute. e.g. controlName.rotate
    :param type: Control attribute type. e.g rotate = 8
    :param value: Value for attribute. e.g. rotates should be in radians (1.2, 2.0, 3.0]
    :return: None

    """
    index = getPoseIndex(interp, pose)
    if not index:
        return
    poseControlData = mc.ls('{}.pose[{}].poseControllerData[*]'.format(interp, index))
    for data in poseControlData:
        cur_name = mc.getAttr(data + '.poseControllerDataItemName')
        if cur_name == name:
            mc.setAttr(data + '.poseControllerDataItemName', name, type='string')
            mc.setAttr(data + '.poseControllerDataItemType', type)
            if type == 8:
                mc.setAttr(data + '.poseControllerDataItemValue', *value, type='double3')

def getDeformer(interp):
    # Mel call
    # poseInterpolatorConnectedShapeDeformers

    interp = getInterp(interp)
    poses = getPoseNames(interp)
    indexes = getPoseIndexes(interp)
    for pose, index in zip(poses, indexes):
        con = mc.listConnections(interp+'.output[{index}]'.format(index=index))
        if con:
            if mc.nodeType(con[0]) == 'blendShape':
                return(con[0])

def goToPose(interp, pose):
    mm.eval('poseInterpolatorGoToPose "{}" "{}"'.format(interp, pose))

def goToNeutralPose(interp):
    poses = getPoseNames(interp)
    for pose in poses:
        if pose == 'neutral':
            goToPose(interp, pose)

def updatePose(interp, poseName):
    '''
    :param interp: Pose interpolator transform
    :param poseName: Name of pose
    :return: None
    '''

    mm.eval('poseInterpolator -edit -updatePose {poseName} {interp}'.format(interp=interp,
                                                                                poseName=poseName))
def syncPose(interp, pose):
    goToPose(interp, pose)
    updatePose(interp, pose)

def setPoseKernalFalloff(interp, pose):
    '''
    Auto adjusts the gaussian falloff for a more normalized overlap between poses
    :param interp: Pose interpolator
    :param pose: Pose name
    :return: None
    '''
    mm.eval('poseInterpolatorCalcKernelFalloff"{}" "{}"'.format(interp, pose))

def addShape(interp, pose, bs=None):
    interp = getInterp(interp)

    if not bs:
        bs = getDeformer(interp)
    if not bs:
        return

    shapeIndex = mm.eval('doBlendShapeAddTarget("{bs}", 1, 1, "", 0, 0, {{}})'.format(bs=bs))[0]
    mc.aliasAttr(pose, bs+'.w[{index}]'.format(index=shapeIndex))

    poseIndex = getPoseIndex(interp, pose)
    mc.connectAttr(interp+'.output[{}]'.format(poseIndex), bs+'.w[{}]'.format(shapeIndex))

def remShape(interp, pose, bs=None):
    interp = getInterp(interp)

    if not bs:
        bs = getDeformer(interp)
    if not bs:
        return

    shapeIndex = mm.eval('doBlendShapeAddTarget("{bs}", 1, 1, "", 0, 0, {{}})'.format(bs=bs))[0]
    mc.aliasAttr(pose, bs+'.w[{index}]'.format(index=shapeIndex))

    poseIndex = getPoseIndex(interp, pose)
    mc.connectAttr(interp+'.output[{}]'.format(poseIndex), bs+'.w[{}]'.format(shapeIndex))

def getAllGroups():
    groupIndexes = mc.ls(manager + '.poseInterpolatorDirectory[*]')
    groups = list()
    for group in groupIndexes:
        name = mc.getAttr(group + '.directoryName')
        # Ignore the default groups named "Group"
        if name == 'Group':
            continue
        # Ignore groups with no interpolator children
        if not getGroupChildren(name):
            continue
        groups.append(name)
    return groups

def getGroupChildren(group):
    # Directories are any pose interpoloator group
    groupAttrs = mc.ls(manager + '.poseInterpolatorDirectory[*]')
    for groupAttr in groupAttrs:
        name = mc.getAttr(groupAttr + '.directoryName')
        if name != group:
            continue

        childAttrs = mc.getAttr(groupAttr + '.childIndices')
        if not childAttrs:
            return []
        children = list()
        for childAttr in childAttrs:
            childAttr = int(childAttr)
            # The child index is -2 if there are no children
            # or if the only child is a group, guessing...
            if childAttr == -2:
                continue
            child = mc.listConnections(manager+'.poseInterpolatorParent[{}]'.format(childAttr))
            child = common.getFirstIndex(child)
            child = getInterp(child)
            if child:
                children.append(child)
        return(children)

def getGroup(interp):
    interp = getInterp(interp)
    if not interp:
        return
    con = mc.listConnections(interp+'.midLayerParent', p=1)
    con = common.getFirstIndex(con)
    index = int(con.split('[')[1].replace(']',''))
    groups = mc.ls(manager + '.poseInterpolatorDirectory[*]')
    for group in groups:
        name = mc.getAttr(group + '.directoryName')
        childIndices = mc.getAttr(group + '.childIndices')
        if index in childIndices:
            return(name)

def deleteGroup(group):
    '''
    Delete all interpoloators and targets for the given group
    :param group:
    :return: None
    '''
    if not group in getAllGroups():
        mc.warning('psd group [ {} ] does not exist'.format(group))
        return
    interps = getGroupChildren(group)
    if interps:
        deleteInterp(interps)

def deleteInterp(interp):
    '''
    Delete interpolaotr and it's poses and drivens.
    :param interp:
    :return:
    '''
    pass

def deletePose(interp, pose):
    '''
    Delete the pose and its drivens
    :param interp:
    :param pose:
    :return:
    '''
    pass

def deleteDriven(interp, pose, driven):
    '''
    Delete the driven for the given pose
    :param interp:
    :param pose:
    :return:
    '''
    pass

def disablePose(interp, pose):
    interp = getInterp(interp)
    poseIndex = getPoseIndex(interp, pose)
    mc.setAttr('{}.pose[{}].isEnabled'.format(interp, poseIndex), 0)

def enablePose(interp, pose):
    interp = getInterp(interp)
    poseIndex = getPoseIndex(interp, pose)
    mc.setAttr('{}.pose[{}].isEnabled'.format(interp, poseIndex), 1)


