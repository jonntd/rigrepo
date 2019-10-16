from PySide2 import QtGui, QtCore, QtWidgets, QtOpenGL
import sys
import os
# graphics classes that will deal with drawing QGraphicsScene, QGraphicsView, QGraphicsItem

class GraphicsView(QtWidgets.QGraphicsView):
    '''
    This is the base abstract class to be used for modifying the way the 
    view functions.

    .. note:: 
        This is currently temporary. We will have to update this later when we 
        decide how we're going to use it.
    '''
    def __init__(self):
        '''
        The constructor for the GraphicsView class.
        '''
        # currently we will just call the parent class contructor.
        super(GraphicsView, self).__init__()

        # set the defualt panning and scale
        self._panSpeed = 1
        self._scale = 1

        # turn off the scroll bars
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def mouseMoveEvent(self, event):
        '''
        This will track the movement of the cursor when moving the mouse after press
        '''
        if event.buttons() == QtCore.Qt.MiddleButton:
            if QtCore.Qt.AltModifier == QtWidgets.QApplication.keyboardModifiers():
                mouseDelta = QtCore.QPointF(self.mapToScene(event.pos()) - self.mapToScene(self._lastMousePos))
                self.pan(mouseDelta)
                self._lastMousePos = event.pos()
        if event.buttons() == QtCore.Qt.RightButton:
            if QtCore.Qt.AltModifier == QtWidgets.QApplication.keyboardModifiers():
                mouseDelta = QtCore.QPointF(self.mapToScene(event.pos()) - self.mapToScene(self._lastMousePos))
                if mouseDelta.x() > 0:
                    self.scale(1.01, 1.01)
                    self._scale *= 1.01
                else:
                    self.scale(0.99, 0.99)
                    self._scale *= 0.99
                self._lastMousePos = event.pos()

        super(GraphicsView, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        '''
        '''
        self._lastMousePos = event.pos()
                

        super(GraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        '''
        '''
        super(GraphicsView, self).mouseReleaseEvent(event)


    def wheelEvent(self, event):
        '''
        This will handle wheel events and make sure it scales the scene.
        '''
        # check to make sure the delta is less than zero and we can scale up.
        # otherwise we scale down
        if event.delta() > 0:
            self.scale(1.1, 1.1)
            self._scale *= 1.1
        else:
            self.scale(0.9, 0.9)
            self._scale *= 0.9

    def pan(self, delta):
        # Scale the pan amount by the current zoom.
        #delta *= self._scale
        delta *= self._panSpeed

        # Have panning be anchored from the mouse.
        self.setTransformationAnchor(self.AnchorUnderMouse)
        newCenter = QtCore.QPoint(self.width() / 2 - delta.x(),  self.height() / 2 - delta.y())
        self.centerOn(self.mapToScene(newCenter))

        # For zooming to anchor from the view center.
        self.setTransformationAnchor(self.AnchorViewCenter)

class GraphicsScene(QtWidgets.QGraphicsScene):
    '''
    This is the base abstract class to be used for modifying the way the 
    scene functions.

    .. note:: 
        This is currently temporary. We will have to update this later when we 
        decide how we're going to use it.
    '''
    def __init__(self):
        '''
        The constructor for the GraphicsScene class.
        '''
        # currently we will just call the parent class contructor.
        super(GraphicsScene,self).__init__()

class PolygonItem(QtWidgets.QGraphicsItem):
    '''
    This is the abstract item class that will be used for all buttons in the picker page.
    '''
    def __init__(self,name, polygon=QtGui.QPolygonF(), color=QtGui.QColor(0, 0, 255, 255)):
        '''
        This constructor will hadnle setting the name, color, and polygon for this item

        :param name: The name of the button
        :type name: str

        :param polygon: This will use a QPolygonF to contruct the polygon
        :type polygon: QPolygonF

        :param color: The color in RGBa values 
        :type color: QColor
        '''
        super(PolygonItem,self).__init__()
        self.name = name
        self.color = QtGui.QColor(color)
        self.polygon = QtGui.QPolygonF(polygon)
        self.setFlags(self.ItemIsSelectable)

    def hoverEnterEvent(self, event):
        '''
        This is the hoverEvent that will handle when the item has the
        cursor enter it.
        '''
        print "we have entered the polygon"
        #self.setOpacity(.8)

    def mousePressEvent(self,event):
        '''
        Event handling method for when the mouse is pressed on the item.
        '''
        #print "pressing the {}".format(self.name)
        self.setOpacity(.6)
        super(PolygonItem, self).mousePressEvent(event)


    def mouseReleaseEvent(self,event):
        '''
        Event handling method for when the mouse is released from the item.
        '''
        super(PolygonItem, self).mouseReleaseEvent(event)
        self.execute()
        #print "releasing the {}".format(self.name)
        self.setOpacity(1.0)

    def boundingRect(self):
        '''
        Sets the bounding rect for this item.

        .. note::
            Currently this is being used the mouseEvent are checking if it's
            over the item or not. We should look into making it check the polygon.
        '''
        return self.polygon.boundingRect()
        
    def paint(self, painter, options, widget=None):
        '''
        This is where we will do the drawing.
        '''
        # set the painter to not use a pen
        painter.setPen(QtCore.Qt.NoPen)
        # create the brush and set it's color to the item color.
        brush = QtGui.QBrush(self.color)
        painter.setBrush(brush)
        # draw the polygon using the polygon passed into the item
        painter.drawPolygon(self.polygon.toPolygon())

    def execute(self):
        '''
        This is here as an abstract method.
        '''
        pass

class EllipseItem(PolygonItem):
    '''
    This is the abstract item class that will be used for all buttons in the picker page.
    '''
    def paint(self, painter, options, widget=None):
        '''
        This is where we will do the drawing.
        '''
        # set the painter to not use a pen
        painter.setPen(QtCore.Qt.NoPen)
        # create the brush and set it's color to the item color.
        brush = QtGui.QBrush(self.color)
        painter.setBrush(brush)
        # draw the polygon using the polygon passed into the item
        painter.drawEllipse(self.boundingRect)
