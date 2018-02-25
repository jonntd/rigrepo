'''
This module is used for everything ikfk
'''

import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.libs.common as common
import rigrepo.libs.transform as transform

class IKFKBase(object):
    '''
    This is the base class for all ik/fk classes.
    '''

    def __init__(self,jointList):
        '''
        This is the constructor

        :param jointList: List of joints to create ikfk setup on.
        :type jointList: list
        '''

        self.setJointList(jointList)
        self._ikJointList = list()
        self._fkJointList = list()
        self._blendJointList = list()
        self._group = "ikfk_grp"

    #GET
    def getJointList(self):
        '''
        Return the list of joints that are being used/created within this
        instance.

        :return: List of joints
        :rtype: list
        '''
        return self._jointList

    def getIkJointList(self):
        '''
        Return the list of joints that are being used/created within this
        instance.

        :return: List of joints
        :rtype: list
        '''
        return self._ikJointList

    def getFkJointList(self):
        '''
        Return the list of joints that are being used/created within this
        instance.

        :return: List of joints
        :rtype: list
        '''
        return self._fkJointList

    def getBlendJointList(self):
        '''
        Return the list of joints that are being used/created within this
        instance.

        :return: List of joints
        :rtype: list
        '''
        return self._blendJointList

    def getGroup(self):
        '''
        Returns the group
        '''
        return self._group

    #SET
    def setJointList(self, value):
        '''
        This will set the _jointList attribute to the given list of jointNames.

        :param value: List of joints you wish to create/use in this instance.
        :type value: list | tuple
        '''
        # do some error checking
        if not isinstance(value, (list,tuple)):
            raise TypeError("{0} must be a list or tuple.".format(value))

        self._jointList = value

    def setFkJointList(self, value):
        '''
        This will set the _jointList attribute to the given list of jointNames.

        :param value: List of joints you wish to create/use in this instance.
        :type value: list | tuple
        '''
        # do some error checking
        if not isinstance(value, (list,tuple)):
            raise TypeError("{0} must be a list or tuple.".format(value))

        self._fkJointList = value

    def setIkJointList(self, value):
        '''
        This will set the _jointList attribute to the given list of jointNames.

        :param value: List of joints you wish to create/use in this instance.
        :type value: list | tuple
        '''
        # do some error checking
        if not isinstance(value, (list,tuple)):
            raise TypeError("{0} must be a list or tuple.".format(value))

        self._ikJointList = value

    def setBlendJointList(self, value):
        '''
        This will set the _jointList attribute to the given list of jointNames.

        :param value: List of joints you wish to create/use in this instance.
        :type value: list | tuple
        '''
        # do some error checking
        if not isinstance(value, (list,tuple)):
            raise TypeError("{0} must be a list or tuple.".format(value))

        self._blendJointList = value

    def setGroup(self, value):
        '''
        Sets the attribute self._group
        '''
        if not isinstance(value, basestring):
            raise TypeError("{0} must be a str".format(value))

        #  if group exists and the value passed is different then rename the group in maya
        if mc.objExists(self._group) and value != self._group:
            mc.rename(self._group, value)

        self._group = value


    def create(self):
        '''
        This will create the ik/fk joint chains and connect/blend them together.
        '''
        #check to see if the ikfk group exists in the current scene.
        if not mc.objExists(self._group):
            mc.createNode("transform",n = self._group)

        ikfkAttr = "{0}.ikfk".format(self._group)

        if not mc.objExists(ikfkAttr):
            mc.addAttr(self._group, ln='ikfk', at="double", 
                min=0, max=1, keyable=True)

        #loop through the joints in the given jointList, and if they exists,
        #create the ik, fk, and blend joint setup.
        fkParent = self._group
        ikParent = self._group
        blendParent = self._group

        for joint in self._jointList:
            if not mc.objExists(joint):
                continue 

            #FK
            fkJnt = "{0}_fk".format(joint)
            if not mc.objExists(fkJnt):
                mc.duplicate(joint, po=True, rr=True, 
                        name= fkJnt)[0]
                mc.parent(fkJnt,fkParent)

            self._fkJointList.append(fkJnt)

            fkParent = fkJnt

            #IK
            ikJnt = "{0}_ik".format(joint)
            if not mc.objExists(ikJnt):
                mc.duplicate(joint, po=True, rr=True, 
                        name= ikJnt)[0]
                mc.parent(ikJnt,ikParent)
            
            self._ikJointList.append(ikJnt)

            ikParent = ikJnt

            #Blend
            blendJntExists = False
            blendJnt = "{0}_blend".format(joint)
            if not mc.objExists(blendJnt):
                mc.duplicate(joint, po=True, rr=True, 
                        name= blendJnt)[0]
                mc.parent(blendJnt,blendParent)
            else:
                blendJntExists = True

            self._blendJointList.append(blendJnt)

            blendParent = blendJnt

            if not blendJntExists:
                # create the blend colors nodes and connect everything
                rotbcn = mc.createNode("blendColors", n="{0}_rot_bcn".format(joint))
                trsbcn = mc.createNode("blendColors", n="{0}_trs_bcn".format(joint))

                # make the connections
                mc.connectAttr(ikfkAttr,"{0}.blender".format(rotbcn),f=True)
                mc.connectAttr(ikfkAttr,"{0}.blender".format(trsbcn),f=True)

                mc.connectAttr("{0}.rotate".format(fkJnt),
                    "{0}.color1".format(rotbcn),f=True)
                mc.connectAttr("{0}.rotate".format(ikJnt),
                    "{0}.color2".format(rotbcn),f=True)

                mc.connectAttr("{0}.translate".format(fkJnt),
                    "{0}.color1".format(trsbcn),f=True)
                mc.connectAttr("{0}.translate".format(ikJnt),
                    "{0}.color2".format(trsbcn),f=True)

                mc.connectAttr("{0}.output".format(rotbcn), 
                    "{0}.rotate".format(blendJnt), f=True)
                mc.connectAttr("{0}.output".format(trsbcn), 
                    "{0}.translate".format(blendJnt), f=True)


