import rigrepo.libs.psd as psd
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
        interp = psd.getPoseInterp(interp)
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
    interps = [psd.getPoseInterp(x) for x in interps]
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
    bs = psd.getDeformer(interp)
    blendShape.invertShape(bs, target, geo[0])

