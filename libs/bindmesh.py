'''
This module will handle everything to do with how bindmesh's are handled.
'''
import maya.cmds as mc
import maya.api.OpenMaya as om

def create(name, positionList, cv_names=[]):
    '''
    This will create a bindmesh based on the give N amount of positions. 
    .. note::
        Bindmesh is a bunch of polygon plane's that are combined with rivets at the center
        of each of them.

    :param positionList: An N amount array of 3 point array's.
    :type positionList: tuple | list

    :return: The bindmesh and the follicle information 
    :trype: tuple
    '''
    # Check if the bindmesh has already been created.
    # If it exists return existing bindmesh and follicle names
    #
    newGeoName = "{0}_bindmesh".format(name)
    if mc.objExists(newGeoName):
        follicleNameList = list()
        for i in xrange(len(positionList)):
            follicleName = "{0}_{1}_follicle".format(name, i)
            if cv_names:
                follicleName = cv_names[i]+'_follicle'
            follicleNameList.append(follicleName)
        return newGeoName, follicleNameList

    # define variables we will be mutating
    geoList = list()
    follicleList = list()
    pointList = list()
    # iterate through the cvList and create the plane's and follicles for each plane.
    for i, position in enumerate(positionList):
        geo,createNode = mc.polyPlane()
        for attr in ["subdivisionsHeight","subdivisionsWidth"]:
            mc.setAttr("{0}.{1}".format(createNode,attr),1)
        for attr in ["height","width"]:
            mc.setAttr("{0}.{1}".format(createNode,attr),.02)
        mc.xform(geo,ws=True,t=position)
        geoList.append(geo)
        pointList.append(om.MPoint(*position))

        mc.select(cl=True)

    # combine the plane's into one piece of geometry.
    newGeo = mc.polyUnite(geoList,ch=False,n="{0}_bindmesh".format(name))[0]
    newGeoFaces = mc.ls("{0}.f[*]".format(newGeo))
    mc.polyAutoProjection(newGeoFaces,ch=False,lm=False,pb=False,ibd=True,cm=False,l=2,sc=1,o=1,p=6,ps=0.2,ws=0)
    mc.select(newGeo,r=True)
    selList = om.MGlobal.getActiveSelectionList()
    newGeoDagPath = selList.getDagPath(0)
    newGeoFn = om.MFnMesh(newGeoDagPath)
    newGeoShape = mc.listRelatives(newGeo,c=True,shapes=True)[0]
    # iterate through the cv points and connect the follictles to the bindmesh.
    for i,point in enumerate(pointList):
        uPosition,vPosition = newGeoFn.getUVAtPoint(point)[:-1]
        follicle_name = "{0}_{1}_follicle".format(name,i)
        if cv_names:
            follicle_name = cv_names[i]+'_follicle'
        follicle = mc.createNode("transform", n=follicle_name)
        constraint = mc.pointOnPolyConstraint(newGeoDagPath.fullPathName(), follicle)[0]
        u,v,id = newGeoFn.getUVAtPoint(point,om.MSpace.kWorld)
        mc.setAttr("{}.{}U0".format(constraint, newGeoDagPath.partialPathName()), u)
        mc.setAttr("{}.{}V0".format(constraint, newGeoDagPath.partialPathName()), v)
        follicleList.append(follicle)
    # return the bindmesh
    return newGeo, follicleList

def createFromCurve(name, curve, cv_names=[]):
    '''
    This will create a bindmesh based on the given curve. 
    .. note::
        Bindmesh is a bunch of polygon plane's that are combined with rivets at the center
        of each of them.

    :param curve: The curve you want to put the bindmesh on.
    :type curve: str
    '''
    # get the cv list from the curve
    cvList = mc.ls("{0}.cv[*]".format(curve),flatten=True)
    cvPositionList = [mc.xform(cv,q=True,ws=True,t=True) for cv in cvList]
    return create(name, cvPositionList, cv_names=cv_names)