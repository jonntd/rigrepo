'''
This module is used for everything spline ik related
'''

import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.libs.curve  
import rigrepo.libs.cluster
import rigrepo.libs.transform

class SplineBase(object):
    '''
    This is the base class for all ik/fk classes.
    '''

    def __init__(self,jointList,splineName='splineIk',curve=None):
        '''
        This is the constructor

        :param jointList: List of joints to create spline ik setup on. Assumes descending order [root, child, child...]
        :param curve: Curve to be used by spline ik. A curve will be created automatically if None is passed.
        :type jointList: list
        '''

        self.setJointList(jointList)
        self._name = splineName 
        self._group = self._name+'_grp' 
        self._curve = curve
        self._ikHandle = str()
        self._ikJointList = list()
        self._clusters = list()
        self._startTwistNul = str()
        self._endTwistNul = str() 

    #GET
    def getJointList(self):
        '''
        Return the list of joints that are being used/created within this
        instance.

        :return: List of joints
        :rtype: list
        '''
        return self._jointList

    def getGroup(self):
        '''
        Returns the group
        '''
        return self._group

    def getClusters(self):
        '''
        Returns the group
        '''
        return self._clusters

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
        This will create the ik spline on the joint list.
        jointList must be in descending hierarchical order
        '''
        #loop through the joints in the given jointList, and if they exist,
        ikParent = self._group
        blendParent = self._group

        for joint in self._jointList:
            if not mc.objExists(joint):
                raise RuntimeError('Joint [ {} ] does not exist'.format(joint))

        if not mc.objExists(self._group):
            mc.createNode("transform", n=self._group)

        # Creat duplicate joint chain
        for i,joint in enumerate(self._jointList):
            j = mc.duplicate(joint, po=True, rr=True, name= "{}_jnt_{}".format(self._name, i))[0]
            self._ikJointList.append(j)
            mc.setAttr(j+'.displayLocalAxis', 1)
            if i:
                mc.parent(j, self._ikJointList[i-1])
            else:
                mc.parent(j, self._group)

        startJoint = self._ikJointList[0]
        endJoint = self._ikJointList[-1]
        ik = mc.ikHandle(n=self._name+'_handle', pcv=0, ns=1, sol='ikSplineSolver', sj=startJoint, ee=endJoint)
        self._ikHandle =  ik[0]
        self._curve = mc.rename(ik[2], self._name+'_curve')
        mc.parent(self._ikHandle, self._curve, self._group)

        # Localize curve
        #mc.connectAttr(self._curve+'.local', self._ikHandle+'.inCurve', f=1) 

        # Create clusters
        #clusterGrp = mc.createNode('transform', n=self._name+'_clusters_grp', p=self._group)
        cvs = rigrepo.libs.curve.getCVs(self._curve) 
        for i,cv in enumerate(cvs):
            cluster,handle = mc.cluster(cv, n='{}_cluster_{}'.format(self._name, i))
            self._clusters.append(handle)
            mc.parent(handle, self._group)
            rigrepo.libs.cluster.localize(cluster, self._group, self._group, weightedCompensation=True)

        # Stretch 
        curve_info = mc.arclen(self._curve, ch=1)
        curve_info = mc.rename(curve_info, self._name+"_curveInfo")
        mc.connectAttr(self._curve+'.local', curve_info+'.inputCurve', f=1) 

        full_scale = mc.createNode('multiplyDivide', n=self._name+'_scale_mul')
        mc.connectAttr(curve_info+'.arcLength', full_scale+'.input1X')
    
        arc_length = mc.getAttr(curve_info+'.arcLength')
        mc.setAttr(full_scale+'.input2X', arc_length)
        mc.setAttr(full_scale+'.operation', 2)

        for i,j in enumerate(self._ikJointList[1:]):
            bone_scale = mc.createNode('multiplyDivide', n='{}_{}_stretch_mul'.format(self._name, i))
            mc.connectAttr(full_scale+'.output.outputX', bone_scale+'.input2X')
            joint_tx = mc.getAttr(j+'.tx')
            mc.setAttr(bone_scale+'.input1X', joint_tx)
            mc.connectAttr(bone_scale+'.output.outputX', j+'.tx')

        # Start 
        startGrp = mc.createNode('transform', n=self._name+'_start_grp', p=self._group)
        start = mc.spaceLocator(n=self._name+'_start')[0]
        self._startTwistNul = start
        mc.parent(start, startGrp)
        con = mc.parentConstraint(self._ikJointList[0], startGrp)
        mc.delete(con)
        rigrepo.libs.transform.decomposeRotation(start)

        # End 
        endGrp = mc.createNode('transform', n=self._name+'_end_grp', p=self._group)
        end = mc.spaceLocator(n=self._name+'_end')[0]
        self._endTwistNul = end
        mc.parent(end, endGrp)
        con = mc.parentConstraint(self._ikJointList[-1], endGrp)
        mc.delete(con)
        rigrepo.libs.transform.decomposeRotation(end)

        twist_add = mc.createNode('plusMinusAverage', n=self._name+'_addtwist')

        mc.connectAttr(end+'.decomposeTwist', twist_add+'.input1D[0]')

        reverseStartTwist = mc.createNode('multiplyDivide', n=self._name+'_reverseStart_mul')
        mc.setAttr(reverseStartTwist+'.input2X', -1)
        mc.connectAttr(start+'.decomposeTwist', reverseStartTwist+'.input1X')

        mc.connectAttr(reverseStartTwist+'.outputX', twist_add+'.input1D[1]')

        mc.connectAttr(start+'.decomposeTwist', self._ikHandle+'.roll')
        mc.connectAttr(twist_add+'.output1D', self._ikHandle+'.twist')

        # Connect to bind joints
        for ik,bind in zip(self._ikJointList, self._jointList):
            mc.pointConstraint(ik, bind, mo=1)
            mc.orientConstraint(ik, bind, mo=1)
            mc.connectAttr(ik+'.s', bind+'.s')
