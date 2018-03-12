'''
This is the base module for all of your parts.
'''
import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.ikfk 
import rigrepo.libs.control
import rigrepo.libs.common

class Foot(part.Part):
    '''
    '''
    def __init__(self, name, jointList, ankleHandle, fkAnchor, ikAnchor='ankle_l_bind_ik_offset', 
                anklePivot='ankle_l_pivot', ankleStretchTarget="ankle_l_bind_ik_tgt", ikfkGroup=None):
        '''
        This is the constructor for the foot. We will initialize all of the attributes for this
        object in the constructor.

        :param name: What you wish to call this part.
        :type name: str

        :param jointList: List of bind joints you wish to use for the foot.
        :type jointList: list | tuple

        :param ankleHandle: Handle that is being used for the leg you're attaching the ankle to.
        :type ankleHanlde: str

        :param fkAnchor: The node that will be driving the fk setup of the rig.
        :type fkAnchor: str

        :param ikAnchor: The node that will be driving the ik setup of the rig.
        :type ikAnchor: str

        :param anklePivot: The parent of all the pivots you will be using to create the foot rig.
        :type anklePivot: str

        :param ankleStretchTarget: This is the node being used to measure the stretch.
        :type ankleStretchTarget: str

        :param ikfkGroup: The name of the group that may already exists for the leg that you can put
                        this setup into. If there isn't one, then we will make one for the foot.
        :type ikfkGroup: str
        '''
        super(Foot, self).__init__(name)

        # We need pivots to be able to build the system.
        if len(jointList) != 3:
            raise RuntimeError("""{0} must be an array of 3 elements
                that exists in Maya.""".format(jointList))

        self._anklePivot = anklePivot
        self._ankleHandle = ankleHandle
        self._jointList = jointList
        
        self._ikAnchor = ikAnchor
        self._fkAnchor = fkAnchor
        self.ikfkSystem = None

        self.addAttribute("anklePivot", anklePivot, attrType=str)
        self.addAttribute("ankleHandle", ankleHandle, attrType=str)
        self.addAttribute("jointList", jointList, attrType=list)
        self.addAttribute("ikAnchor", ikAnchor, attrType=str)
        self.addAttribute("fkAnchor", fkAnchor, attrType=str)
        self.addAttribute("ikfkGroup", ikfkGroup, attrType=str)
        self.addAttribute("ankleStretchTarget",ankleStretchTarget, attrType=str)
        
    def build(self):
        '''
        This is where the construction of the rig is executed.
        '''
        # currently I am getting all of the attributes and setting them to class attributes. I will
        # get rid of these at some point and just have the class call the node attributes instead.
        self._anklePivot = self.getAttributeByName("anklePivot").getValue()
        self._ankleHandle = self.getAttributeByName("ankleHandle").getValue()
        self._jointList = self.getAttributeByName("jointList").getValue()
        self._ikAnchor = self.getAttributeByName("ikAnchor").getValue()
        self._fkAnchor = self.getAttributeByName("fkAnchor").getValue()
        ikfkGroup = self.getAttributeByName("ikfkGroup").getValue()
        ankleStretchTarget=self.getAttributeByName("ankleStretchTarget").getValue()

        if not mc.objExists(self._anklePivot):
            raise RuntimeError("{0} doesn't exist in the current Maya seesion.".format(self._anklePivot))

        if not mc.objExists(self._ankleHandle):
            raise RuntimeError("{0} doesn't exist in the current Maya seesion.".format(self._ankleHandle))

        self.ikfkSystem = rigrepo.libs.ikfk.IkFkFoot(self._jointList, self._anklePivot)

        if ikfkGroup:
            if mc.objExists(ikfkGroup):
                self.ikfkSystem.setGroup(ikfkGroup)

        # run the super method first.
        super(Foot, self).build()

        # This will create the ikfk system for the foot.
        self.ikfkSystem.create()
        # get all of the pivots
        pivotList = self.ikfkSystem.pivotList

        if mc.objExists(ankleStretchTarget):
            mc.parent(ankleStretchTarget, pivotList[-2])

        #parent the ankle handle to the pivot hierarchy
        if mc.objExists(self._ikAnchor):
            mc.parent(self._anklePivot, self._ikAnchor)

        # get blend joint list
        blendJointList = self.ikfkSystem.getBlendJointList()

        # loop through and connect original joint list to the blend joints
        for blendJoint, joint in zip(blendJointList[1:], self._jointList[1:]):
            mc.pointConstraint(blendJoint, joint)
            mc.orientConstraint(blendJoint, joint)

        #-------------------------------------------------------------------------------------------
        #FK SETUP
        #-------------------------------------------------------------------------------------------
        # get the fk joint list from the ikfk system
        fkJointList = self.ikfkSystem.getFkJointList()

        # create the ball fk control
        ballFkctrlHierarchy = rigrepo.libs.control.create("{}_ctrl".format(fkJointList[1]), 
                                                            controlType = "cube", 
                                                            hierarchy=['nul'])

        rigrepo.libs.attribute.lockAndHide(ballFkctrlHierarchy[-1],
                                            ['v', 'sx','sy','sz'])

        # position the ball control
        ballJointMatrix = mc.xform(fkJointList[1], q=True, ws=True, matrix=True)
        mc.xform(ballFkctrlHierarchy[0], ws=True, matrix=ballJointMatrix)
        mc.pointConstraint(ballFkctrlHierarchy[-1], fkJointList[1])
        mc.orientConstraint(ballFkctrlHierarchy[-1], fkJointList[1])

        # create the toe fk control
        toeFkctrlHierarchy = rigrepo.libs.control.create("{}_ctrl".format(fkJointList[2]), 
                                                            controlType = "cube", 
                                                            hierarchy=['nul'], 
                                                            parent= ballFkctrlHierarchy[-1])
        
        rigrepo.libs.attribute.lockAndHide(toeFkctrlHierarchy[-1],
                                            ['v', 'sx','sy','sz'])

        toeJointMatrix = mc.xform(fkJointList[2], q=True, ws=True, matrix=True)
        mc.xform(toeFkctrlHierarchy[0], ws=True, matrix=toeJointMatrix)
        mc.pointConstraint(toeFkctrlHierarchy[-1], fkJointList[2])
        mc.orientConstraint(toeFkctrlHierarchy[-1], fkJointList[2])


        if mc.objExists(self._fkAnchor):
            mc.parent(ballFkctrlHierarchy[0], self._fkAnchor)
        parent = None

        #-------------------------------------------------------------------------------------------
        #IK SETUP
        #-------------------------------------------------------------------------------------------
        pivotPos = mc.xform(self._anklePivot, q=True, ws=True, t=True)[0]
        # create controls for our pivot, the last index is the control
        pivotSide = mc.xform(self._jointList[0], q=True, ws=True, t=True)[0]
        # we will have to come up with a better way to handle this. Maybe make an attribue 
        # that a user can change.
        bankCtrlName = "bank_l_ctrl"
        if pivotPos < .01:
            bankCtrlName = "bank_r_ctrl"

        bankctrlHierarchy = rigrepo.libs.control.create(bankCtrlName, 
                                                controlType = "cube", 
                                                hierarchy=['nul', 'ort'],
                                                parent=self._anklePivot,
                                                color=rigrepo.libs.common.RED)
        # get the ball pivot position
        ballJntTrs = mc.xform(self._jointList[1], q=True, ws=True, t=True)
        mc.xform(bankctrlHierarchy[0], ws=True, t=ballJntTrs)

        #lock all attributes except for translateX
        rigrepo.libs.attribute.lockAndHide(bankctrlHierarchy[-1],['ty','tz','v','rx','ry','rz','sx','sy','sz'])

        # create the remap and multDoubleLinear node.
        bankRemapNode = mc.createNode("remapValue", name="{}_remap".format(bankctrlHierarchy[-1]))
        bankMdl = mc.createNode("multDoubleLinear", n="{}_invert_mdl".format(bankctrlHierarchy[-1]))

        #connect the ctrl.tx to the remap inputValue
        mc.connectAttr("{}.tx".format(bankctrlHierarchy[-1]), "{}.inputValue".format(bankRemapNode))
        ballPivotDistance = mc.getAttr("{}.tx".format(pivotList[1]))

        # set attributes for input/output min/max on the remap node.
        mc.setAttr("{}.inputMin".format(bankRemapNode), ballPivotDistance*-1)
        mc.setAttr("{}.inputMax".format(bankRemapNode), ballPivotDistance)
        mc.setAttr("{}.outputMin".format(bankRemapNode), -180)
        mc.setAttr("{}.outputMax".format(bankRemapNode), 180)
        mc.connectAttr("{}.outValue".format(bankRemapNode), "{}.input1".format(bankMdl))
        mc.setAttr("{}.input2".format(bankMdl), -1)

        for pivot in pivotList:
            # if the pivot is a joint, we want to turn off it's joint display
            if mc.nodeType(pivot) == "joint":
                mc.setAttr("{}.drawStyle".format(pivot), 2)

            # if it's certain pivots in the order we want to not make controls.
            if pivot in [pivotList[0], pivotList[1], pivotList[3]]:
                if pivot == pivotList[0]:
                    # create the control hierarchy
                    if  pivotPos > .01:
                        mc.transformLimits(pivot, rz=(0,0), erz=(1,0))
                        mc.connectAttr("{}.output".format(bankMdl), "{}.rz".format(pivot))
                    else:
                        mc.transformLimits(pivot, rz=(0,0), erz=(0,1))
                        mc.connectAttr("{}.outValue".format(bankRemapNode), "{}.rz".format(pivot))
                elif pivot == pivotList[1]:
                    # create the control hierarchy
                    if  pivotPos > .01:
                        mc.transformLimits(pivot, rz=(0,0), erz=(0,1))
                        mc.connectAttr("{}.output".format(bankMdl), "{}.rz".format(pivot))
                    else:
                        mc.transformLimits(pivot, rz=(0,0), erz=(1,0))
                        mc.connectAttr("{}.outValue".format(bankRemapNode), "{}.rz".format(pivot))
                
                parent = pivot
                continue

            # create the control hierarchy
            pivotctrlHierarchy = rigrepo.libs.control.create("{}_ctrl".format(pivot), 
                                                            controlType = "cube", 
                                                            hierarchy=['nul'])

            rigrepo.libs.attribute.lockAndHide(pivotctrlHierarchy[-1],
                                            ['tx', 'ty','tz','v','sx','sy','sz'])

            pivotMatrix = mc.xform(pivot, q=True, ws=True, matrix=True)
            mc.xform(pivotctrlHierarchy[0], ws=True, matrix=pivotMatrix)
            mc.parent(pivot, pivotctrlHierarchy[-1])

            if parent:
                mc.parent(pivotctrlHierarchy[0], parent)

            if pivot == pivotList[-2]:
                continue

            parent = pivot

        # turn of the joint display on the anklePivot
        if mc.nodeType(self._anklePivot) == "joint":
                mc.setAttr("{}.drawStyle".format(self._anklePivot), 2)