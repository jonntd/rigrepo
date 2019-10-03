'''
Functions for working with Maya's viewport
'''

from PySide2 import QtGui, QtWidgets
import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui2

def getCursorPos():
    pos = QtGui.QCursor.pos()
    widget = QtWidgets.QApplication.widgetAt(pos)
    relpos = widget.mapFromGlobal(pos)
    height = widget.height()
    panel = mc.getPanel(underPointer=True) or ""

    if not "modelPanel" in panel:
        return

    return (relpos.x(), height-relpos.y())

def getObjUnderCursor():
    panel = mc.getPanel(underPointer=True) or ""
    print('panel', panel)
    relpos = getCursorPos()

    obj = mc.hitTest(panel, relpos[0], relpos[1])
    print(obj)
    return obj

def viewToWorld(screenX, screenY):
    worldPos = om.MPoint() # out variable
    worldDir = om.MVector() # out variable

    activeView = omui2.M3dView().active3dView()
    activeView.viewToWorld(int(screenX), int(screenY), worldPos, worldDir)

    return worldPos, worldDir

def rayIntersect(pos, dir, mesh):

    pos2 = om.MFloatPoint(pos.x, pos.y, pos.z)
    dir  = om.MFloatVector(dir.x, dir.y, dir.z)

    selectionList = om.MSelectionList()
    selectionList.add(mesh)
    dagPath = om.MDagPath()
    sel = selectionList.getDagPath(0)
    fnMesh = om.MFnMesh(sel)

    intersection = fnMesh.closestIntersection(pos2,
                                              dir,
                                              om.MSpace.kWorld,
                                              9999,
                                              False)
    hitpoint = intersection[0]
    if intersection:
        x = hitpoint.x
        y = hitpoint.y
        z = hitpoint.z
        return x, y, z
    else:
        return None

def testIt():
    '''

    Test, find point on mesh from clicking on mesh
    :return:
    '''
    mesh = 'pSphereShape1'
    cursorPos = getCursorPos()
    if cursorPos:
        pos, dir = viewToWorld(*cursorPos)
        obj = getObjUnderCursor()
        if obj:
            intersectPos = rayIntersect(pos, dir, obj[0])
            print('obj', obj)
            if intersectPos:
                print(intersectPos)
                if obj:
                    print("HIT")
                    mc.spaceLocator(p=intersectPos)

'''
mesh = 'pSphereShape1'
cursorPos = getCursorPos()
if cursorPos:
    pos, dir = viewToWorld(*cursorPos)
    print(pos, dir)
    rayIntersect(pos, dir, mesh)
    #print(w[0].x, w[0].y, w[0].z)
    #mc.spaceLocator(p=[w[0].x, w[0].y, w[0].z])
'''
