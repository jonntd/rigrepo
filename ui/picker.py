'''
This module is used for the picker page interface's.

.. warning::
    This is very rough pass and will be volatile for a while until we figure it out
'''
from PySide2 import QtCore, QtWidgets, QtOpenGL
import rigrepo.libs.data.picker_data as picker_data
import rigrepo.ui.graphicsWidgets as graphicsWidgets

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