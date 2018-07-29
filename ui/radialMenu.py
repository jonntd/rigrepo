import sys
import traceback
import math
from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

class RadialMenuItem(QtWidgets.QPushButton):
    def __init__(self, position=None):
        QtWidgets.QPushButton.__init__(self)
        self.position = position
        # Stop mouse events from affecting radial widgets
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.height = 40
        self.setFixedHeight(self.height)

        # Style
        h = self.palette().highlight().color().getRgb()
        c = self.palette().light().color().getRgb()
        self.h = h
        self.c = c
        style =  """RadialMenuItem:hover{{
                        background-color:rgb({},{},{});
                        border: 2px solid black;
                    }}
                    RadialMenuItem{{
                        border: 2px solid black; 
                        background-color:rgb({},{},{})
                    }}
                 """.format(h[0], h[1], h[2], c[0], c[1], c[2] )
        self.setStyleSheet(style)
        self.checkBox = None

    def connect(self, function):
        self.function = function

    def setCheckable(self, state):
        # ON
        if state:
            if self.checkBox:
                # checkBox already exists, just show it
                self.checkBox.show()
                return
            box = QtWidgets.QCheckBox(self)
            rect = QtCore.QRect(10,7,25, 25)
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

        self.transparent = False 
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.NoDropShadowWindowHint)
        if self.transparent:
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.painter = QtGui.QPainter()
        self.painterMask = QtGui.QPainter()
        # Menu width and heigth
        self.width    = 1000
        #self.height   = 500
        self.height   = 2000
        self.setFixedSize(self.width, self.height)
        # Pixmap used for mask
        self.maskPixmap = QtGui.QPixmap(self.width, self.height)
        # Radius of origin circle
        self.originRadius = 8
        # Right click widget - Stores the mouse press event of the widget 
        #                      the menu is opened from when right clicked
        self.rightClickWidgetMousePressEvent = None
        # Stores which item position is active
        self.activeItem = None
        # Pens
        gray = QtGui.QColor(128, 128, 128, 255)
        self.penOrigin      = QtGui.QPen(gray,             5,  QtCore.Qt.SolidLine)
        self.penCursorLine  = QtGui.QPen(gray,             3,  QtCore.Qt.SolidLine)
        self.penBlack       = QtGui.QPen(QtCore.Qt.black,  2,  QtCore.Qt.SolidLine)
        self.penActive      = QtGui.QPen(QtCore.Qt.red,    20, QtCore.Qt.SolidLine)
        self.penWhite       = QtGui.QPen(QtCore.Qt.white,  5,  QtCore.Qt.SolidLine)
        self.transparentPen = QtGui.QPen(QtCore.Qt.transparent, 5000)

        self.leaveButtonEvent = QtCore.QEvent(QtCore.QEvent.Leave)
        self.enterButtonEvent = QtCore.QEvent(QtCore.QEvent.Enter)

        ##########################################################
        # location menu items
        ##########################################################
        self.itemHeight = 40
        # Stores item widget objects
        self.itemWidgets = dict()
        self.items = list()
        # Item rectangles - used in mouseMove event to check if mouse if over item
        self.itemRect = dict()
        # Item positions relative to center of radial menu
        self.position_xy = {'N':  [   0, - 90],
                            'S':  [   0,   90],
                            'E':  [ 120,    0],
                            'W':  [-120,    0],
                            'NE': [  85,  -45],
                            'NW': [ -85,  -45],
                            'SE': [  85,   45],
                            'SW': [ -85,   45]}
        # Slices - Each number = 22.5 degree slice, so each position gets a
        #          45 degree slice of the pie
        self.angles = {'E':  [15,  0],
                       'SE': [ 1,  2],
                       'S':  [ 3,  4],
                       'SW': [ 5,  6],
                       'W':  [ 7,  8],
                       'NW': [ 9, 10],
                       'N':  [11, 12],
                       'NE': [13, 14]}

        self.slices = {'E':  [15,  0],
                       'SE': [ 1,  2],
                       'S':  [ 3,  4],
                       'SW': [ 5,  6],
                       'W':  [ 7,  8],
                       'NW': [ 9, 10],
                       'N':  [11, 12],
                       'NE': [13, 14]}
        # The item widget is determined by the width of the items text
        self.itemWidth = dict()

        # Store what angles (slices) are used 
        self.anglesUsed = list()

        # Calculate the x and y coordinates of the button items
        #for item in items:
        #    item.setParent(self)
        #    itemPos = item.position
        #    # Calculate the width of the text
        #    font = item.property('font')
        #    fm = QtGui.QFontMetrics(font)
        #    itemWidth = fm.width(item.text()) + 110

        #    # Offset the positions because the buttons are drawn from the top left corner
        #    # and the stored positions are the center around the origin
        #    if 'W' in itemPos:
        #        self.position_xy[itemPos][0] -= itemWidth
        #        self.position_xy[itemPos][1] -= self.itemHeight * .5
        #    if 'E' in itemPos:
        #        self.position_xy[itemPos][1] -= self.itemHeight * .5
        #    if 'N' == itemPos:
        #        self.position_xy[itemPos][0] -= itemWidth * .5
        #        self.position_xy[itemPos][1] -= self.itemHeight
        #    if 'S' == itemPos:
        #        self.position_xy[itemPos][0] -= itemWidth * .5
        #    if 'NE' == itemPos or 'NW' == itemPos:
        #        self.position_xy[itemPos][1] -= 20
        #    if 'SE' == itemPos or 'SW' == itemPos:
        #        self.position_xy[itemPos][1] += 20
        #    self.itemWidgets[itemPos] = item
        #    self.items.append(item)
        #    self.itemWidth[itemPos] = itemWidth
        #    self.anglesUsed += self.angles[itemPos]

        # Draw radial menu and its mask
        self.maskPixmap.fill(QtCore.Qt.white)
        self.columnWidgetRect = None
        self.drawColumnItems()
        self.drawRadialItems()

    def addItem(self, item=None, text=None):
        """
        """
        item.setParent(self)
        self.items.append(item)
        self.painterMask.begin(self.maskPixmap)

        # Calculate the width of the text
        item.setText('hialsdkfsld')
        font = item.property('font')
        metric = QtGui.QFontMetrics(font)
        width = metric.width(item.text()) + 110
        height = item.height

        # Radial item specific settings
        if item.position:
            # Get base coordinates for position
            position = item.position
            x,y = self.position_xy[position]

            # Calculate top left x,y - Offset the positions because the 
            #                          buttons are drawn from the top left
            #                          corner and the stored positions are 
            #                          the center around the origin
            if 'W' in position:
                x -= width
                y -= height * .5
            if 'E' in position:
                y -= height * .5
            if 'N' == position:
                x -= width * .5
                y -= height
            if 'S' == position:
                x -= width * .5
            if 'NE' == position or 'NW' == position:
                y -= 20
            if 'SE' == position or 'SW' == position:
                y += 20

            self.itemWidgets[position] = item
            self.itemWidth[position] = width

            # Widget rectangle
            x += self.width*.5
            y += self.height*.5
            # slice 
            item.slices = self.slices[position]
            self.updateSliceMembership()

        # Define rect
        rect = QtCore.QRect(x,y,width,height)
        # Store rect for mouse over detection 
        self.itemRect[item.position] = rect
        item.p_rect = rect
                                    
        # Paint rect mask
        self.painterMask.fillRect(rect, QtCore.Qt.black)
        # Apply widget rect
        item.setGeometry(rect)
        # Stop paint
        self.painterMask.end()
        # Apply mask
        if not self.transparent:
            self.setMask(self.maskPixmap.createMaskFromColor(QtCore.Qt.white))

    def updateSliceMembership(self):
        """
        Manage mapping pie slices to active positions
           This needs to be updated for all the slices
           each time an item is added or removed.
        
           Default slice membership is predefined for each 
           position in the menu __init__.  self.angles[position] 
           
           We loop through the positional items 
           and store their angles in self.slicesUsed.
        
           Now we need to loop through and give unused slices
           To the nearest active position.
        """

        self.slicesUsed = list()
        for item in self.items:
            position = item.position
            self.slicesUsed += self.slices[position]

        while len(self.slicesUsed) < 16:
            for item in self.items:
                position = item.position
                # Find surrounding slices from the current items slices
                n = self.pieLast(self.slices[position][0])
                l = self.pieNext(self.slices[position][-1])
                # If slices is not used add it to its own slices
                if not n in self.slicesUsed:
                    self.slices[position] = [n]+self.slices[position]
                    self.slicesUsed.append(n)
                if not l in self.slicesUsed:
                    self.slices[position].append(l)
                    self.slicesUsed.append(l)


        # Main widget column items live in

    def drawColumnItems(self):
        # Main widget column items live in
        self.columnWidget = QtWidgets.QWidget()
        self.columnWidget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.columnWidget.setParent(self)

        self.columnWidget.items = list()
        self.columnWidget.rects = list()

        # column dimensions
        w = 300
        x = (self.width*.5)-(w*.5)
        y = (self.height*.5)+150  

        itemText = ['item1', 'item2', 'item3', 'item4']
        for i, itemText in enumerate(itemText):
            item = RadialMenuItem()
            self.columnWidget.items.append(item)
            if not i:
                h = item.height
            else:
                item.setCheckable(True)
            item.setParent(self.columnWidget)
            item.setText(itemText)
            item.setFixedWidth(w)
            rect = QtCore.QRect(0,(i*(h-2)),w,h)
            item.setGeometry(rect)
            self.columnWidget.rects.append(rect)

        i = len(self.columnWidget.items)
        rect = QtCore.QRect(x,y,w,((h*i)-((i-1)*2)))
        self.columnWidget.setGeometry(rect)
        self.columnWidgetRect = rect

    def drawRadialItems(self):
        '''
        Paint a mask for the items so it is transparent around them.
        '''
        # Pixmap for mask
        self.painterMask.begin(self.maskPixmap)

        # Draw item rectangles
        for itemPosition in self.position_xy:
            if not itemPosition in self.itemWidgets:
                continue
            pos  = self.position_xy[itemPosition]
            item = self.itemWidgets[itemPosition]
            # Widget rectangle
            x = pos[0]+self.width *.5
            y = pos[1]+self.height*.5
            w = self.itemWidth[itemPosition]
            h = self.itemHeight
            rect = QtCore.QRect(x,y,w,h)
                                        
            # Store rect for mouse over detection 
            self.itemRect[itemPosition] = rect
            item.p_rect = rect
            # Mask rectangle
            self.painterMask.fillRect(rect, QtCore.Qt.black)
            # Apply widget rectangle
            item.setGeometry(rect)
        # Column items
        if self.columnWidgetRect:
            self.painterMask.fillRect(self.columnWidgetRect, QtCore.Qt.black)

        # Center background cicle - Where the origin dot and line are drawn
        self.painterMask.setBrush(QtCore.Qt.black)
        offset = 30
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
        # Using try statement to capture the traceback errors, no errors were printing
        # sometimes without out it.
        #QtWidgets.QMenu.paintEvent(self, event)
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
            self.painter.drawArc((self.width *.5)-self.originRadius*.5,
                                 (self.height*.5)-self.originRadius*.5,
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
        self.livePos = QtGui.QCursor.pos()
        # Calculate how far has the mouse moved from origin
        length = math.hypot(self.startPos.x() - self.livePos.x(), self.startPos.y() - self.livePos.y())
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

        # Check if mouse is outside the origin circle
        cursorPos = self.mapFromParent(self.livePos)
        if length > 20:
            # Column items check
            if self.columnWidgetRect.contains(cursorPos):
                cursorPos = self.columnWidget.mapFromGlobal(self.livePos)
                for i in xrange(len(self.columnWidget.rects)):
                    rect = self.columnWidget.rects[i]
                    if rect.contains(cursorPos):
                        self.activeItem = self.columnWidget.items[i]
                        break
            # Radial items check
            else:
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
                    if slice in self.slices[position]:
                        self.activeItem = item
        if self.activeItem:
            QtCore.QCoreApplication.sendEvent(self.activeItem, self.enterButtonEvent)
        # Call paint event
        self.update()

    def mouseReleaseEvent(self, event):
        QtWidgets.QMenu.mouseReleaseEvent(self, event)
        for position in self.position_xy:
            if not position in self.itemWidgets:
                continue
            item = self.itemWidgets[position]
            QtCore.QCoreApplication.sendEvent(item, self.leaveButtonEvent)
        # Run items function if it exists
        if self.activeItem:
            if self.activeItem.function:
                self.activeItem.function()
        self.activeItem = None
        #self.hide()

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
        #self.setAttribute(QtCore.Qt.WA_NoSystemBackground, 1)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.setAttribute(QtCore.Qt.WA_NoSystemBackground, 0)
        QtWidgets.QMenu.popup(self, QtCore.QPoint(x,y))

    def rightClickConnect(self, widget=None):
        self.rightClickWidgetMousePressEvent = widget.mousePressEvent
        widget.mousePressEvent = self.rightClickPopup

    def rightClickPopup(self, event):
        if event.buttons() != QtCore.Qt.RightButton:
            self.rightClickWidgetMousePressEvent(event)
            return()

        pos = QtGui.QCursor.pos()
        self.popup(pos)

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

