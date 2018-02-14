'''
This module is used for everything ikfk
'''

import maya.cmds as mc
import maya.api.OpenMaya as om

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

        mc.addAttr(self._group, ln='ikfk', at="double", 
            min=0, max=1, keyable=True)

        ikfkAttr = "{0}.ikfk".format(self._group)

        #loop through the joints in the given jointList, and if they exists,
        #create the ik, fk, and blend joint setup.
        fkParent = self._group
        ikParent = self._group
        blendParent = self._group

        for joint in self._jointList:
            if not mc.objExists(joint):
                continue 

            #FK
            fkJnt = mc.duplicate(joint, po=True, rr=True, 
                        name= "{0}_fk".format(joint))[0]

            mc.parent(fkJnt,fkParent)
            self._fkJointList.append(fkJnt)

            fkParent = fkJnt

            #IK
            ikJnt = mc.duplicate(joint, po=True, rr=True, 
                        name= "{0}_ik".format(joint))[0]

            mc.parent(ikJnt,ikParent)
            self._ikJointList.append(ikJnt)

            ikParent = ikJnt

            #Blend
            blendJnt = mc.duplicate(joint, po=True, rr=True, 
                        name= "{0}_blend".format(joint))[0]

            mc.parent(blendJnt,blendParent)
            self._blendJointList.append(blendJnt)

            blendParent = blendJnt

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
        self.poleVectorScaler = 9.4

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
    def getPoleVectorPosition(jointList, scaler=3):
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

        poleVector = om.MVector(*mc.getAttr("{0}.poleVector".format(self._handle))[0]) * self.poleVectorScaler
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