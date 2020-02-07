import maya.cmds as mc
import rigrepo.libs.common
import traceback

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
            continue
        try:
            rotateOrder = mc.xform(jnt,q=True,roo=True)
            mc.xform(jnt,roo="xyz")
            orient = mc.xform(jnt,q=True,ws=True,rotation=True)
            mc.setAttr("{0}.jo".format(jnt),0,0,0)
            mc.xform(jnt,ws=True,rotation=orient)
            ori = mc.getAttr(jnt+'.r')[0]
            mc.setAttr("{0}.jo".format(jnt),*ori)
            mc.setAttr("{0}.r".format(jnt),0,0,0)
            mc.xform(jnt,p=True,roo=rotateOrder)
            children = mc.listRelatives(jnt,c=True, type="joint") or []
            if children:
                mc.parent(children[0],w=True)
                mc.setAttr("{0}.rotateAxis".format(jnt),0,0,0)
                mc.parent(children[0],jnt)
            else:
                mc.setAttr("{0}.rotateAxis".format(jnt),0,0,0)
        except:
            continue



def mirror (joint, search = '_l_', replace = '_r_', axis = "x", mode='rotate'):
    '''
    Mirror joint orientation
    It will not create a new joint. It will only mirror to an existing joint that has the same
    name with the search and replace different.

    ..example ::
         mirror( mc.ls(sl=True) )

    :param joint: Point you want to mirror
    :type joint: str | list

    :param search: Search side token
    :type search: str

    :param mode: Type of mirror. 'rotate' or 'translate'
                 rotation is for things like limbs generally.
                 translation is for joints that need symmetric translation and rotation, like in the face.
    :type mode: string

    :param replace: Replace side token
    :type replace: str
    '''


    # get given joints
    jointList = rigrepo.libs.common.toList(joint)

    # get selection
    selection = mc.ls(sl=True)

    trsVector = ()
    rotVector = ()
    if axis.lower() == 'x':
        trsVector = (-1,1,1)
        rotVector = (0,180,180)
    elif axis.lower() == 'y':
        trsVector = (1,-1,1)
        rotVector = (180,0,180)
    elif axis.lower() == 'z':
        trsVector = (1,1,-1)
        rotVector = (180,180,0)

    for i,jnt in enumerate(jointList):

        jnt2 = jnt.replace( search, replace )

        if mc.objExists(jnt) and mc.objExists(jnt2) and jnt != jnt2:

            # parent children
            jointGroup = mc.createNode('transform')
            children   = mc.listRelatives( jnt2, type='transform' )
            if children:
                mc.parent( list(set(children)), jointGroup )

            # get position and rotation
            trs = mc.xform( jnt, q=True, rp=True, ws=True )
            rot = mc.xform( jnt, q=True, ro=True, ws=True )

            # set rotation orientation
            mc.xform( jnt2, ws = True, 
                        t = ( trs[0]*trsVector[0], trs[1]*trsVector[1], trs[2]*trsVector[2] ), 
                        ro=rot )
            mc.xform( jnt2, ws = True, r = True, ro = rotVector )

            # Mirror mode translate is for things like face joints where
            # symmetric translation is needed
            if mode == 'translate':
                try:
                    mc.makeIdentity(jnt2, apply=1, r=1)
                    mc.setAttr(jnt2+'.rz', 180)
                    mc.makeIdentity(jnt2, apply=1, r=1)
                except:
                    traceback.print_exc()
                    print('Could not zero out {}'.format(jnt2))

            # set prefered angle
            if mc.objExists( '{}.{}'.format(jnt, 'preferredAngle') ):
                preferredAngle = mc.getAttr( '{}.{}'.format(jnt, 'preferredAngle'))[0]
                if mc.objExists( '{}.{}'.format(jnt2, 'preferredAngle')):
                    mc.setAttr( '{}.{}'.format(jnt2, 'preferredAngle'),
                                  preferredAngle[0],
                                  preferredAngle[1],
                                  preferredAngle[2] )

            # re-parent children to jnt2
            if children:
                mc.parent( children, jnt2 )
            mc.delete( jointGroup )

        else:
            raise RuntimeError, 'Node not found: {}}'.format(jnt2)

    # --------------------------------------------------------------------------
    # re-select objects
    if selection:
        mc.select( selection )
    else:
        mc.select( cl= True)

def duplicateChain(jointList, names=None, parent=None):
    '''
    Duplicates a list of joints into a chain. Generally used for ik chain building.

    :param jointList: List of joints that will be duplicated into a chain.
    :param names: Name for each of the created joints
    :param parent: Parent of the new chain
    :return: List of the newly created joints
    '''
    newJointList = list()
    if not names:
        names = [x + '_dup' for x in jointList]

    for joint, name in zip(jointList, names):
        if not mc.objExists(joint):
            continue
        dupJoint = mc.createNode('joint', name=name)
        newJointList.append(dupJoint)
        if parent:
            mc.parent(dupJoint, parent)
        mc.delete(mc.parentConstraint(joint, dupJoint))
        mc.makeIdentity(dupJoint, apply=1, r=1)
        parent = dupJoint

    mc.select(dupJoint)
    return(newJointList)

