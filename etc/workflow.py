'''
Module for tool management across apps
A tool has these major properties
    - Context: The mode the app needs to be for the tool to work
    - Settings: The properties of the tool
'''
from PySide2 import QtWidgets, QtGui, QtCore
from grm.radialmenu import RadialMenu, RadialMenuItem, GrmMousePressFilter
from functools import partial

def build_weights_brush_menu():
    items = {'N': 'North',
             'S': 'South',
             'E': 'East',
             # 'W': 'West',
             'NE': 'NorthEast',
             'NW': 'NorthWest',
             'SE': 'SouthEast',
             'SW': 'SouthWest'}

    radial_menu = RadialMenu()
    item_widgets = list()
    for pos in items:
        item = RadialMenuItem(position=pos)
        item.setText(items[pos])
        radial_menu.addItem(item)
        item_widgets.append(item)
        item.connect(partial(temp_print, pos, item))

    # Make some items checkable
    item_widgets[0].setCheckable(True)
    item_widgets[1].setCheckable(True)

    # Build menu
    item = RadialMenuItem(position='W')
    item.setText('WESTSIDE!')
    radial_menu.addItem(item)

    # Test column menu
    item = RadialMenuItem(position=None)
    item.setText('I am in a column')
    radial_menu.addItem(item)

    column_widgets = list()
    for itemText in ['itemA', 'itemB', 'itemC', 'itemD', 'itemF']:
        item = RadialMenuItem(position=None)
        item.setText(itemText)
        item.connect(partial(temp_print, itemText, item))
        radial_menu.addItem(item)
        column_widgets.append(item)
    column_widgets[3].setCheckable(True)

    return(radial_menu)

def build_weights2_brush_menu():
    items = {'N': 'Suck',
             'S': 'it',
             'E': 'trabeck',
             # 'W': 'West',
             'NE': 'trabeck',
             'SW': 'Thats what your mother said'}

    radial_menu = RadialMenu()
    item_widgets = list()
    for pos in items:
        item = RadialMenuItem(position=pos)
        item.setText(items[pos])
        radial_menu.addItem(item)
        item_widgets.append(item)
        item.connect(partial(temp_print, pos, item))

    # Make some items checkable
    item_widgets[0].setCheckable(True)
    item_widgets[1].setCheckable(True)

    # Build menu
    item = RadialMenuItem(position='W')
    item.setText('WESTSIDE!')
    radial_menu.addItem(item)

    # Test column menu
    item = RadialMenuItem(position=None)
    item.setText('I am in a column')
    radial_menu.addItem(item)

    column_widgets = list()
    for itemText in ['itemA', 'itemB', 'itemC', 'itemD', 'itemF']:
        item = RadialMenuItem(position=None)
        item.setText(itemText)
        item.connect(partial(temp_print, itemText, item))
        radial_menu.addItem(item)
        column_widgets.append(item)
    column_widgets[3].setCheckable(True)

    return(radial_menu)

def temp_print(printStuff, widget):
    print(printStuff)
    if widget.checkBox:
        widget.checkBox.setChecked(not(widget.checkBox.checkState()))
