'''
This module is used for the picker page interface's.

.. warning::
    This is very rough pass and will be volatile for a while until we figure it out
'''
from PySide2 import QtGui, QtCore, QtWidgets, QtOpenGL
import rigrepo.libs.data.picker_data as picker_data
import rigrepo.ui.graphicsWidgets as graphicsWidgets
import maya.cmds as mc
import maya.api.OpenMaya as om
import sys
import os
from collections import OrderedDict
import json
import getpass
from time import gmtime, strftime

# graphics classes that will deal with drawing QGraphicsScene, QGraphicsView, QGraphicsItem
class GraphicsWidget(QtWidgets.QWidget):
    '''
    This is the widget that stores the QGraphicsScene, QGraphicsView.
    '''
    def __init__(self, filepath, parent=None):
        '''
        This is the constructor for the main widget
        '''
        super(GraphicsWidget,self).__init__(parent)

        # create the layout.
        mainLayout = QtWidgets.QVBoxLayout()

        self.setMinimumSize(350,350)
        self.resize(800,800)
        self.scene = graphicsWidgets.GraphicsScene()
        self.view = graphicsWidgets.GraphicsView()
        self.view.setScene(self.scene)
        self.scene.setSceneRect(0,0,800,800)
        self.view.setViewport(QtOpenGL.QGLWidget())
        mainLayout.addWidget(self.view)
        self.setLayout(mainLayout)
        pickerData = picker_data.PickerData(self.scene)
        pickerData.read(filepath)
        pickerData.applyData(pickerData.getData().keys())
        self.view.fitInView(self.scene.itemsBoundingRect(),QtCore.Qt.KeepAspectRatio)

# maya specific classes will have to be moved out of this file.
# these classes are going to be used to have Maya callbacks and command
class SelectButtonItem(graphicsWidgets.PolygonItem):
    '''
    This class should extend the PolygonItem class and do all of the 
    selecting of items if they happen to exists
    '''
    # Store a static variable for the type of button we're using
    buttonType = "select"
    def __init__(self, name, polygon, color, selectableItems=list()):
        '''
        The constructor for the SelectButtonItem class.
        '''
        super(SelectButtonItem, self).__init__(name, polygon, color)

        self._selectableItems = selectableItems

    def mouseReleaseEvent(self,event):
        '''
        We might want to have this override how the opacity switching is happening.
        We want to keep it on if something is selected in the scene. Turn is back
        to default if nothing is selected anymore
        '''
        if event.buttons() == QtCore.Qt.LeftButton:
            selectableItems = self.execute()
        super(SelectButtonItem, self).mouseReleaseEvent(event)

    def execute(self):
        '''
        This will select the items in the selectable item list if they 
        exist in your scene
        '''
        selectableItems = mc.ls(self._selectableItems,o=True,ni=True)

        # if shift is held down, we will toggle the selection of the items
        if QtCore.Qt.ShiftModifier == QtWidgets.QApplication.keyboardModifiers():
        	mc.select(selectableItems, tgl=True)
        # if control is held down, we will remove the items from the selection
        elif QtCore.Qt.ControlModifier == QtWidgets.QApplication.keyboardModifiers():
        	mc.select(selectableItems, d=True)
        # if no modifiers are held down, we will just replace the selection.
        else:
        	mc.select(selectableItems, r=True)
        return selectableItems

class CommandButtonItem(graphicsWidgets.PolygonItem):
    buttonType = "command"
    def __init__(self, name, polygon, color, command=str()):
        '''
        This class should extend the PolygonItem class and do all of the 
        selecting of items if they happen to exists
        '''
        super(CommandButtonItem, self).__init__(name, polygon, color)

        self._cmd = command

    def execute(self):
        '''
        When button is clicked, the command for the button will be ran
        '''
        exec(self._cmd)