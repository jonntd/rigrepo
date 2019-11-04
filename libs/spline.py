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

        :param jointList: List of joints to create spline ik setup on. Assumes descending order 
                            [root, child, child...]
        :param curve: Curve to be used by spline ik. A curve will be created automatically if 
                        None is passed.
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

    def getCurve(self):
        '''
        Returns the curve for the spline
        '''
        return self._curve

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

        curve = rigrepo.libs.curve.createCurveFromTransforms((self._ikJointList[0], 
                                                                self._ikJointList[1], 
                                                                self._ikJointList[-2], 
                                                                self._ikJointList[-1]), 
                                                            degree=2, name=self._name+'_curve')
        ik = mc.ikHandle(n=self._name+'_handle', pcv=0, ns=1, sol='ikSplineSolver', 
                            sj=startJoint, ee=endJoint, curve=curve, freezeJoints=True)
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
            rigrepo.libs.cluster.localize(cluster, self._group, self._group, 
                                            weightedCompensation=True)

        # Stretch 
        curve_info = mc.arclen(self._curve, ch=1)
        curve_info = mc.rename(curve_info, self._name+"_curveInfo")
        mc.connectAttr(self._curve+'.local', curve_info+'.inputCurve', f=1) 

        full_scale = mc.createNode('multiplyDivide', n=self._name+'_scale_mul')
        mc.connectAttr(curve_info+'.arcLength', full_scale+'.input1X')
    
        arc_length = mc.getAttr(curve_info+'.arcLength')
        mc.setAttr(full_scale+'.input2X', arc_length)
        mc.setAttr(full_scale+'.operation', 2)

        # get the rotateOrder and twistAxis for the 
        transValue = mc.getAttr("{}.t".format(self._ikJointList[-1]))[0]
        twistAxis = ['x','y','z'][transValue.index(max(transValue))]
        rotateOrder = mc.getAttr("{}.ro".format(self._ikJointList[-1]))

        for i,j in enumerate(self._ikJointList[1:]):
            bone_scale = mc.createNode('multiplyDivide', 
                                        n='{}_{}_stretch_mul'.format(self._name, i))
            mc.connectAttr(full_scale+'.output.outputX', bone_scale+'.input2X')
            joint_tx = mc.getAttr(j+'.t{}'.format(twistAxis))
            mc.setAttr(bone_scale+'.input1X', joint_tx)
            mc.connectAttr(bone_scale+'.output.outputX', j+'.t{}'.format(twistAxis))

        # Start 
        startGrp = mc.createNode('transform', n=self._name+'_start_grp', p=self._group)
        start = mc.spaceLocator(n=self._name+'_start')[0]
        self._startTwistNul = start
        mc.parent(start, startGrp)
        con = mc.parentConstraint(self._ikJointList[0], startGrp)
        mc.delete(con)
        rigrepo.libs.transform.decomposeRotation(start, twistAxis=twistAxis, rotateOrder=rotateOrder)

        # End 
        endGrp = mc.createNode('transform', n=self._name+'_end_grp', p=self._group)
        end = mc.spaceLocator(n=self._name+'_end')[0]
        self._endTwistNul = end
        mc.parent(end, endGrp)
        con = mc.parentConstraint(self._ikJointList[-1], endGrp)
        mc.delete(con)
        rigrepo.libs.transform.decomposeRotation(end, twistAxis=twistAxis, rotateOrder=rotateOrder)

        twist_add = mc.createNode('plusMinusAverage', n=self._name+'_addtwist')

        mc.connectAttr(end+'.decomposeTwist', twist_add+'.input1D[0]')

        reverseStartTwist = mc.createNode('multiplyDivide', n=self._name+'_reverseStart_mul')
        mc.setAttr(reverseStartTwist+'.input2X', -1)
        mc.connectAttr(start+'.decomposeTwist', reverseStartTwist+'.input1X')

        mc.connectAttr(reverseStartTwist+'.outputX', twist_add+'.input1D[1]')

        mc.connectAttr(start+'.decomposeTwist', self._ikHandle+'.roll')
        mc.connectAttr(twist_add+'.output1D', self._ikHandle+'.twist')

        # Connect to bind joints
        i = 0
        for ik,bind in zip(self._ikJointList, self._jointList):
            mc.addAttr(self._group, ln="scale_{}".format(i), at="double", min=0, max=1, dv=0)
            mc.pointConstraint(ik, bind, mo=1)
            mc.orientConstraint(ik, bind, mo=1)
            mc.connectAttr(ik+'.s', bind+'.s')
            blendNode = mc.createNode("blendColors", n="{}_scale_blend".format(ik))
            addNode = mc.createNode("plusMinusAverage", n="{}_scale_add".format(ik))
            subtractNode = mc.createNode("plusMinusAverage", n="{}_scale_subtract".format(ik))

            # set add and subtract attributes
            mc.setAttr("{}.input1D[0]".format(subtractNode), 1)
            mc.setAttr("{}.operation".format(subtractNode), 2)
            mc.connectAttr("{}.outputR".format(blendNode), "{}.input1D[1]".format(subtractNode), f= True)

            # set add and subtract attributes
            mc.setAttr("{}.input1D[1]".format(addNode), 1)
            mc.connectAttr("{}.output1D".format(subtractNode), "{}.input1D[0]".format(addNode), f= True)

            # make connections
            mc.connectAttr("{}.outputX".format(full_scale), "{}.color1R".format(blendNode), f=True)
            mc.connectAttr("{}.scale_{}".format(self._group, i), "{}.blender".format(blendNode), f=True)
            mc.setAttr("{}.color2R".format(blendNode), 1.0)
            scaleAttrs = ['x','y', 'z']
            scaleAttrs.pop(scaleAttrs.index(twistAxis))
            for attr in scaleAttrs:
                mc.connectAttr("{}.output1D".format(addNode), '{}.s{}'.format(ik, attr), f= True)
            i += 1

        # set the scale for the spine
        setScaleList = list(self._ikJointList)
        value = 1.0
        size = len(setScaleList)
        valueScale = value/size
        for i in xrange(size):
            #minus 1 because the first element is index 0
            middleIndex = (len(setScaleList) - 1)/2
            mc.setAttr("{}.scale_{}".format(self._group, self._ikJointList.index(setScaleList[middleIndex])), value)
            value-=valueScale
            setScaleList.pop(middleIndex)


