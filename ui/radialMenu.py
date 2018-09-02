import sys
import traceback
import math
from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools
import timeit

'''
TODO
- Icons for items
- Option boxes for items
- Sub menus

'''

class RadialMenuItem(QtWidgets.QPushButton):
    def __init__(self, position=None, text=None):
        QtWidgets.QPushButton.__init__(self)
        self.position = position
        self.screenRatio, self.screenFontRatio = getScreenRatio()
        # Stop mouse events from affecting radial widgets
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        if text:
            self.setText(text)

        # Style
        h = self.palette().highlight().color().getRgb()
        c = self.palette().light().color().getRgb()
        if self.screenRatio < 1.0:
            b = 1.0
        else:
            b = 2.0
        if position:
            style =  """RadialMenuItem:hover{{
                            background-color:rgb({hr},{hg},{hb});
                            border: {border}px solid black
                        }}
                        RadialMenuItem{{
                            background-color:rgb({cr},{cg},{cb});
                            border: {border}px solid black 
                        }}
                     """.format(hr=h[0], hg=h[1], hb=h[2], cr=c[0], cg=c[1], cb=c[2], border=b )
        else:
            style =  """RadialMenuItem:hover{{
                            background-color:rgb({},{},{});
                        }}
                        RadialMenuItem{{
                            background-color:rgb({},{},{});
                            Text-align:left;
                            padding-left: 20px
                        }}
                     """.format(h[0], h[1], h[2], c[0], c[1], c[2] )
        self.setStyleSheet(style)
        self.checkBox = None
        self.function = None

    def connect(self, function):
        self.function = function

    def setCheckable(self, state):
        # ON
        rf = self.screenFontRatio
        r = self.screenRatio
        if state:
            if self.checkBox:
                # checkBox already exists, just show it
                self.checkBox.show()
                return
            box = QtWidgets.QCheckBox(self)
            rect = QtCore.QRect(10*rf,7*rf,25*r, 25*r)
            box.setGeometry(rect)
            box.setChecked(True)
            self.checkBox = box
        # OFF 
        else:
            if self.checkBox:
                self.checkBox.hide()

