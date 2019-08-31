import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.libs.transform
import rigrepo.libs.common
from rigrepo.libs.common import getMirrorName

def createCurveFromPoints(points, degree=3, name='curve', transformType="transform", form="Open"):
    '''
    :param points: Points you wish to use to create a curve
    :type points: list

    :param degree: The degree of the curve you want to create
    :type degree: int

    :param name: the name of the curve.
    :type name: str

    :param form: The form of the curve. i.e (Open, Closed, Periodic). If the form is Closed or 
                    Periodic we will use a nurbs circle.
    :type form: str

    :return: The name of the curve that was created.
    :rtype: str
    '''
    knotList = [0]
    if degree == 1:
        knotList.extend(range(len(points))[1:])
    elif degree == 2:
        knotList.extend(range(len(points) - 1))
        knotList.append(knotList[-1]) 
    elif degree == 3:
        knotList.append(0) 
        knotList.extend(range(len(points) - 2))
        knotList.extend([knotList[-1],knotList[-1]]) 

    # if the form is closed, we will use a circle to create the control
    if form not in ['Closed', 'Periodic']:
        curve = mc.curve(name=name, p=points,k=knotList,degree=degree)
    else:
        curve = mc.circle(name=name, c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, 
                                d=degree, ut=0, tol=0.01, s=len(points), ch=False) [0] 
        for i,position in enumerate(points):
            mc.setAttr("{}.controlPoints[{}]".format(curve,i), *position)

    # rename all of the shapes that are children of the curve. In this instance, there should
    # only be one.
    for shape in mc.listRelatives(curve, c=True, type="shape"):
        if transformType == "joint":
            trsTypeName =mc.createNode("joint", name="{}_jtn".format(name))
            mc.parent(shape, trsTypeName, r=True, shape=True)
            mc.delete(curve)
            mc.rename(trsTypeName, curve)
            mc.setAttr("{}.drawStyle".format(curve), 2)
        mc.rename(shape, "{}Shape".format(curve))
    
    return curve

def createCurveFromTransforms(transforms, degree=3, name='curve', transformType="transform"):
    '''
    This is a wrapper around createCurveFromPoints

    :param transforms: Points you wish to use to create a curve
    :type transforms: list

    :param degree: The degree of the curve you want to create
    :type degree: int

    :param name: the name of the curve.
    :type name: str

    :return: The name of the curve that was created.
    :rtype: str
    '''
    # This is going to get all of the world space positions for the transforms
    points = [mc.xform(trs, q=True, ws=True, t=True) for trs in transforms]
    return createCurveFromPoints(points, degree, name, transformType)


#----------------------------------------------------
# get information functions
def getCVs(curve):
    '''
    Returns all of the cv's on a given curve

    :param curve: The name of the curve you wish to get the cv's for.
    :type curve: str

    :return: Returns the list of cv's
    :rtype: list
    '''
    return mc.ls('%s.cv[*]' % curve, flatten = True)
    
    
def getCVpositions(cvList):
    '''
    This funtion will return the positions of the cvs

    :param cvList: The points you wish to get the positions for.
    :type cvList: list

    :return: Positions in world space for the cv's given
    :rtype: list
    '''
    positions = list()
    
    for point in cvList:
        ws = mc.xform(point, q=True, ws=True, t=True)
        positions.append(ws)
    
    return positions

def getParamFromPosition(curve, point):
    '''
    Gets a curves parameter value from a position or object in space
    
    :param curve: Curve you want to get paremter for
    :type curve: *str* or *MObject*
    
    :param point: Point in space or Node to get MPoint from
    :type: list | MPoint
    '''
    #get dag path for curve and assign it a nurbsCurve function object 
    dagPath = rigrepo.libs.transform.getDagPath(curve)
    dagPath.extendToShape()
    mFnNurbsCurve = om.MFnNurbsCurve(dagPath)
    
    #Check to see if point is a list or tuple object
    if not isinstance(point, list) and not isinstance(point, tuple):
        if mc.objExists(point):
            point = mc.xform(point, q=True, ws=True, t=True)
    
    return mFnNurbsCurve.getParamAtPoint(om.MPoint(point[0], point[1], point[2]))

def getPointOnCurveFromPosition(curve, point, space=om.MSpace.kWorld):
    '''
    Gets a curves point at curve from position. It will return a MPoint
    
    :param curve: Curve you want to get paremter for
    :type curve: *str* or *MObject*
    
    :param point: Point in space or Node to get MPoint from
    :type: list | MPoint

    :return: This will return the position in world space on the curve
    :rtype: MPoint
    '''
    #get dag path for curve and assign it a nurbsCurve function object 
    dagPath = rigrepo.libs.transform.getDagPath(curve)
    dagPath.extendToShape()
    mFnNurbsCurve = om.MFnNurbsCurve(dagPath)
    
    #Check to see if point is a list or tuple object
    if not isinstance(point, list) and not isinstance(point, tuple):
        if mc.objExists(point):
            point = mc.xform(point, q=True, ws=True, t=True)

    return mFnNurbsCurve.closestPoint(om.MPoint(point[0], point[1], point[2]), space=space)[0]


def mirror (curve, axis = "x"):
    '''
    Mirror curves
    It won't create a new curve, it will only mirror the if there is an existing curve with the 
    replace in it matching the name of search and the currvent curve hase search in it.

    ..example ::
         mirror( mc.ls(sl=True) )

    :param joint: Point you want to mirror
    :type joint: str | list

    :param search: Search side token
    :type search: str

    :param replace: Replace side token
    :type replace: str
    '''

    # get given points
    curveList = rigrepo.libs.common.toList(curve)

    # get selection
    selection = mc.ls(sl=True)

    posVector = ()
    if axis.lower() == 'x':
        posVector = (-1,1,1)
    elif axis.lower() == 'y':
        posVector = (1,-1,1)
    elif axis.lower() == 'z':
        posVector = (1,1,-1)

    # loop through the curve list and mirror across worldspace
    for curveNode in curveList:
        if mc.nodeType(curveNode) == "transform" or mc.nodeType(curveNode) == "joint":
            shapeList = mc.listRelatives(curveNode, c=True, shapes=True, type="nurbsCurve") 
        else:
            shapeList = [curveNode]
        for curve in shapeList:
            cvList=getCVs(curve)
            mirrorCurve = getMirrorName(curve)
            if not mc.objExists(mirrorCurve):
                continue
            for cv in cvList:
                toCV = cv.replace( curve, mirrorCurve )

                # check to make sure that both objects exist in the scnene
                if mc.objExists(cv) and mc.objExists(toCV) and cv != toCV:
                    # get position and rotation
                    pos = mc.xform( cv, q=True, t=True, ws=True )

                    # set rotation orientation
                    mc.xform( toCV, ws = True, t = ( pos[0]*posVector[0], pos[1]*posVector[1], pos[2]*posVector[2] ))
                else:
                    print 'Node not found: {}'.format(toCV)
                    continue                    
                    #raise RuntimeError, 'Node not found: {}'.format(toCV)

    # --------------------------------------------------------------------------
    # re-select objects
    if selection:
        mc.select( selection )
    else:
        mc.select( cl= True)