def preserveLength(name='spineIk',
                   curve='spineIk_curve',
                   primary_control='chest',
                   rotate_controls=['chest', 'chest_ik', 'torso'],
                   no_rotate_cvs=[2, 3],
                   parent='spine',
                   position_output_child='chest_top_nul'):

    curve_full = name

    # Create length curves
    curve_full = mc.duplicate(curve, n=curve_full)[0]
    mc.parent(curve_full, parent)
    mc.hide(curve_full)

    # Remove orig shapes
    mc.delete(mc.ls(mc.listRelatives(curve_full, s=1), io=1))

    # Make nuls for each of the rotate controls and connect the rotates.
    # This is so we only get rotation deforming the curves
    for i in xrange(len(rotate_controls)):
        nul = mc.createNode('transform', n=rotate_controls[i] + '_input', p=rotate_controls[i])
        mc.delete(mc.parentConstraint(rotate_controls[i], nul))
        mc.connectAttr(rotate_controls[i]+'.r', nul+'.r')
        if not i:
            top_nul = mc.duplicate(nul, n=name+'_rotate_input')[0]
            mc.parent(nul, top_nul)
            mc.parent(top_nul, parent)
        else:
            mc.parent(nul, lastNul)
        lastNul = nul

    # Create clusters to rotate the cvs
    for i in no_rotate_cvs:
        cluster, handle = mc.cluster(curve_full + '.cv[{}]'.format(i),
                                     name=name + '_no_rotate_cluster_{}'.format(i))
        rigrepo.libs.cluster.localize(cluster, parent, parent,
                                      weightedCompensation=True)
        mc.parent(handle, nul)
        mc.hide(handle)

    # Create scale pivot
    pos = mc.pointPosition(curve + '.cv[0]')
    scale_pivot = mc.createNode('transform', n=name + '_scale_pivot', p=parent)
    mc.xform(scale_pivot, ws=1, t=pos)

    # Create position output nul, this will be the parent of everything that is a child of the spine
    # that needs to move with the length change
    pos_output_parent = mc.listRelatives(position_output_child, p=1)[0]
    pos_output_nul = mc.createNode('transform', n=position_output_child + '_length_input', p=pos_output_parent)

    # Create position constraint target, that is child of the scale pivot
    position_constraint_target = mc.duplicate(pos_output_nul, n=name + '_translate_constraint_target')[0]
    mc.parent(position_constraint_target, scale_pivot)

    # Put the output child under the newly created node so everything moves with it
    mc.parent(position_output_child, pos_output_nul)

    # Create output nuls for the translate
    position_constraint_base_nul = mc.duplicate(position_constraint_target, n=name + '_translate_output_nul')[0]
    mc.parent(position_constraint_base_nul, parent)
    position_constraint_base = mc.createNode('transform', n=name + '_translate_output',
                                             p=position_constraint_base_nul)

    # Translate output constraint
    mc.pointConstraint(position_constraint_target, position_constraint_base)

    # connect the constrained nul to the position output nul
    mc.connectAttr(position_constraint_base + '.t', pos_output_nul + '.t')

    # Create scale cluster
    scale_cluster, scale_cluster_handle = mc.cluster(curve, n=name + '_scale_cluster')
    mc.hide(scale_cluster_handle)
    mc.parent(scale_cluster_handle, scale_pivot)
    rigrepo.libs.cluster.localize(scale_cluster, parent, parent,
                                  weightedCompensation=True)

    # Move scale cluster to front of deformation order
    tweak = mc.ls(mc.listHistory(curve, pdo=1, il=2), type='tweak')[0]
    mc.reorderDeformers(tweak, scale_cluster, curve)

    # Curve infos for measuring length
    info_full = mc.createNode('curveInfo', n=name + '_full_curveInfo')
    mc.connectAttr(curve_full + '.local', info_full + '.inputCurve')

    # Divide distances
    length_mul = mc.createNode('multiplyDivide', n=name + '_length_divide')
    mc.setAttr(length_mul + '.operation', 2)
    arc_length = mc.getAttr(info_full+'.arcLength')
    mc.setAttr(length_mul+'.input1X', arc_length)
    mc.connectAttr(info_full + '.arcLength', length_mul + '.input2X')

    # Add length preservation dial attribute
    mc.addAttr(primary_control, ln='preserveLength', min=0, max=1, dv=1, at='double', k=1)

    # Add diagnostic attributes
    #   Current Length
    mc.addAttr(primary_control, ln='currentLength', min=0, max=1, dv=1, at='double')
    mc.setAttr(primary_control + '.currentLength', cb=1)
    comp_mul = mc.createNode('multiplyDivide', n=name + '_current_length_mul')
    mc.setAttr(comp_mul + '.operation', 2)
    arc_length = mc.getAttr(info_full+'.arcLength')
    mc.setAttr(comp_mul+'.input2X', arc_length)
    info_main = mc.ls(mc.listConnections(mc.listRelatives(curve, s=1, ni=1)[0]), type='curveInfo')[0]
    mc.connectAttr(info_main+'.arcLength', comp_mul+'.input1X')
    mc.connectAttr(comp_mul + '.outputX', primary_control + '.currentLength')
    #   Compensated Length
    mc.addAttr(primary_control, ln='compensatedLength', min=0, max=1, dv=1, at='double')
    mc.setAttr(primary_control + '.compensatedLength', cb=1)
    mc.connectAttr(length_mul + '.outputX', primary_control+'.compensatedLength')

    # Create blend node for dial attribute
    blend = mc.createNode('blendTwoAttr', n=name + '_attr_blend')
    mc.connectAttr(primary_control + '.preserveLength', blend + '.attributesBlender')
    mc.setAttr(blend + '.input[0]', 1)
    mc.connectAttr(length_mul + '.outputX', blend + '.input[1]')

    # Connect the blend output to the scale pivot
    mc.connectAttr(blend + '.output', scale_pivot + '.sy')


