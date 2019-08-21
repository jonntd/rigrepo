"""
This module is for dealing with blendShapes inside Maya
"""
import maya.cmds as mc
import maya.mel as mm
import rigrepo.libs.common
import rigrepo.libs.wrap
import rigrepo.libs.shape as shape
import os

def transferBlendShape(source, target, deformer, differentTopology=0, connections=1):
    """
    This will transfer blendShape from one mesh to another. If the target doesn't have a
    blendShape on it, it will create a new blendShape. Then once there is a blendShape
    We will copy weights over.

    :param source: The geomertry you are transfer from
    :type source:  str

    :param target: The geometry you want to transfer to
    :type target: str | list

    """
    # do some error checking
    if not mc.objExists(source):
        raise RuntimeError('The source mesh "{}" does not exist in the current Maya session.'.format(source))

    # first we will turn the target into a list if it's not already a list
    targetMeshList = rigrepo.libs.common.toList(target)

    # make sure we have a blendShape on the source mesh
    sourceBlendShapes = getBlendShapes(source)
    blendShapeList = list()
    if deformer not in sourceBlendShapes:
        mc.warning('The source mesh "{}" is missing "{}"'.format(source, deformer))
        return

    # Loop through target meshes
    for targetMesh in targetMeshList:
        if not mc.objExists(targetMesh):
            mc.warning('The target mesh "{}" does not exist in the current Maya session.'.format(target))
            continue

        # check to see if there is a blendShape already  on the target mesh
        hist = getBlendShapes(targetMesh)
        if deformer in hist:
            mc.warning('The target mesh "{}" is being deformed by "{}", aborting.'.format(targetMesh, deformer))
            continue

        name = "{}_bs".format(targetMesh)

        # =================
        # Same Topology
        # =================
        if not differentTopology:
            # Build blendShape
            target_bs = mc.blendShape(targetMesh, n=deformer)[0]
            targets = getTargetNames(deformer)

            for target in targets:
                # Get target data
                deltas, indices = getTargetDeltas(deformer, target)
                targetWeight = getTargetWeight(deformer, target)
                # Add target
                target = addTarget(target_bs, name=target)
                # Set target data
                setTargetWeight(target_bs, target, targetWeight)
                setTargetDeltas(target_bs, deltas, indices, target)
            blendShapeList.append(target_bs)

        # =================
        # Different Topology
        # =================
        if differentTopology:

            # Dup Source - Make duplicate of source mesh and bs so it can be
            #              wrapped to and the targets can to turned on and off
            #              without interfering with any connections that may exist
            #              on the original source meshes blendshape.
            #              Build blendShape
            wrap_target_dup = mc.duplicate(source, n=source+'_wrap_target')[0]
            wrap_target_bs = transferBlendShape(source, wrap_target_dup, deformer)[0]
            mc.polySmooth(wrap_target_dup)

            # Dup Target - Make a duplicated of the target mesh and wrap it to the
            #              target dup.
            wrap_source_dup = mc.duplicate(targetMesh, n=targetMesh+'_wrapped')[0]
            # Dup Target Get Deltas - Make another dup of the tafget that is
            #                         blendshaped to the wrapped dup target.
            #                         This is the blendShape we will get the deltas from
            get_deltas_from_wrap_dup = mc.duplicate(targetMesh, n=targetMesh+'_get_deltas')[0]
            mc.select(get_deltas_from_wrap_dup)
            get_deltas_from_wrap_bs = mc.blendShape(wrap_source_dup, get_deltas_from_wrap_dup, w=[0,1])[0]
            mm.eval('performDeltaMush 0')

            # Wrap the source dup to the target dup
            wrap_node = rigrepo.libs.wrap.createWrap(wrap_source_dup, wrap_target_dup, exclusiveBind=1)

            # Build target blendShape
            target_bs = mc.blendShape(targetMesh, n=deformer)[0]

            targets = getTargetNames(deformer)
            connectionsList = list()
            for target in targets:
                # Turn on the target
                setTargetWeight(wrap_target_bs, target, 1)

                # Get target data
                deltas, indices = getTargetDeltas(get_deltas_from_wrap_bs, 0)
                targetWeight = getTargetWeight(deformer, target)
                connection = mc.listConnections(deformer+'.'+target, p=1) or []
                connectionsList.append(connection)

                # Add target
                target = addTarget(target_bs, name=target)

                # Set target data
                setTargetWeight(target_bs, target, targetWeight)
                setTargetDeltas(target_bs, deltas, indices, target)

                # Turn off the target
                setTargetWeight(wrap_target_bs, target, 0)

            # Hook up connections
            if connections:
                for target, con in zip(targets, connectionsList):
                    if con:
                        mc.connectAttr(con[0], target_bs+'.'+target)

            # Garbage collection
            mc.delete(wrap_target_dup, wrap_source_dup, get_deltas_from_wrap_dup)

            blendShapeList.append(target_bs)

    return blendShapeList

