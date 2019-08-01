"""
This module is for dealing with wraps inside Maya
"""
import maya.cmds as mc
import maya.mel as mm
import rigrepo.libs.common

def transferWrap(source, target, deformer):
    """
    This will transfer wrap from one mesh to another. If the target doesn't have a
    wrap on it, it will create a new wrap. Then once there is a wrap
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

    # make sure we have a wrap on the source mesh
    sourceWraps = getWraps(source)
    wrapList = list()
    if deformer not in sourceWraps:
        mc.warning('The source mesh "{}" is missing "{}"'.format(source, deformer))
        return

    # Loop through target meshes
    for targetMesh in targetMeshList:
        if not mc.objExists(targetMesh):
            mc.warning('The target mesh "{}" does not exist in the current Maya session.'.format(target))
            continue

        # check to see if there is a wrap already  on the target mesh
        hist = getWraps(targetMesh)
        if deformer in hist:
            mc.warning('The target mesh "{}" is being deformed by "{}", aborting.'.format(targetMesh, deformer))
            continue

        name = "{}_bs".format(targetMesh)
        # Build wrap
        target_bs = mc.wrap(targetMesh, n=deformer)[0]
        targets = getTargetNames(deformer)
        for target in targets:
            addTarget(target_bs, name=target)

        print('source', source, 'target', targetMesh)
        print('targets', targets)
        #wrapList.append(hist[0])

    return wrapList

def createWrap(sourceGeo, targetGeo, exclusiveBind=0):
    """
    Create wrap deformer

    Main call from
    C:/Program Files/Autodesk/Maya2018/scripts/others/performCreateWrap.mel

    :param sourceGeo: The geo that is being controlled by the wrap
    :param targetGeo: The geo that is being wrapped to.
    :param exclusiveBind: Only bind to closest points, fastest option.
    :return:
    """
    sel = mc.ls(sl=1)
    mc.select(sourceGeo, targetGeo)
    cmd = 'doWrapArgList "7" {{ "1","0","1", "2", "{}", "1", "0", "0" }}'.format(exclusiveBind)
    wrap = mm.eval(cmd)[0]
    if sel:
        mc.select(sel)

    return wrap

def getWraps(geometry):
    """
    This will check the geometry to see if it has a wrap in it's history stack

    :param geometry: The mesh you want to check for a wrap
    :type geometry: str
    """
    # check the history to see if there is a wrap
    hist = mc.listHistory(geometry, pdo=True, il=2) or []
    hist = [node for node in hist if mc.nodeType(node) == "wrap"]
    return hist

def addTarget(wrap, targetName):
    pass

def getTargetIndex(wrap, targetName):
    pass

def getTargetName(wrap, targetIndex):
    pass

def getTargetNames(wrap):
    pass

def getTargetIds(wrap):
    pass
