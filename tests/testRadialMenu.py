#############################################################
'''
TO RUN TEST 
In Maya
import rigrepo; from rigrepo.tests import testRadialMenu; reload(testRadialMenu); reload(rigrepo.ui.radialMenu); testRadialMenu.test()
In giged Shell
python -c "import rigrepo; from rigrepo.tests import testRadialMenu; reload(testRadialMenu); reload(rigrepo.ui.radialMenu); testRadialMenu.test()"
'''
#############################################################

import sys
from functools import partial
from rigrepo.ui.radialMenu import RadialMenu, RadialMenuItem
from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

class MyWindow(QtWidgets.QMainWindow):
    def tempPrint(self, printStuff, widget):
        print(printStuff)
        if widget.checkBox:
            widget.checkBox.setChecked(not(widget.checkBox.checkState()))

    def __init__(self):
        super(MyWindow, self).__init__()

        ########################################################
        # Build test window
        ########################################################
        ui = Ui_MainWindow()
        ui.setupUi(self)
 
        ########################################################
        # Main Radial Menu
        ########################################################
        # Built items
        items=     {    'N': 'North',
                        'S': 'South',
                        'E': 'East',
                        #'W': 'West',
                        #'NE':'NorthEast',
                        'NW':'NorthWest',
                        'SE':'SouthEast',
                        'SW':'SouthWest'
                        }

        self.pieQMenu = RadialMenu()
        itemWidgets = list()
        for pos in items:
            item = RadialMenuItem(position=pos)
            self.pieQMenu.addItem(item)
            item.setText(items[pos])
            itemWidgets.append(item)
            #item.setCheckable(True)
            item.connect(partial(self.tempPrint, pos, item))
        itemWidgets[0].setCheckable(True)
        itemWidgets[1].setCheckable(True)
        # Build menu
        item = RadialMenuItem(position='W')
        self.pieQMenu.addItem(item)
        self.pieQMenu.rightClickConnect(ui.targetList)

        ########################################################
        # Sub Radial menu
        ########################################################
        #itemWidget[0].connectSub

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
