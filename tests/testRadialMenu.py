#############################################################
'''
TO RUN TEST 
In Maya
import rigrepo; from rigrepo.tests import testRadialMenu; reload(rigrepo.ui.radialMenu); reload(testRadialMenu); testRadialMenu.test()
In giged Shell
python -c "import rigrepo; from rigrepo.tests import testRadialMenu; reload(rigrepo.ui.radialMenu); reload(testRadialMenu); testRadialMenu.test()"
'''
#############################################################

import sys
from functools import partial
from rigrepo.ui.radialMenu import RadialMenu, RadialMenuItem
from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

class MyWindow(QtWidgets.QMainWindow):
    def tempPrint(self, printStuff):
        print(printStuff)

    def __init__(self):
        super(MyWindow, self).__init__()
        ui = Ui_MainWindow()
        ui.setupUi(self)
        # Items
        items=     {    'N': 'North',
                        'S': 'South',
                        'E': 'East',
                        'W': 'West',
                        'W': 'West',
                        'NE':'NorthEast',
                        'NW':'NorthWest'
                        #'SE':'SouthEast',
                        #'SW':'SouthWest'
                        }
        buttons = list()
        for pos in items:
            item = RadialMenuItem(position=pos)
            item.setText(items[pos])
            item.connect(partial(self.tempPrint, pos))
            if pos == 'W':
                item.setCheckable(1)
            buttons.append(item)
        # Menu
        self.pieQMenu = RadialMenu(items=buttons)
        self.pieQMenu.rightClickConnect(ui.targetList)

        #####################################################################################
        # CONTEXT MENU - connect right click to popup up menu
        #####################################################################################
        
        #  DIRECT METHOD CONNECT - This works, but requires me to store the default mousePressEvent
        #                          for the parent widget of the radialMenu so I can call it the radial
        #                          menu is not needed 
        #
        #ui.targetList.mousePressEvent = self.showMenu 
        
        #  CUSTOM CONTEXT MENU - Doesn't work because signal is only emitted after right click
        #                       is released.
        #
        #ui.targetList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #ui.targetList.customContextMenuRequested.connect(self.showMenu)

        #  DEFUALT CONTEXT MENU - Doesn't work because event is only emitted after right click
        #                         is released.
        #
        #ui.targetList.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        #ui.targetList.contextMenuEvent = pieQMenu.popup

        #  ACTIONS CONEXT MENU - Only works if actions have been added to the widget
        #                         
        #
        self.pieQMenu.addAction('hi')
        #ui.targetList.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        #ui.targetList.customContextMenuRequested.connect(self.showMenu)
        #ui.targetList.contextMenuEvent = self.showMenu

        #  NO CONTEXT MENU - Blocks any context menu call and lets the parent widget handle it.
        #                    This could be useful if I create a signal in the parent widget 
        #                    that emits on right click press. But it doesn't help me with the main
        #                    issue of opening the radial menu on right click press.    
        #
        #ui.targetList.setContextMenuPolicy(QtCore.Qt.NoContextMenu)


##############################
# TEST WINDOW FROM QT DESIGNER
##############################

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(639, 458)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.targetList = QtWidgets.QListWidget(self.centralWidget)
        self.targetList.setObjectName("targetList")
        QtWidgets.QListWidgetItem(self.targetList)
        QtWidgets.QListWidgetItem(self.targetList)
        QtWidgets.QListWidgetItem(self.targetList)
        self.verticalLayout.addWidget(self.targetList)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 639, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Stuff", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        __sortingEnabled = self.targetList.isSortingEnabled()
        self.targetList.setSortingEnabled(False)
        self.targetList.item(0).setText(QtWidgets.QApplication.translate("MainWindow", "ItemA", None, -1))
        self.targetList.item(1).setText(QtWidgets.QApplication.translate("MainWindow", "ItemB", None, -1))
        self.targetList.item(2).setText(QtWidgets.QApplication.translate("MainWindow", "ItemC", None, -1))
        self.targetList.setSortingEnabled(__sortingEnabled)

def test():
    activeWindow = QtWidgets.QApplication.activeWindow()
    if activeWindow:
        title = activeWindow.windowTitle()
        window = MyWindow()
        window.setParent(activeWindow)
        window.setWindowFlags(QtCore.Qt.Window)
        window.show()
        #print("Inside QT {} app".format(title))
    if not activeWindow:
        app = QtWidgets.QApplication(sys.argv)
        window = MyWindow()
        window.show()
        sys.exit(app.exec_())

#if __name__ == '__main__':
#    activeWindow = QtWidgets.QApplication.activeWindow()
#    if activeWindow:
#        title = activeWindow.windowTitle()
#        print("Inside QT {} app".format(title))
#    if not activeWindow:
#        app = QtWidgets.QApplication(sys.argv)
#    window = MyWindow()
#    window.show()
#    if not activeWindow:
#        sys.exit(app.exec_())
