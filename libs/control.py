'''
'''
import os
import rigrepo.libs.curve as curve
import rigrepo.libs.common as common
import rigrepo.libs.data.curve_data as curve_data
import maya.cmds as mc

CONTROLPATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','controls.data')

def create(name="control", controlType = "square", hierarchy=['nul'], position=[0,0,0], 
        rotation=[0,0,0], parent=None, color=common.BLUE):
    '''
    '''
    curveData = curve_data.CurveData()
    curveData.read(CONTROLPATH)
    data = curveData.getData()
    control = curve.createCurveFromPoints(data[controlType]['cvPositions'], 
        degree=data[controlType]['degree'],name=name)

    parent = parent

    hierarchyList = []

    if hierarchy:
        for suffix in hierarchy:
            node = mc.createNode("transform", n="{0}_{1}".format(control,suffix))
            if parent:
                mc.parent(node,parent)

            parent = node
            hierarchyList.append(node)

    if parent:
        mc.parent(control, parent)

    mc.xform(hierarchyList[0], ws=True, t=position)
    mc.xform(hierarchyList[0], ws=True, rotation=rotation)

    if color:
        mc.setAttr("{0}.overrideEnabled".format(control), 1)
        mc.setAttr("{0}.overrideColor".format(control), color)

    return hierarchyList + [control]