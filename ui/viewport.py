'''
Functions for working with Maya's viewport
'''

try:
    from Qt import QtWidgets, QtGui, QtCore
except:
    from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui2

hoverFilterInstalled = False
hoverFilter = None

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
    relpos = getCursorPos()

    obj = mc.hitTest(panel, relpos[0], relpos[1])
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
    faceId = intersection[2]
    if intersection:
        x = hitpoint.x
        y = hitpoint.y
        z = hitpoint.z
        return x, y, z, faceId
    else:
        return None

class viewportEventFilter(QtCore.QObject):
    '''
    Used for intercepting top level events in the viewport/maya
    '''
    def __init__(self):
        QtCore.QObject.__init__(self)
        print('viewport event filter initialized')
        self.menu = None
        self.mouse_button = QtCore.Qt.RightButton
        self.installed = False
        self.active = False

    def setMouseButton(self, button):
        '''
        Specifies which mouse button the event filter should look for.
        :param button: [QtCore.Qt.LeftButton, QtCore.Qt.MiddleButton, QtCore.Qt.RightButton]
                       defaults to right button.
        '''
        self.mouse_button = button

    def eventFilter(self, obj, event):
        '''
        Standard event filter installed on the qApp.
        :param obj:
        :param event:
        :return:
        '''
        if self.active:
            pressEvents = [QtCore.QEvent.MouseMove]
            if event.type() in pressEvents:
                testIt()
        # standard event processing
        return QtCore.QObject.eventFilter(self, obj, event)

def startHoverFilter():
    global hoverFilterInstalled
    global hoverFilter
    if not hoverFilterInstalled:
        # Build the filter object
        hoverFilter = viewportEventFilter()

        # Get the main maya app instance
        q_app = QtWidgets.QApplication.instance()
        q_app.installEventFilter(hoverFilter)

        # Track that it is installed
        hoverFilterInstalled = True
        print('-'*100)
        print('Hover Filter installed')
        print('-'*100)
    hoverFilter.active = True

def stopHoverFilter():
    hoverFilter.active = False

def deleteHoverFilter():
    hoverFilter.active = False

def testIt():
    '''

    Test, find point on mesh from clicking on mesh
    :return:
    '''
    cursorPos = getCursorPos()
    if cursorPos:
        pos, dir = viewToWorld(*cursorPos)
        obj = getObjUnderCursor()
        if obj:
            intersectPos = rayIntersect(pos, dir, obj[0])
            faceId = intersectPos[3]
            if intersectPos:
                if obj:
                    mc.select(obj[0]+'.f[{}]'.format(faceId))