class RadialMenu(QtWidgets.QMenu):
    '''
    Glossary
        item ----- A child widget which is displayed either in a cardinal
                   position or in a standard column menu.

        position - The 8 avialable cardinal directions that an item can
                   occupy. ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE]

        slice ---- One of the 16 divisions of the pie. Each slice is
                   22.5 degrees of the pie. As the cursor moves the menu
                   tracks what slice it is in. The slice is traced to 
                   its position and the position traces to its item. 

                   cursor(x,y)-->angle-->slice-->position-->item

                   A position is assocaited with two slices so its slices
                   can be given to its neighboring positions when the 
                   position is not in use (No item has mapped it). 
                   
                   For example, if only one item in the menu has has 
                   declared its position, it will eat up all the slices.
                   So no matter where the cursor is it will activate that
                   item.

    Data structure
        self.items    - contains the RaidialMenuItems that have been 
                        added to the menu.
        item.position - The position associated with item. If None the 
                        item will display in the column menu. 
        item.x        - The x and y coordinate of the top left corner
        item.y          of the item widget. This is assigned in the
                        addItem method.
    Item sizing
        item.width  - The setText method of the RadialItem calculates
                      the width of the text plus margins and assigns
                      it to item.width.
        item.height - The height does not need to change per item
                      so it is statically set in the __init__ of the
                      RadialItem.
    '''
    def __init__(self, items=None):
        '''
        Base custom QMenu
        '''
        QtWidgets.QMenu.__init__(self)

        # Window
        self.transparent = False 
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.NoDropShadowWindowHint)
        if self.transparent:
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Ratio for different screen sizes
        self.screenRatio, self.screenFontRatio = getScreenRatio()
        # Dimensions
        self.width    = 1000 * self.screenRatio
        self.height   = 2000 * self.screenRatio

        self.setFixedSize(self.width, self.height)

        # Timer for gestures
        self.timer = QtCore.QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.trackCursor)
        self.timer.setInterval(2)

        # Turns off when the cursor stops moving
        self.gesture = True

        # Main painter
        self.painter = QtGui.QPainter()
        # Mask painter
        self.painterMask = QtGui.QPainter()
        self.maskPixmap = QtGui.QPixmap(self.width, self.height)
        self.maskPixmap.fill(QtCore.Qt.white)
        # Radius of origin circle
        self.originRadius = 8.0 * self.screenRatio
        # Right click widget - Stores the mouse press event of the widget 
        #                      the menu is opened from when right clicked
        self.rightClickWidgetMousePressEvent = None
        # Stores which item is active
        self.activeItem = None
        # Pens
        gray = QtGui.QColor(128, 128, 128, 255)
        self.penOrigin      = QtGui.QPen(gray,             5,  QtCore.Qt.SolidLine)
        self.penCursorLine  = QtGui.QPen(gray,             3,  QtCore.Qt.SolidLine)
        self.penBlack       = QtGui.QPen(QtCore.Qt.black,  2,  QtCore.Qt.SolidLine)
        self.penActive      = QtGui.QPen(QtCore.Qt.red,    20, QtCore.Qt.SolidLine)
        self.penWhite       = QtGui.QPen(QtCore.Qt.white,  5,  QtCore.Qt.SolidLine)
        self.transparentPen = QtGui.QPen(QtCore.Qt.transparent, 5000)

        ##########################################################
        # Items
        ##########################################################
        self.itemHeight = 40.0 * self.screenFontRatio
        self.items = list()
        # Events sent to items to highlight them
        self.leaveButtonEvent = QtCore.QEvent(QtCore.QEvent.Leave)
        self.enterButtonEvent = QtCore.QEvent(QtCore.QEvent.Enter)

        # Radial item positions relative to center of radial menu
        r = self.screenRatio
        self.position_xy = {'N':  [   0*r, - 90*r],
                            'S':  [   0*r,   90*r],
                            'E':  [ 120*r,    0*r],
                            'W':  [-120*r,    0*r],
                            'NE': [  85*r,  -45*r],
                            'NW': [ -85*r,  -45*r],
                            'SE': [  85*r,   45*r],
                            'SW': [ -85*r,   45*r]}
        # Slices - Each number represents a 22.5 degree slice, so each 
        #          position gets a 45 degree slice of the pie
        self.slices = {'E':  [15,  0],
                       'SE': [ 1,  2],
                       'S':  [ 3,  4],
                       'SW': [ 5,  6],
                       'W':  [ 7,  8],
                       'NW': [ 9, 10],
                       'N':  [11, 12],
                       'NE': [13, 14]}

        # Column widget
        self.column_widget = QtWidgets.QWidget()
        self.column_widget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.column_widget.setParent(self)
        self.column_widget.items = list()
        self.column_widget.rects = list()

        # Draw radial menu and its mask
        self.column_widget_rect = None
        self.paintMask()

    def addItem(self, item=None, text=None):
        self.items.append(item)
        self.painterMask.begin(self.maskPixmap)

        if item.position:
            self.addRadialItem(item=item)
        else:
            self.addColumnItem(item=item)

        self.painterMask.end()
        if not self.transparent:
            self.setMask(self.maskPixmap.createMaskFromColor(QtCore.Qt.white))

    def addRadialItem(self, item=None):
        """
        """
        r = self.screenRatio
        item.setParent(self)
        # Calculate the width of the text
        w,h = self.getTextDimensions(item)
        width = w + (110*r) 
        #height = h+((h*1.2)*r)
        height = h+(h*.75)

        # Get base coordinates for position
        position = item.position
        x,y = self.position_xy[position]

        # Calculate top left x,y - Offset the positions because the 
        #                          buttons are drawn from the top left
        #                          corner and the stored positions are 
        #                          the center around the origin
        if 'W' in position:
            x -= width
            y -= height * (.5)
        if 'E' in position:
            y -= height * (.5)
        if 'N' == position:
            x -= width * (.5)
            y -= height
        if 'S' == position:
            x -= width * (.5)
        if 'NE' == position or 'NW' == position:
            y -= (20*self.screenFontRatio)
        if 'SE' == position or 'SW' == position:
            y += (20*self.screenFontRatio)

        # Widget rectangle
        x += self.width*(.5)
        y += self.height*(.5)
        # slice 
        self.updateSliceMembership()
        # Define rect
        rect = QtCore.QRect(x,y,width,height)
        # Mask and draw
        self.painterMask.fillRect(rect, QtCore.Qt.black)
        item.setGeometry(rect)
        item.p_rect = rect

    def addColumnItem(self, item=None):
        r = self.screenRatio
        greatest_width = 0.0
        columnItems = list()
        for item in self.items: 
            if not item.position:
                columnItems.append(item)
                width = self.getTextDimensions(item)[0] + (110*self.screenFontRatio)
                if width > greatest_width:
                    greatest_width = width
        w = greatest_width+10
        h = self.itemHeight
        i = len(columnItems)
        item.p_rect = QtCore.QRect(40*r,((i-1)*(h-1)),w,h)

        # update class
        self.column_widget.rects.append(item.p_rect)
        self.column_widget.items.append(item)

        # Main column dimensions
        x = (self.width*(.5))-(w*(.5))
        y = (self.height*(.5))+(170*r) 

        # Mask and draw main column
        rect = QtCore.QRect(x,y,w,((h*i)-((i-1)*2)))
        self.column_widget.setGeometry(rect)
        self.column_widget_rect = rect

        # Column mask for all items
        self.painterMask.fillRect(rect, QtCore.Qt.black)

        # Draw item on column
        item.setParent(self.column_widget)
        item.setGeometry(item.p_rect)

    def getTextDimensions(self, item):
        font = item.property('font')
        metric = QtGui.QFontMetrics(font)
        width = metric.width(item.text())
        height = metric.ascent() 
        return(width, height)

    def updateSliceMembership(self):
        """
        Manage mapping pie slices to active positions
           This needs to be updated for all the slices
           each time an item is added or removed.
        
           Default slice membership is predefined for each 
           position in the menu __init__.  self.slices[position] 
           
           We loop through the positional items 
           and store their slices in slicesUsed.
        
           Now we need to loop through and give unused slices
           To the neighboring nearest active position.
        """

        slicesUsed = list()
        for item in self.items:
            position = item.position
            slicesUsed += self.slices[position]
            item.slices = list(self.slices[position]) # Makes copy

        while len(slicesUsed) < 16:
            for item in self.items:
                position = item.position
                # Find surrounding slices from the current items slices
                n = self.pieLast(item.slices[0])
                l = self.pieNext(item.slices[-1])
                # If slices is not used add it to its own slices
                if not n in slicesUsed:
                    item.slices.append(n)
                    slicesUsed.append(n)
                if not l in slicesUsed:
                    item.slices.append(l)
                    slicesUsed.append(l)

    def paintMask(self):
        '''
        Paint a mask for the items so it is transparent around them.
        '''
        self.painterMask.begin(self.maskPixmap)

        # Center background cicle - Where the origin dot
        #                           and line are drawn
        self.painterMask.setBrush(QtCore.Qt.black)
        # Origin offset - how big the visible circles is 
        #                 around the origin dot
        offset = 30*self.screenRatio

        x = (self.width* .5)-((self.originRadius+offset)*.5)
        y = (self.height*.5)-((self.originRadius+offset)*.5)
        w = self.originRadius+offset
        h = w
        self.painterMask.drawEllipse(x,y,w,h)
        self.painterMask.end()

        # Apply mask
        if not self.transparent:
            self.setMask(self.maskPixmap.createMaskFromColor(QtCore.Qt.white))

    def paintEvent(self, event):
        '''
        Main paint event that handles the orginn circle and the line 
        from the origin to the moust direction.
        '''
        try:
            # init painter - QPainting on self does not work outside this method
            #self.painter  = QtGui.QPainter(self)
            self.painter.begin(self)
            cursorPos     = self.mapFromParent(QtGui.QCursor.pos())
            menuCenterPos = QtCore.QPoint(self.width*.5, self.height*.5)

            # Cursor line
            self.painter.setPen(self.penCursorLine)
            self.painter.drawLine(menuCenterPos, cursorPos)
            # Origin circle - black outline
            offset = 2
            self.painter.setPen(self.penOrigin)
            self.painter.drawArc((self.width *.5)-(self.originRadius*.5),
                                 (self.height*.5)-(self.originRadius*.5),
                                  self.originRadius,  self.originRadius, 16, (360*16))
            # Origin circle - gray center
            self.painter.setPen(self.penBlack)
            self.painter.drawArc( (self.width *.5)-((self.originRadius+offset) *.5),
                                  (self.height*.5)-((self.originRadius+offset) *.5),
                                   self.originRadius+offset, self.originRadius+offset, 16, (360*16))

            self.painter.end()
        except:
            traceback.print_exc()

    def mouseMoveEvent(self, event):
        QtWidgets.QMenu.mouseMoveEvent(self, event)
        self.updateWidget()

    def updateWidget(self):
        self.livePos = QtGui.QCursor.pos()
        # Calculate how far has the mouse moved from origin
        length = math.hypot(self.startPos.x() - self.livePos.x(), 
                            self.startPos.y() - self.livePos.y())
        # Calculate angle of current cursor position to origin
        angle  = self.angleFromPoints([self.startPos.x(), self.startPos.y()], 
                                      [self.livePos.x(),  self.livePos.y()])
            
        # Item locations are broken into two 22.5 degree slices
        slice  = int(angle/22.5)
        ############################################################################
        # Highlight items - Highlighting is managed by sending leave and enter 
        #                   events to the items instead of explicingly setting the 
        #                   color.
        ############################################################################
        # Stores what item the user has chosen
        if self.activeItem:
            QtCore.QCoreApplication.sendEvent(self.activeItem, self.leaveButtonEvent)
            self.activeItem = None

        if not self.gesture and self.column_widget_rect:
            self.column_widget.setEnabled(True)
        cursorPos = self.mapFromParent(self.livePos)
        # Check if mouse is outside the origin circle
        if length > 20:
            # Check cursor speed, when the cursor is moving quickly 
            # then we need to ignore the column items
            # Column items check
            if not self.gesture and self.column_widget_rect:
                if self.column_widget_rect.contains(cursorPos):
                    cursorPos = self.column_widget.mapFromGlobal(self.livePos)
                    for i in xrange(len(self.column_widget.rects)):
                        rect = self.column_widget.rects[i]
                        if rect.contains(cursorPos):
                            self.activeItem = self.column_widget.items[i]
                            break
            # Radial items check 
            if not self.activeItem:
                for item in self.items:
                    position = item.position
                    if not position:
                        continue
                    rect = item.p_rect
                    # Clear any existing highlighting
                    QtCore.QCoreApplication.sendEvent(item, self.leaveButtonEvent)
                    # Radial rectangle check
                    if rect.contains(cursorPos):
                        self.activeItem = item
                        break
                    # Slice check
                    if slice in item.slices:
                        self.activeItem = item
        if self.activeItem:
            QtCore.QCoreApplication.sendEvent(self.activeItem, self.enterButtonEvent)
        # Call paint event
        self.update()

    def mouseReleaseEvent(self, event):
        QtWidgets.QMenu.mouseReleaseEvent(self, event)
        for item in self.items:
            QtCore.QCoreApplication.sendEvent(item, self.leaveButtonEvent)
        self.hide()

        # Run items function if it exists
        if self.activeItem:
            if self.activeItem.function:
                try:
                    self.activeItem.function()
                except:
                    traceback.print_exc()

        # Reset widgets
        self.activeItem = None
        self.column_widget.setEnabled(False)
        self.timer.stop()

    def timerStart(self):
        self.gesture = True
        self.startTime = timeit.default_timer()

        self.lastCursorPosition = None
        self.lastTime= None

        self.cursorChange = list()
        self.timeChange = list()
        self.timer.start()

    def angleFromPoints(self, p1=None, p2=None):
        '''
        +X axis to the right is 0 Degrees
        +Y axis up is 90 degrees
        '''
        radians = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
        degrees = math.degrees(radians)
        if(degrees < 0.0):
            degrees += 360.0
        return(degrees)

    def popup(self, pos=None):
        self.startPos = pos
        x = (pos.x()+(self.width*.5))-self.width 
        y = (pos.y()+(self.height*.5))-self.height 
        self.menuRect = QtCore.QRect(x,y,self.width,self.height)
        self.setGeometry(self.menuRect)
        self.show()
        self.timerStart() 

    def rightClickPopup(self, event):
        if event.buttons() != QtCore.Qt.RightButton:
            self.rightClickWidgetMousePressEvent(event)
            return()
        pos = QtGui.QCursor.pos()
        self.popup(pos)

    def rightClickConnect(self, widget=None):
        self.rightClickWidgetMousePressEvent = widget.mousePressEvent
        widget.mousePressEvent = self.rightClickPopup

    def trackCursor(self):
        # Track cursor - When the mouse is first pressed start a timer (x).
        #                At each interval track how much the cursor has moved.
        #                If cursor speed is less then specified threshold
        #                turn of gestuer mode and allow any colum items to be 
        #                selected.
        #       
        pos =  QtGui.QCursor.pos()
        currentTime = timeit.default_timer()
        # Time samples before judging if we have left gesture mode
        samples = 40
        # When the cursor speed is below this value turn gesture mode off
        cursorSpeedTolerance = .02

        if self.lastCursorPosition and self.gesture:
            #timeChange = self.lastTime - currentTime 
            timeChange = currentTime - self.lastTime 
            change = math.hypot(self.lastCursorPosition.x() - pos.x(), 
                                self.lastCursorPosition.y() - pos.y())
            if len(self.cursorChange) < samples:
                self.cursorChange.append(change)
                self.timeChange.append(timeChange)
            else:
                for i in xrange(samples-1):
                    self.cursorChange[i] = self.cursorChange[i+1]
                    self.timeChange[i] = self.timeChange[i+1]
                self.cursorChange[samples-1] = change
                self.timeChange[samples-1] = timeChange

            cursorSpeed = self.mean(self.cursorChange)
            rateOfTimeChange = self.mean(self.timeChange)
            # If the cursor speed is less than .01 pixels 
            # when averaged over the numner of samples then
            # Turn of gesture mode and allow all column items 
            # to be selected
            if len(self.cursorChange) > samples-1:
                if cursorSpeed < cursorSpeedTolerance:
                    self.gesture = False
                    self.updateWidget()
                    self.timer.stop()

        self.lastCursorPosition = pos
        self.lastTime = currentTime

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

    def mean(self, numbers):
        return float(sum(numbers)) / max(len(numbers), 1)

def getScreenRatio():
    refDpi = 192.0
    refHeight = 3240.0
    refWidth = 2160.0

    rect = QtGui.QGuiApplication.primaryScreen().geometry()
    height = max(rect.width(), rect.height())
    width = min(rect.width(), rect.height())
    dpi = QtGui.QGuiApplication.primaryScreen().logicalDotsPerInch()
    screenRatio = min(height/refHeight, width/refWidth);
    if screenRatio < .8:
        screenRatio = .8
    screenFontRatio = min(height*refDpi/(dpi*refHeight), width*refDpi/(dpi*refWidth))
    return(screenRatio, screenFontRatio)