def addTarget(bs, name=None):
    """
    Add a blank target to blendShape
    :param bs: BlendShape node
    :param name: Name of the target to be added
    :return: Name of created target
    """
    shapeIndex = mm.eval('doBlendShapeAddTarget("{bs}", 1, 1, "", 0, 0, {{}})'.format(bs=bs))[0]
    mc.aliasAttr(name, bs+'.w[{index}]'.format(index=shapeIndex))
    targetName = mc.aliasAttr(bs+'.w[{index}]'.format(index=shapeIndex), q=1)
    return targetName

def getBlendShapes(geometry):
    """
    This will check the geometry to see if it has a blendShape in it's history stack
    :param geometry: The mesh you want to check for a blendShape
    :type geometry: str
    """
    # check the history to see if there is a blendShape
    hist = mc.listHistory(geometry, pdo=True, il=2) or []
    hist = [node for node in hist if mc.nodeType(node) == "blendShape"]
    return hist

def getTargetIndex(bs, targetName):
    """
    Finds index for the target name.
    :param bs: blendShape
    :param targetName: target name to find index for
    :return: int
    """

    # If target name is an int, just return it
    if isinstance(targetName, (int, long)):
        return targetName

    targetCount = mc.blendShape(bs, q=1, target=1, wc=1)
    n = i = 0
    while n < targetCount:
        alias = mc.aliasAttr(bs + '.w[{}]'.format(i), q=1)
        if alias == targetName:
            return i
        if alias:
            n += 1
        i += 1


def getTargetName(bs, targetIndex):
    """
    Finds the name of a target from the index.
    :param bs:
    :param targetIndex:
    :return:
    """
    name = mc.aliasAttr(bs + '.w[{}]'.format(targetIndex), q=1)
    return name


def getTargetNames(bs):
    """
    Get all the target names for a blendshape
    :param bs:  blendShape
    :return: list
    """
    targetCount = mc.blendShape(bs, q=1, target=1, wc=1)
    targetNames = list()
    n = i = 0
    while n < targetCount:
        alias = mc.aliasAttr(bs + '.w[{}]'.format(i), q=1)
        if alias:
            targetNames.append(alias)
            n += 1
        i += 1
    return targetNames


def getTargetIds(bs):
    """
    Get all the target indices for a blendshape
    :param bs:  blendShape
    :return: list of ints
    """
    targetCount = mc.blendShape(bs, q=1, target=1, wc=1)
    targetIds = list()
    n = i = 0
    while n < targetCount:
        alias = mc.aliasAttr(bs + '.w[{}]'.format(i), q=1)
        if alias:
            targetIds.append(i)
            n += 1
        i += 1
    return targetIds


def getTargetDeltas(bs, target):
    """
    Get the delta values for the given target
    :param bs: BlendShape
    :param target: String name of target or the target's index
    :return: list of deltas, list of indices
    """
    # If string name is passed get the index
    targetIndex = getTargetIndex(bs, target)
    indexedAttr = bs+'.it[0].itg[{}].iti[6000]'.format(targetIndex)
    delta_list = mc.getAttr(indexedAttr+'.ipt') or []
    index_list = mc.getAttr(indexedAttr+'.ict') or []

    return delta_list, index_list


