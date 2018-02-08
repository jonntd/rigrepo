import maya.cmds as mc

def rotateToOrient(jointList):
    '''
    This will take a joint list and change the rotation in to orientations.

    :param jointList: List of joints you wish to change rotation into orientation.
    '''
    if not isinstance(jointList,(tuple,list)):
        if isinstance(jointList,basestring):
            jointList = [jointList]
        else:
            raise TypeError("{0} must be a list | tuple".format(jointList))

    for jnt in jointList:
        if not mc.objExists(jnt):
            mc.warning("{0} doesn't exist in the current Maya session.".format(jnt))
            continue

        rotateOrder = mc.xform(jnt,q=True,roo=True)
        mc.xform(jnt,roo="xyz")
        orient = mc.xform(jnt,q=True,ws=True,rotation=True)
        mc.setAttr("{0}.jo".format(jnt),0,0,0)
        mc.xform(jnt,ws=True,rotation=orient)
        ori = mc.getAttr(jnt+'.r')[0]
        mc.setAttr("{0}.jo".format(jnt),*ori)
        mc.setAttr("{0}.r".format(jnt),0,0,0)
        mc.xform(jnt,p=True,roo=rotateOrder)
        children = mc.listRelatives(jnt,c=True) or []
        if children:
            mc.parent(children[0],w=True)
            mc.setAttr("{0}.rotateAxis".format(jnt),0,0,0)
            mc.parent(children[0],jnt)
        else:
            mc.setAttr("{0}.rotateAxis".format(jnt),0,0,0)