class IKFKLimb(IKFKBase):
    '''
    This class is meant for creating three joint ik/fk systems using a rotate plane solver.
    '''
    def __init__(self, jointList):
        '''
        This is the constructor

        :param jointList: List of joints to create ikfk setup on.
        :type jointList: list
        '''
        super(IKFKLimb, self).__init__(jointList)

        self._handle = str()

    # Get
    def getHandle(self):
        '''
        This will return the ikHandle for object
        '''
        return self._handle

    # Set
    def setJointList(self, value):
        '''
        This will check the lenght of the value passed in and then call the parent class 
        to check the type of data.
        '''
        if len(value) != 3:
            raise RuntimeError('This list must be a length of 3')

        super(IKFKLimb, self).setJointList(value)

    @staticmethod
    def createStretchIK(ikHandle, grp):
        '''
        creates a stretchy joint chain based off of influences on ikHandle
        
        Example:
    
        ..python:
            createStrecthIK('l_leg_ik_hdl')
            #Return: 
    
        :param ikHandle: ik handle you influencing joint chain you want to stretch
        :type ikHandle: str
        
        :retrun targetJnts: Joints that are used to calculate the distance
        :rtype: list
        '''
        if not grp or not mc.objExists(grp):
            grp = mc.createNode('transform', n = 'ik_stretch_grp')
    
        #create attributes on grp node
        mc.addAttr(grp, ln='stretch', at='double', dv = 1, min = 0, max = 1, k=True)
        mc.addAttr(grp, ln='stretchTop', at='double', dv = 1, k=True)
        mc.addAttr(grp, ln='stretchBottom', at='double', dv = 1, k=True)
        stretchAttr  = '{}.stretch'.format(grp)
        stretchTopAttr = '{}.stretchTop'.format(grp)
        stretchBottomAttr = '{}.stretchBottom'.format(grp)
        
        #get joints influenced by the ikHandle
        jnts = mc.ikHandle(ikHandle, q = True, jl = True)
        jnts.append(mc.listRelatives(jnts[-1], c = True)[0])
        #create tgt joints for distance node
        targetJnt1 = mc.createNode('joint', n = '{}_{}'.format(jnts[0], common.TARGET))
        targetJnt2 = mc.createNode('joint', n = '{}_{}'.format(jnts[2], common.TARGET))
        mc.xform(targetJnt1, ws=True, t=mc.xform(jnts[0], q=True, ws=True, t=True))
        mc.xform(targetJnt2, ws=True, t=mc.xform(jnts[2], q=True, ws=True, t=True))
        
        #create distance and matrix nodes
        distanceBetween = mc.createNode('distanceBetween', n = '{}_{}'.format(ikHandle, common.DISTANCEBETWEEN))
        startDecomposeMatrix = mc.createNode('decomposeMatrix', n = '{}_{}'.format(targetJnt1, common.DECOMPOSEMATRIX))
        endDecomposeMatrix = mc.createNode('decomposeMatrix', n = '{}_{}'.format(targetJnt2, common.DECOMPOSEMATRIX))
        
        #create condition and multplyDivide nodes
        multiplyDivide = mc.createNode('multiplyDivide', n = '{}_{}'.format(ikHandle, common.MULTIPLYDIVIDE))
        condition = mc.createNode('condition', n = '{}_{}'.format(ikHandle, common.CONDITION))
        multiplyDivideJnt1 = mc.createNode('multiplyDivide', n = '{}_{}'.format(jnts[1], common.MULTIPLYDIVIDE))
        
        blendColorStretch = mc.createNode('blendColors', n = '{}_stretch_{}'.format(grp, common.BLEND))
        multiplyStretch = mc.createNode('multiplyDivide', n = '{}_stretch_{}'.format(grp, common.MULTIPLYDIVIDE))
        plusMinusStretch = mc.createNode('plusMinusAverage', n = '{}_stretch_{}'.format(grp, common.PLUSMINUSAVERAGE))
        
        #connect matrix nodes to distance between node
        mc.connectAttr('{}.worldMatrix[0]'.format(targetJnt1), '{}.inputMatrix'.format(startDecomposeMatrix), f = True)
        mc.connectAttr('{}.worldMatrix[0]'.format(targetJnt2), '{}.inputMatrix'.format(endDecomposeMatrix), f = True)
        mc.connectAttr('{}.outputTranslate'.format(startDecomposeMatrix), '{}.point1'.format(distanceBetween), f = True)
        mc.connectAttr('{}.outputTranslate'.format(endDecomposeMatrix), '{}.point2'.format(distanceBetween), f = True)
        
        #connect multiplyDivide and condition nodes
        aimAxis = transform.getAimAxis(jnts[1], False)
        jnt1Distance = mc.getAttr('{}.t{}'.format(jnts[1], aimAxis))
        jnt2Distance = mc.getAttr('{}.t{}'.format(jnts[2], aimAxis))
        jntLength = jnt1Distance + jnt2Distance
        mc.setAttr('{}.operation'.format(multiplyDivide), 2)    
        if jntLength < 0:
            negDistanceMultiply = mc.createNode('multiplyDivide', n = '{}_distanceNeg_{}'.format(grp, common.MULTIPLYDIVIDE))
            mc.connectAttr('{}.distance'.format(distanceBetween), '{}.input1X'.format(negDistanceMultiply), f = True)
            mc.setAttr('{}.input2X'.format(negDistanceMultiply), -1)
            mc.connectAttr('{}.outputX'.format(negDistanceMultiply), '{}.input1X'.format(multiplyDivide), f = True)
            mc.connectAttr('{}.outputX'.format(negDistanceMultiply), '{}.firstTerm'.format(condition), f = True)
            mc.setAttr('{}.operation'.format(condition), 4)
        else:
            mc.connectAttr('{}.distance'.format(distanceBetween), '{}.input1X'.format(multiplyDivide), f = True)
            mc.connectAttr('{}.distance'.format(distanceBetween), '{}.firstTerm'.format(condition), f = True)
            mc.setAttr('{}.operation'.format(condition), 2)
    
        mc.connectAttr('{}.outputX'.format(multiplyDivide), '{}.input1X'.format(multiplyDivideJnt1), f = True)
        mc.connectAttr('{}.outputX'.format(multiplyDivide), '{}.input1Y'.format(multiplyDivideJnt1), f = True)
        mc.connectAttr('{}.outputX'.format(multiplyDivideJnt1), '{}.colorIfTrueR'.format(condition), f = True)
        mc.connectAttr('{}.outputY'.format(multiplyDivideJnt1), '{}.colorIfTrueG'.format(condition), f = True)
        mc.connectAttr('{}.outColorR'.format(condition), '{}.t{}'.format(jnts[1], aimAxis), f = True)
        mc.connectAttr('{}.outColorG'.format(condition), '{}.t{}'.format(jnts[2], aimAxis), f = True)
    
        mc.connectAttr(stretchAttr, '{}.blender'.format(blendColorStretch), f=True)
        mc.connectAttr(stretchTopAttr, '{}.input1X'.format(multiplyStretch), f=True)
        mc.setAttr('{}.input2X'.format(multiplyStretch), jnt1Distance)
        mc.connectAttr(stretchBottomAttr, '{}.input1Y'.format(multiplyStretch), f=True)
        mc.setAttr('{}.input2Y'.format(multiplyStretch), jnt2Distance)
        mc.connectAttr('{}.outputX'.format(multiplyStretch), '{}.input2D[0].input2Dx'.format(plusMinusStretch), f=True)
        mc.connectAttr('{}.outputY'.format(multiplyStretch), '{}.input2D[1].input2Dx'.format(plusMinusStretch), f=True)
        mc.connectAttr('{}.output2Dx'.format(plusMinusStretch), '{}.input2X'.format(multiplyDivide), f=True)
        mc.connectAttr('{}.output2Dx'.format(plusMinusStretch), '{}.secondTerm'.format(condition), f=True)
        mc.connectAttr('{}.outputX'.format(multiplyStretch), '{}.colorIfFalseR'.format(condition), f=True)
        mc.connectAttr('{}.outputY'.format(multiplyStretch), '{}.colorIfFalseG'.format(condition), f=True)
        mc.connectAttr('{}.outputX'.format(multiplyStretch), '{}.input2X'.format(multiplyDivideJnt1), f=True)
        mc.connectAttr('{}.outputY'.format(multiplyStretch), '{}.input2Y'.format(multiplyDivideJnt1), f=True)
        
        mc.connectAttr('{}.outColorR'.format(condition), '{}.color1R'.format(blendColorStretch), f=True)
        mc.connectAttr('{}.outputX'.format(multiplyStretch), '{}.color2R'.format(blendColorStretch), f=True)
        mc.connectAttr('{}.outColorG'.format(condition), '{}.color1G'.format(blendColorStretch), f=True)
        mc.connectAttr('{}.outputY'.format(multiplyStretch), '{}.color2G'.format(blendColorStretch), f=True)
        
        mc.connectAttr('{}.outputR'.format(blendColorStretch), '{}.t{}'.format(jnts[1], aimAxis), f=True)
        mc.connectAttr('{}.outputG'.format(blendColorStretch), '{}.t{}'.format(jnts[2], aimAxis), f=True)
        
        #parent ikHandle under targetJnt2
        mc.parent(ikHandle, targetJnt2)
        
        #turn off visibility of targetJnts and parent under grp node
        for jnt in [targetJnt1, targetJnt2]:
            mc.setAttr('{}.drawStyle'.format(jnt), 2)
            #mc.parent(jnt, grp)
    
        return [targetJnt1, targetJnt2]
    
    @staticmethod
    def ikMatchFk(fkJoints, ikDriver, pvDriver):
        newPvPos = IKFKLimb.getPoleVectorPosition(fkJoints)
        endJntPos = mc.xform(fkJoints[2], q = True, ws = True, t = True)
        endJntRot = mc.xform(fkJoints[2], q = True, ws = True, ro = True)
        
        mc.xform(pvDriver, ws = True, t = newPvPos)
        mc.xform(ikDriver, ws = True, t = endJntPos)
        mc.xform(ikDriver, ws = True, ro = endJntRot)
        
    @staticmethod
    def fkMatchIk(joints, ikJoints):
        if not joints:
            try:
                joints = mc.ls(sl =True)
            except:
                raise RuntimeError('Nothing selected')
        #end if        
        if not isinstance(joints, list) and not isinstance(joints, tuple):
            raise RuntimeError('{} must be a list or tuple of 3 joints'.format(joints))
        #end if
        if len(joints) != 3:
            raise RuntimeError('{} must have 3 joints in the list'.format(joints))
        #end if
        for jnt in joints:
            if mc.nodeType(jnt) != 'joint':
                raise TypeError('{} must be a joint'.format(jnt))
            
        for jnt, ikJnt in zip(joints, ikJoints):
            trs = mc.xform(ikJnt, q = True, ws = True, t = True)
            rot = mc.xform(ikJnt, q = True, ws = True, ro = True)
            
            mc.xform(jnt, ws = True, t = trs)
            mc.xform(jnt, ws = True, ro = rot)

    @staticmethod
    def getPoleVectorPosition(jointList, scaler=6):
        '''
        This will return a position for the polevector
        '''
        if len(jointList) != 3:
            raise RuntimeError("{0} must be a lenght of three and a list.".format(jointList))
        
        # getting postions to use for the vectors.
        jnt1Pos = mc.xform(jointList[0],q=True, ws=True, t=True)
        jnt2Pos = mc.xform(jointList[1],q=True, ws=True, t=True)
        jnt3Pos = mc.xform(jointList[2],q=True, ws=True, t=True)

        # create vector from world space positions
        vector1 = om.MVector(*jnt1Pos)
        vector2 = om.MVector(*jnt2Pos)
        vector3 = om.MVector(*jnt3Pos)

        # getting the final polevector position.
        midVector = (vector1 + vector3) / 2
        poleVector = ((vector2 - midVector) * 5) + midVector

        return (poleVector.x, poleVector.y, poleVector.z)

    def getPoleVectorFromHandle(self):
        '''
        '''
        if not mc.objExists(self._handle):
            raise RuntimeError("The handle doesn't exist in the current Maya session!!!!")
        '''
        startPoint = om.MPoint(*mc.xform(self._ikJointList[0], q=True, ws=True, t=True))
        endPoint = om.MPoint(*mc.xform(self._ikJointList[-1], q=True, ws=True, t=True))

        pvDistanceVector = (endPoint - startPoint) / 2
        '''
        pvDistanceVector = om.MVector(*mc.xform(self._ikJointList[1], q=True, relative=True, t=True))

        poleVector = om.MVector(*mc.getAttr("{0}.poleVector".format(self._handle))[0]) * pvDistanceVector.length()
        poleVector = poleVector + om.MVector(*mc.xform(self._jointList[0], q=True, ws=True, t=True))

        return (poleVector.x, poleVector.y, poleVector.z)

    def create(self):
        '''
        '''
        if not self._ikJointList:
            super(IKFKLimb, self).create()

        if not mc.objExists(self._handle):
            self._handle = mc.ikHandle(sj=self._ikJointList[0],  ee=self._ikJointList[-1], 
                                        sol="ikRPsolver", 
                                        name="{0}_hdl".format(self._ikJointList[-1]))[0]

        # parent the handle into the ik/fk group
        mc.parent(self._handle, self._group)