def setTargetDeltas(bs, deltas=None, indices=None, target=None):
    """
    Set deltas for a blendShape target
    :param bs: BlendShape node
    :param deltas: List of tuples. Each tuple contains 4 floats. [(1.0, 2.0, 3.0, 1.0)]
    :param indices: List of indices [0, 1, 3]
    :param target: String name of target or the target's index
    :return: None
    """

    if not deltas:
        return
    targetIndex = getTargetIndex(bs, target)
    indexedAttr = bs+'.it[0].itg[{}].iti[6000]'.format(targetIndex)
    deltas.insert(0, len(deltas))
    indices.insert(0, len(indices))
    mc.setAttr(indexedAttr+'.ict', *indices, type='componentList')
    mc.setAttr(indexedAttr+'.ipt', *deltas, type='pointArray')


def clearTargetDeltas(bs, target):
    """
    Clear any deltas set for target
    :param bs: BlendShape node
    :param target: String name of target or the target's index
    :return: None
    """
    setTargetDeltas(bs, [(0.1, 0.0, 0.0, 1.0)], ['vtx[0]'], target)

def getAllTargetDeltas(bs):
    """
    Convenience method for getting all target deltas
    :param bs: BlendShape node
    :return: list of deltas [(delta, indices), (deltas, indices)]
    """
    targets = getTargetNames(bs)
    all_deltas = list()
    for target in targets:
        deltas, indices = getTargetDeltas(bs, target)
        all_deltas.append((deltas, indices))
    return all_deltas


def setAllTargetDeltas(bs, deltas):
    """
    Convenience method for setting all target deltas
    :param bs: BlendShape node
    :param deltas: List of tuples. One tuple per target. [(deltas, indices)]
    :return: None
    """
    targets = getTargetNames(bs)
    for target, delta in zip(targets, deltas):
        setTargetDeltas(bs, delta[0], delta[1], target)


def setTargetWeight(bs, target, value):
    """
    Set target values by index
    :param bs: BlendShape node
    :param target: String name of target or the target's index
    :return: None
    """

    targetIndex = getTargetIndex(bs, target)
    mc.setAttr(bs+'.w[{}]'.format(targetIndex), value)

def getTargetWeight(bs, target):
    """
    Get target values by index
    :param bs: BlendShape node
    :param target: String name of target or the target's index
    :return: None
    """

    targetIndex = getTargetIndex(bs, target)
    return mc.getAttr(bs+'.w[{}]'.format(targetIndex))

def invertShape(bs, target, geo):

    melInvert = os.path.dirname(shape.__file__).replace('\\', '/') + '/invertShape.mel'
    mm.eval('source "' + melInvert + '"')

    # Indices of points with different positions of two meshes
    base = mc.deformer(bs, q=1, geometry=1)
    if not base:
        raise Exception("No geo associated with blendShape [ " + bs + " ] ")
        return
    else:
        base = mc.listRelatives(base, path=1, p=1)[0]

    if not getTargetIndex(bs, target):
        raise Exception(
            '[ ' + bs + ' ] missing target [ ' + target + ' ] The duplicate shape must be named the same as the blendShape target.')

    sel = mc.ls(sl=1)
    clearTargetDeltas(bs, target)

    indices = shape.getDeltaIndices(base, target)
    indicesStr = ['vtx[' + str(x) + ']' for x in indices]
    vertices = [geo + '.vtx[' + str(x) + ']' for x in indices]

    mc.select(vertices)
    cmd = 'absRelMovePolySel `ls -l -fl -sl` ' + base + ' ' + geo + ' .001'
    melDeltas = mm.eval(cmd)

    deltas = list()
    for d in melDeltas:
        x, y, z = d.split()
        deltas.append((float(x), float(y), float(z), 1.0))

    setTargetDeltas(bs, deltas, indicesStr, target)

    if sel:
        mc.select(sel)

