import sys
import traceback
import math
from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

class RadialMenuItem_(QtWidgets.QLabel):
    def __init__(self, position=None):
        QtWidgets.QLabel.__init__(self)
        self.position = position
        self.setAlignment(QtCore.Qt.AlignCenter)

    def connect(self, function):
        self.function = function

class StopHoverEvent(QtCore.QObject):
    def eventFilter(self, obj, event):
        hoverEvents = [QtCore.QEvent.HoverLeave,
                       QtCore.QEvent.HoverEnter,
                       QtCore.QEvent.GraphicsSceneHoverEnter,
                       QtCore.QEvent.GraphicsSceneHoverLeave,
                       QtCore.QEvent.GraphicsSceneHoverMove,
                       QtCore.QEvent.HoverMove]
        if event.type() in hoverEvents:
            #print "Ate hover enter"
            return False
        else:
            return QtCore.QObject.eventFilter(self, obj, event)

class RadialMenuItem(QtWidgets.QPushButton):
    def __init__(self, position=None):
        QtWidgets.QPushButton.__init__(self)
        self.position = position
        #self.setWidnowFlags = QtCore.Qt.WA_Hover
        #stopHoverEvent = StopHoverEvent(self)
        #self.installEventFilter(stopHoverEvent)

    def connect(self, function):
        self.function = function

    #def enterEvent(self, event):
    #    pass
    #def leaveEvent(self, event):
    #    pass

    #def event(self, e):
    #    if e.type() not in (127, 128, 129):
    #        print e.type()
    #        return super(RadialMenuItem, self).event(e)
    #    return False

    #def event(self, event):
    #    hoverEvents = [QtCore.QEvent.HoverLeave,
    #                   QtCore.QEvent.HoverEnter,
    #                   QtCore.QEvent.HoverMove]
    #    if event.type() in hoverEvents:
    #        print('pos', event.pos())
    #    else:
    #        QtWidgets.QPushButton.event(self, event)
    #    return(True)

