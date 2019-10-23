'''
This is the data strucure for writing out and reading in picker files.
'''
import rigrepo.libs.data.abstract_data as abstract_data
from collections import OrderedDict
from PySide2 import QtWidgets, QtGui, QtCore
import rigrepo.ui.graphicsWidgets as graphicsWidgets
import rigrepo.ui.mayaGraphicsWidgets as mayaGraphicsWidgets
import maya.cmds as mc

class PickerData(abstract_data.AbstractData):
    '''
    This Class is meant to store picker page information.

    .. note:: 
        Currently this is very rough. We will have to break up or add funcionality still.

    .. warning::
        This is going to be a volatile class for a while until we iron out how this is 
        going to work.
    '''
    def __init__(self, scene=None):
        '''
        Constructor for the joint data class

        :param scene: Item you wish to gather the data for.
        :type scene: QGraphicsScene
        '''
        super(PickerData, self).__init__()
        # this is all super rough. 
        self.scene = scene

    def gatherData(self,item, maya=True):
        '''
        This method will gather data for the node that is passed in as an argument. It will
        store this data on the self._data member/attribute on the class.

        :param maya: Whether or not we're gathering data from Maya or the QGraphicsScene
        :type maya: bool
        '''
        if maya:
            # import the modules we will be using for maya
            import maya.cmds as mc
            import rigrepo.ui.viewport as viewport
            # if the item doesn't exist in the scene then we will return
            if not mc.objExists(item):
                return

            # get the color
            color = QtGui.QColor()
            color.setRgbF(*mc.polyColorPerVertex(mc.ls("{}.vtx[0]".format(item)), q=True, rgb=True))
            vertex_list = mc.ls("{}.vtx[*]".format(item), fl=True)
            # set the dictionary of data for the object.
            self._data[item] = OrderedDict(color=color.getRgb(), 
                points=[list(viewport.worldToQtView(mc.xform(vtx, q=True, ws=True, t=True))) for vtx in vertex_list],
                zValue=mc.xform(vertex_list[0], q=True, ws=True, t=True)[-1], 
                selectableItems=list(), buttonType="null")
            # make sure the attribute exists before trying to set the data.
            # this will store any selectable items that were stored on the button in Maya.
            if mc.objExists(".selectableItems".format(item)):
                selectable_items = eval(mc.getAttr("{}.selectableItems".format(item)))
                if isinstance(selectable_items, list):
                    self._data[item]["selectableItems"] = selectable_items
            # make sure the attribute exists before trying to set the data.
            # this will check what button type is being used.
            if mc.objExists(".buttonType".format(item)):
                self._data[item]["buttonType"] = mc.getAttr("{}.buttonType".format(item))
        else:
            # if we're using the QGraphicsScene, then we will query the data differently.
            if not isinstance(item, QtWidgets.QGraphicsItem):
                raise TypeError("{} must be of type QGraphicsItem.".format(item))
            # store the name of the item and get ready to store the point by making and
            # empty list
            self._data[item.name] = OrderedDict(color=item.color.getRgb(), points=list(), zValue=0.0)

            # loop through and create a list of all of the points for this item
            for i in xrange(item.polygon.count()):
                # get the the point for the index we're at 
                point = item.polygon.toPolygon().point(i)
                self._data[item.name]["points"].append([point.x(), point.y()])

    def gatherDataIterate(self, items, maya=True):
        '''
        This method will iterate through the list of items passed in and use ther gatherData
        method to store the data onto the self._data member/attribute.

        :param items: Array of items you wish to gather the data from.
        :type items: list | tuple
        '''
        for item in items:
            self.gatherData(item, maya)

    def applyData(self, items=list(), maya=False):
        '''
        This is temporary to read in json files.
        '''
        # read in the file with the read function which will return the 
        # data into a dictionary we can unpack
        # if there is data, then we will iterate through the dictionary and make the data
        # set the center point as zero and check if the scene is passed. If scene is passed
        if not items:
            items = self._data.keys()
        center_point = QtCore.QPointF()
        if self.scene:
            center_point = self.scene.sceneRect().center()
        for item in items:
            if self._data.has_key(item):
                # store the point array for the button so we can create a polygon.
                if maya:
                    import rigrepo.ui.viewport as viewport
                    import maya.api.OpenMayaUI as omui2
                    activeView = omui2.M3dView().active3dView()
                    point_array = list()
                    for point in self._data[item]["points"]:
                        pointXY = viewport.viewToWorld(point[0], activeView.portHeight() - point[1])
                        print point, pointXY
                        pointZ = self._data[item]["zValue"]

                        point_array.append((pointXY[0].x, pointXY[0].y, pointZ))
                    color = QtGui.QColor(*self._data[item]["color"])
                    color = color.getRgbF()
                    # create the polygon using the points
                    mc.polyCreateFacet(name=item, ch=False, tx=1, s=1, p=point_array)
                    # select the polygon so we can assign the vertex colors to it.
                    mc.select(item)
                    mc.polyColorPerVertex(rgb=color[0:3], a=color[3], cdo=True)
                    mc.addAttr(item, ln="selectableItems", dt="string")
                    mc.setAttr("{}.selectableItems".format(item), self._data[item]["selectableItems"], type="string")
                    if self._data[item].has_key("buttonType"):
                        button_type = self._data[item]["buttonType"]
                        mc.addAttr(item, ln="buttonType", dt="string")
                        mc.setAttr("{}.buttonType".format(item), self._data[item]["buttonType"], type="string")
                else:
                    point_array = [center_point + QtCore.QPoint(*point) for point in self._data[item]["points"]]
                    # default button type is going to be null.
                    button_type = "null"
                    if self._data[item].has_key("buttonType"):
                        button_type = self._data[item]["buttonType"]
                    # check the different button types and make sure we create the correct one.
                    # if the button is null, we will just create a PolygonItem 
                    if button_type == "null":
                        button_item = graphicsWidgets.PolygonItem(item, 
                                                color=QtGui.QColor(*self._data[item]["color"]), 
                                                polygon=QtGui.QPolygonF(point_array))
                    elif button_type == "select":
                        button_item = mayaGraphicsWidgets.SelectButtonItem(item, 
                                                color=QtGui.QColor(*self._data[item]["color"]), 
                                                polygon=QtGui.QPolygonF(point_array), 
                                                selectableItems=self._data[item]["selectableItems"])
                    elif button_type == "command":
                        button_item = mayaGraphicsWidgets.SelectButtonItem(item, 
                                                color=QtGui.QColor(*self._data[item]["color"]), 
                                                polygon=QtGui.QPolygonF(point_array), 
                                                command=self._data[item]["command"])
                    # set the Z depth for the button.
                    if self._data[item].has_key("zValue"):
                        button_item.setZValue(self._data[item]["zValue"])
                    if self.scene:
                        self.scene.addItem(button_item)