class IkFkFoot(IKFKBase):
    def __init__(self, jointList, anklePivot):
        '''
        This is the constructor

        :param jointList: List of joints to create ikfk setup on.
        :type jointList: list
        '''
        super(IkFkFoot, self).__init__(jointList)

        self._handles = list()
        self.ankleHandle = str()
        self.anklePivot = anklePivot
        self.pivotList = None
        if mc.objExists(anklePivot):
            # gathering all the pivots into one list.
            self.pivotList= mc.listRelatives(self.anklePivot, ad=True)
            self.pivotList.reverse()

    # Get
    def getHandles(self):
        '''
        This will return the ikHandle for object
        '''
        return self._handles

    # Set
    def setJointList(self, value):
        '''
        This will check the lenght of the value passed in and then call the parent class 
        to check the type of data.
        '''
        if len(value) != 3:
            raise RuntimeError('This list must be a length of 3')

        super(IkFkFoot, self).setJointList(value)


    def create(self):
        '''
        This method will be used to construct the ikfk system.
        '''
        if not self._ikJointList:
            super(IkFkFoot, self).create()

        ankleConnections = mc.listConnections("{0}.tx".format(self._ikJointList[0]), source=False, destination=True)
        if ankleConnections: 
            effectors = mc.ls(ankleConnections,type='ikEffector')
            if effectors:
                self.ankleHandle = mc.listConnections("{}.handlePath[0]".format(effectors[0]), 
                                    source=False, destination=True)[0]

        # gathering all the pivots into one list.
        if not self.pivotList:
            self.pivotList= mc.listRelatives(self.anklePivot, ad=True)
            self.pivotList.reverse()

        if not self._handles:
            self._handles.append(mc.ikHandle(sj=self._ikJointList[0],  ee=self._ikJointList[1], 
                                        sol="ikSCsolver", 
                                        name="{0}_hdl".format(self._ikJointList[1]))[0])
            self._handles.append(mc.ikHandle(sj=self._ikJointList[1],  ee=self._ikJointList[2], 
                                        sol="ikSCsolver", 
                                        name="{0}_hdl".format(self._ikJointList[2]))[0])

        # parent the handles to the pivot
        mc.parent(self._handles[1], self.pivotList[-1])
        if mc.objExists(self.ankleHandle):
            mc.parent(self.ankleHandle, self.pivotList[-2])

        mc.parent(self._handles[0], self.pivotList[-2])