class RadialMenu(QtWidgets.QMenu):
    def __init__(self, items=None):
        QtWidgets.QMenu.__init__(self)
        self.startPos = QtCore.QPoint(0,0)
        self.width    = 1000
        self.height   = 500
        self.cnRadius = 8
        self.rightClickWidgetMousePressEvent = None
        
        # Returns true if a an existing qt loop is running
        activeWindow =  QtWidgets.QApplication.activeWindow()

        self.setFixedSize(self.width, self.height)
        self.maskPixmap = QtGui.QPixmap(self.width, self.height)
        # Stores which position is active
        self.activeItem = None

        # Pens
        gray = QtGui.QColor(128, 128, 128, 255)
        self.penOrigin      = QtGui.QPen(gray,             5,  QtCore.Qt.SolidLine)
        self.penCursorLine  = QtGui.QPen(gray,             3,  QtCore.Qt.SolidLine)
        self.penBlack       = QtGui.QPen(QtCore.Qt.black,  2,  QtCore.Qt.SolidLine)
        self.penActive      = QtGui.QPen(QtCore.Qt.red,    20, QtCore.Qt.SolidLine)
        self.penWhite       = QtGui.QPen(QtCore.Qt.white,  5,  QtCore.Qt.SolidLine)

        # Color - Query the default background and highlight colors.
        #         Note: For native QT, the color for push buttons is the midlight color group 
        #               For native maya, it is the light color group 
        c = self.palette().light().color().getRgb()
        t = self.palette().buttonText().color().getRgb()
        h = self.palette().highlight().color().getRgb()

        tempButton = QtWidgets.QPushButton()
        self.itemStyleSheetDefault   =  ('background-color:rgb({0},{1},{2});'
                                                    'color:rgb({3},{4},{5});'.format(c[0], c[1], c[2], t[0], t[1], t[2]))
        self.itemStyleSheetHighlight =  ('background-color:rgb({0},{1},{2});'
                                                    'color:rgb({3},{4},{5});'.format(h[0], h[1], h[2], t[0], t[1], t[2]))
        # menu items
        self.itemHeight = 38
        self.itemWidgets = dict()
        # Ordered items from 0 degrees to 360 degrees
        self.itemsOrdered = ['E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE']
        self.items=    {'N':  [   0, - 90],
                        'S':  [   0,   90],
                        'E':  [ 120,    0],
                        'W':  [-120,    0],
                        'NE': [  85,  -45],
                        'NW': [ -85,  -45],
                        'SE': [  85,   45],
                        'SW': [ -85,   45]}
        # Angles - Each number = 22.5 degree slice, so each position gets a
        #          45 degree slice of the pie
        self.angles=   {'E':  [15,  0],
                        'SE': [ 1,  2],
                        'S':  [ 3,  4],
                        'SW': [ 5,  6],
                        'W':  [ 7,  8],
                        'NW': [ 9, 10],
                        'N':  [11, 12],
                        'NE': [13, 14]}
        self.itemWidth = dict()

        anglesUsed = list()
        for item in items:
            pos = item.position
            item.setParent(self)
            # Calculate the width of the text
            font = item.property('font')
            fm = QtGui.QFontMetrics(font)
            itemWidth = fm.width(item.text()) + 80

            # Offset the positions because the buttons are drawn from the top left corner
            if 'W' in pos:
                self.items[pos][0] -= itemWidth
                self.items[pos][1] -= self.itemHeight * .5
            if 'E' in pos:
                self.items[pos][1] -= self.itemHeight * .5
            if 'N' == pos:
                self.items[pos][0] -= itemWidth * .5
                self.items[pos][1] -= self.itemHeight
            if 'S' == pos:
                self.items[pos][0] -= itemWidth * .5
            if 'NE' == pos or 'NW' == pos:
                self.items[pos][1] -= 20
            if 'SE' == pos or 'SW' == pos:
                self.items[pos][1] += 20
            self.itemWidgets[pos] = item
            self.itemWidth[pos] = itemWidth
            #item.setStyleSheet(self.itemStyleSheetDefault)
            anglesUsed += self.angles[pos]

        # If some locations are not being used
        # This loop will give thier slices to the next closest existing location.
        # So the mouse will always active at least one location at all times.
        x = 0
        while len(anglesUsed) < 16:
            for item in items:
                x += 1
                pos = item.position
                n = self.pieLast(self.angles[pos][0])
                l = self.pieNext(self.angles[pos][-1])
                if not n in anglesUsed:
                    self.angles[pos] = [n]+self.angles[pos]
                    anglesUsed.append(n)
                if not l in anglesUsed:
                    self.angles[pos].append(l)
                    anglesUsed.append(l)
            if x > 150:
                print('safety break')
                break
        # Draw the windows
        self.drawItems()

    def pieNext(self, value, max=15):
        if value == max:
            return(0)
        else:
            value+=1
            return(value)

    def pieLast(self, value, max=15):
        if value == 0:
            return(max)
        else:
            value-=1
            return(value)

    def paintEvent(self, event):
        # Using try statement to capture the traceback errors, no errors were printing
        # sometimes without out it.
        try:
            # init painter - QPainter does not work outside this method
            self.painter = QtGui.QPainter(self)
            pos = self.mapFromParent(QtGui.QCursor.pos())
            cnPos = QtCore.QPoint(self.width*.5,
                                  self.height*.5)

            # Cursor line
            self.painter.setPen(self.penCursorLine)
            self.painter.drawLine(cnPos, pos)
            # Origin circle - black outline
            offset = 2
            self.painter.setPen(self.penOrigin)
            self.painter.drawArc((self.width *.5)-self.cnRadius*.5,
                                 (self.height*.5)-self.cnRadius*.5,
                                  self.cnRadius,  self.cnRadius, 16, (360*16))
            # Origin circle - gray center
            self.painter.setPen(self.penBlack)
            self.painter.drawArc( (self.width *.5)-((self.cnRadius+offset) *.5),
                                  (self.height*.5)-((self.cnRadius+offset) *.5),
                                   self.cnRadius+offset, self.cnRadius+offset, 16, (360*16))
            self.painter.end()
        except:
            traceback.print_exc()

    def mouseMoveEvent(self, event):
        self.livePos = QtGui.QCursor.pos()
        length       = math.hypot(self.startPosCn.x() - self.livePos.x(),self.startPosCn.y() - self.livePos.y())
        angle        = self.angleFromPoints([self.startPosCn.x(), self.startPosCn.y()], [self.livePos.x(), self.livePos.y()])
        angle        = int(angle/22.5)
        # Highlight items
        self.activeItem = None
        for position in self.items:
            if not position in self.itemWidgets:
                continue
            item = self.itemWidgets[position]
            #item.setStyleSheet(self.itemStyleSheetDefault)
            # Highlight item if we are in its slice
            if length > 20:
                if angle in self.angles[position]:
                    #item.setStyleSheet(self.itemStyleSheetHighlight)
                    #hoverEvent = QtGui.QHoverEvent(QtCore.QEvent.HoverEnter, QtCore.QPointF(), QtCore.QPointF())
                    hoverEvent = QtGui.QHoverEvent(QtCore.QEvent.HoverEnter, QtCore.QPointF(1,1), QtCore.QPointF(0,0))
                    hoverMove = QtGui.QHoverEvent(QtCore.QEvent.HoverMove, QtCore.QPointF(1,1), QtCore.QPointF(0,0))
                    item.event(hoverEvent)
                    item.event(hoverMove)
                    self.activeItem = item
            # Highlight button if the mouse is over it, overrides slice highlight
            #if item.underMouse():
            #    if self.activeItem:
            #        self.activeItem.setStyleSheet(self.itemStyleSheetDefault)
            #    self.activeItem = item
            #    item.setStyleSheet(self.itemStyleSheetHighlight)
                
        # Call paint event
        self.update()

    def mouseReleaseEvent(self, event):
        self.hide()
        for position in self.items:
            if not position in self.itemWidgets:
                continue
            item = self.itemWidgets[position]
            #item.setStyleSheet(self.itemStyleSheetDefault)
        # Run items function if it exists
        if self.activeItem:
            if self.activeItem.function:
                self.activeItem.function()
        self.activeItem = None

    def popup(self, pos=None):
        self.startPosCn = pos
        self.startPos   = QtCore.QPoint(self.startPosCn.x()+(self.width*.5),
                                      self.startPosCn.y()+(self.height*.5))
        # Window
        rect = QtCore.QRect(self.startPos.x()-self.width,
                            self.startPos.y()-self.height,
                            self.width,
                            self.height)
        self.setGeometry(rect)
        self.show()

    def rightClickConnect(self, widget=None):
        self.rightClickWidgetMousePressEvent = widget.mousePressEvent
        widget.mousePressEvent = self.rightClickPopup

    def rightClickPopup(self, event):
        if event.buttons() != QtCore.Qt.RightButton:
            self.rightClickWidgetMousePressEvent(event)
            return()
        self.popup(QtGui.QCursor.pos())

    def drawItems(self):
        # Mask
        self.maskPixmap.fill(QtCore.Qt.white)
        self.painterMask = QtGui.QPainter()
        self.painterMask.begin(self.maskPixmap)

        # Items
        for position in self.items:
            if not position in self.itemWidgets:
                continue
            pos  = self.items[position]
            item = self.itemWidgets[position]
            # Solid rectangle
            rect = QtCore.QRect(pos[0]+self.width *.5,
                                pos[1]+self.height*.5,
                                self.itemWidth[position],
                                self.itemHeight)
            self.painterMask.fillRect(rect, QtCore.Qt.black)
            item.setGeometry(rect)

        # Center background cicle - Where the origin dot and line are drawn
        self.painterMask.setBrush(QtCore.Qt.black)
        offset = 30
        self.painterMask.drawEllipse((self.width*.5) -((self.cnRadius+offset)*.5),
                                    ( self.height*.5)-((self.cnRadius+offset)*.5),
                                      self.cnRadius+offset, self.cnRadius+offset)
        self.painterMask.end()
        self.setMask(self.maskPixmap.createMaskFromColor(QtCore.Qt.white))

    def angleFromPoints(self, p1=None, p2=None):
        # X axis to the right is 0 Degrees
        # Y axis up is 90 degrees
        radians = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
        degrees = math.degrees(radians)
        if(degrees < 0.0):
            degrees += 360.0
        return(degrees)

