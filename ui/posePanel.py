import rigrepo.libs.psd
import rigrepo.libs.common
import rigrepo.libs.blendShape as blendShape
import maya.cmds as mc
import maya.mel as mm

def getSelectedPoses():
    """
    Gets the poses selected in the Pose Editor
    :return: List of tuples [(interp, pose), ...]
    """

    # Poses
    poses = list()
    poseConnections = mm.eval('getPoseEditorTreeviewSelection(2)')
    for poseConnection in poseConnections:
        interp, index = poseConnection.split('.')
        interp = rigrepo.libs.psd.getInterp(interp)
        if index:
            pose = mc.getAttr(interp+'.pose['+str(index)+'].poseName')
            if pose:
                poses.append((interp, pose))
    return poses

def getSelectedInterps():
    """
    Get the selected interpolators from the Pose Editor
    :return: List of interpolators
    """

    interps = mm.eval('getPoseEditorTreeviewSelection(1)')
    interps = [rigrepo.libs.psd.getInterp(x) for x in interps]
    return interps

def getPoseEditorWidget():
    """
    For getting the qt widget of the Pose Editor.
    MEL file that handles building and showing the editor.
    C:\Program Files\Autodesk\Maya2018\scripts\others\createPosePanelMenu.mel
    :return:
    """
    panelName = 'posePanel1'
    poseEditorPanel = mc.panel(panelName, q=1, control=1)

def overridePerformUpdatePoseShape():
    """
    Overriding mel file:
    C:\Program Files\Autodesk\Maya2018\scripts\others\performUpdatePoseShape.mel
    :return:
    """
    cmd  = 'import rigrepo.ui.posePanel as pp; '
    cmd += 'pp.performUpdatePoseShape();'
    evalCmd ='global proc performUpdatePoseShape(string $_t1, string $_t2, string $_t3){\npython("'+cmd+'");}'
    print(evalCmd)
    mm.eval(evalCmd)

def performUpdatePoseShape():
    """
    Applies the selected geo to the selected pose in the posePanel
    :return:
    """
    selTargets = getSelectedPoses()
    if not selTargets:
        raise Exception('Please select a pose.')

    interp, target = selTargets[0]
    geo = mc.ls(sl=1)
    if not geo:
        raise Exception('Please select a mesh to apply.')

    bs = rigrepo.libs.psd.getDeformer(interp)

    # Mirror - If this is a left right pose we need to turn off the other side
    #          when inverting.
    mirrorInterp = rigrepo.libs.common.getMirrorName(interp)
    doMirror = False
    if mirrorInterp != interp:
        mirrorTarget = rigrepo.libs.common.getMirrorName(target)
        if mirrorTarget != target:
            if mc.objExists(mirrorInterp):
                mirrorTargetIndex = rigrepo.libs.psd.getPoseIndex(mirrorInterp, mirrorTarget)
                if mirrorTargetIndex:
                    doMirror = True

    if doMirror:
        print('*'*100)
        print('MIRROR APPLY')

        # Go to pose
        rigrepo.libs.psd.goToPose(interp, target)
        rigrepo.libs.psd.goToPose(mirrorInterp, mirrorTarget)

        # SIDE 1
        #
        # Disable other side
        rigrepo.libs.psd.disablePose(mirrorInterp, mirrorTarget)
        # Invert
        blendShape.invertShape(bs, target, geo[0])
        # Enable other side
        rigrepo.libs.psd.enablePose(mirrorInterp, mirrorTarget)

        # SIDE 2
        #
        # Disable other side
        rigrepo.libs.psd.disablePose(interp, target)
        # Invert
        blendShape.invertShape(bs, mirrorTarget, geo[0])
        # Enable other side
        rigrepo.libs.psd.enablePose(interp, target)

    else:
        # Got to pose
        rigrepo.libs.psd.goToPose(interp, target)
        # Invert
        blendShape.invertShape(bs, target, geo[0])

