import maya.cmds as cmds
import maya.api.OpenMaya as om

def create(curve):
    '''
    This will create a bindmesh based on the given curve. 
    .. note::
        Bindmesh is a bunch of polygon plane's that are combined with rivets at the center
        of each of them.

    :param curve: The curve you want to put the bindmesh on.
    :type curve: str
    '''
    # get the cv list from the curve
    cvList = cmds.ls("{0}.cv[*]".format(curve),flatten=True)
    geoList = []
    cvPointList = []
    follicleList = []
    # iterate through the cvList and create the plane's and follicles for each plane.
    for i,cv in enumerate(cvList):
        geo,createNode = cmds.polyPlane()
        for attr in ["subdivisionsHeight","subdivisionsWidth"]:
            cmds.setAttr("{0}.{1}".format(createNode,attr),1)
        for attr in ["height","width"]:
            cmds.setAttr("{0}.{1}".format(createNode,attr),.2)
        cvPosition = cmds.xform(cv,q=True,ws=True,t=True)
        cmds.xform(geo,ws=True,t=cvPosition)
        geoList.append(geo)
        cvPointList.append(om.MPoint(*cvPosition))
        
        cmds.select(cl=True)
        # create the follicle
        follicleShape = cmds.createNode("follicle",n="{0}_{1}_follicleShape".format(curve,i))
        follicleTrs = cmds.rename(cmds.listRelatives(follicleShape,p=True)[0],"{0}_{1}_follicle".format(curve,i))
        follicleList.append((follicleTrs,cmds.listRelatives(follicleTrs,c=True,shapes=True)[0]))

    # combine the plane's into one piece of geometry.
    newGeo = cmds.polyUnite(geoList,ch=False,n="{0}_bindmesh".format(curve))[0]
    newGeoFaces = cmds.ls("{0}.f[*]".format(newGeo))
    cmds.polyAutoProjection(newGeoFaces,ch=False,lm=False,pb=False,ibd=True,cm=False,l=2,sc=1,o=1,p=6,ps=0.2,ws=0)
    cmds.select(newGeo,r=True)
    selList = om.MGlobal.getActiveSelectionList()
    newGeoDagPath = selList.getDagPath(0)
    newGeoFn = om.MFnMesh(newGeoDagPath)
    newGeoShape = cmds.listRelatives(newGeo,c=True,shapes=True)[0]
    # iterate through the cv points and connect the follictles to the bindmesh.
    for i,point in enumerate(cvPointList):
        uPosition,vPosition = newGeoFn.getUVAtPoint(point)[:-1]
        u,v,id = newGeoFn.getUVAtPoint(point,om.MSpace.kWorld)
        cmds.connectAttr("{0}.worldMatrix[0]".format(newGeoShape), "{0}.inputWorldMatrix".format(follicleList[i][1]),f=True) 
        cmds.connectAttr("{0}.outMesh".format(newGeoShape), "{0}.inputMesh".format(follicleList[i][1]),f=True) 
        cmds.setAttr("{0}.parameterU".format(follicleList[i][1]),u)
        cmds.setAttr("{0}.parameterV".format(follicleList[i][1]),v)
        cmds.connectAttr("{0}.outRotate".format(follicleList[i][1]), "{0}.rotate".format(follicleList[i][0]),f=True) 
        cmds.connectAttr("{0}.outTranslate".format(follicleList[i][1]), "{0}.translate".format(follicleList[i][0]),f=True)

    # return the bindmesh
    return newGeo, follicleList