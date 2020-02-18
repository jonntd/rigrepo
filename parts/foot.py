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
                anklePivot='ankle_l_pivot', ankleStretchTarget="ankle_l_bind_ik_tgt", ikfkGroup=None, paramNodeName=None):
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
        if not paramNodeName:
            paramNodeName = ""
        self.addAttribute("paramNode", paramNodeName, attrType=str)
        
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
        paramNode = self.getAttributeByName("paramNode").getValue()
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

        # parent the ankle stretch target
        if mc.objExists(ankleStretchTarget):
            mc.parent(ankleStretchTarget, pivotList[-2])

        # parent the ankle handle to the pivot hierarchy
        if mc.objExists(self._ikAnchor):
            mc.parent(self._anklePivot, self._ikAnchor)
            ikJointList = self.ikfkSystem.getIkJointList()
            #mc.pointConstraint(ankleStretchTarget, ikJointList[0])


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
        try:
            mc.parentConstraint(self._fkAnchor, fkJointList[0])
        except:
            print "{} is already connected.".format(fkJointList[0])

        # create the ball fk control
        ballFkctrlHierarchy = rigrepo.libs.control.create("{}".format("".join(fkJointList[1].split("_bind"))), 
                                                            controlType = "cube", 
                                                            hierarchy=['nul','ort'],
                                                            transformType="joint")

        rigrepo.libs.attribute.lockAndHide(ballFkctrlHierarchy[-1],
                                            ['v', 'tx','ty','tz','sx','sy','sz'])

        # position the ball control
        ballJointMatrix = mc.xform(fkJointList[1], q=True, ws=True, matrix=True)
        mc.pointConstraint(self._fkAnchor,ballFkctrlHierarchy[0], mo=False)
        mc.xform(ballFkctrlHierarchy[1], ws=True, matrix=ballJointMatrix)
        #mc.pointConstraint(ballFkctrlHierarchy[-1], fkJointList[1])
        mc.orientConstraint(ballFkctrlHierarchy[-1], fkJointList[1])
        mc.parent(ballFkctrlHierarchy[0], self.name)


        #if mc.objExists(self._fkAnchor):
        #    mc.parent(ballFkctrlHierarchy[0], self._fkAnchor)
        # create the toe fk control
        # TAKING OUT THE TOE FK CONTROL FOR NOW.
        '''
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
        '''
        
        #-------------------------------------------------------------------------------------------
        #IK SETUP
        #-------------------------------------------------------------------------------------------
        pivotPos = mc.xform(self._anklePivot, q=True, ws=True, t=True)[0]
        # create controls for our pivot, the last index is the control
        pivotSide = mc.xform(self._jointList[0], q=True, ws=True, t=True)[0]
        # we will have to come up with a better way to handle this. Maybe make an attribue 
        # that a user can change.
        bankCtrlName = "bank_l"
        if pivotPos < .01:
            bankCtrlName = "bank_r"

        bankctrlHierarchy = rigrepo.libs.control.create(bankCtrlName, 
                                                controlType = "cube", 
                                                hierarchy=['nul', 'ort'],
                                                parent=self._anklePivot,
                                                color=rigrepo.libs.common.RED)
        ikControlList = [bankctrlHierarchy[-1]]
        # get the ball pivot position
        ballJntTrs = mc.xform(self._jointList[1], q=True, ws=True, t=True)
        mc.xform(bankctrlHierarchy[0], ws=True, t=ballJntTrs)

        #lock all attributes except for translateX
        rigrepo.libs.attribute.lockAndHide(bankctrlHierarchy[-1],['ty','v','rx','ry','rz','sx','sy','sz'])

        # create the remap and multDoubleLinear node.
        bankRemapNode = mc.createNode("remapValue", name="{}_remap".format(bankctrlHierarchy[-1]))
        bankMdl = mc.createNode("multDoubleLinear", n="{}_invert_mdl".format(bankctrlHierarchy[-1]))

        #connect the ctrl.tx to the remap inputValue
        mc.connectAttr("{}.tx".format(bankctrlHierarchy[-1]), "{}.inputValue".format(bankRemapNode))
        ballPivotDistance = mc.getAttr("{}.tx".format(pivotList[1]))

        # set attributes for input/output min/max on the remap node.
        mc.setAttr("{}.inputMin".format(bankRemapNode), (ballPivotDistance * 2)*-1)
        mc.setAttr("{}.inputMax".format(bankRemapNode), (ballPivotDistance * 2))
        mc.setAttr("{}.outputMin".format(bankRemapNode), -180)
        mc.setAttr("{}.outputMax".format(bankRemapNode), 180)
        mc.connectAttr("{}.outValue".format(bankRemapNode), "{}.input1".format(bankMdl))
        mc.setAttr("{}.input2".format(bankMdl), -1)
        parent = None
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
                        mc.transformLimits(pivot, rz=(0,0), erz=(1,0))
                        mc.connectAttr("{}.outValue".format(bankRemapNode), "{}.rz".format(pivot))
                        mc.setAttr("{}.sz".format(bankctrlHierarchy[-2]), -1)
                elif pivot == pivotList[1]:
                    # create the control hierarchy
                    if  pivotPos > .01:
                        mc.transformLimits(pivot, rz=(0,0), erz=(0,1))
                        mc.connectAttr("{}.output".format(bankMdl), "{}.rz".format(pivot))
                    else:                        
                        mc.transformLimits(pivot, rz=(0,0), erz=(0,1))
                        mc.connectAttr("{}.outValue".format(bankRemapNode), "{}.rz".format(pivot))
                
                parent = pivot
                continue

            pivotctrlHierarchy = rigrepo.libs.control.create("{}_ctrl".format(pivot), 
                                                            controlType = "cube", 
                                                            hierarchy=['nul'])

            # create the control hierarchy
            if pivot == pivotList[-1]:
                mc.deleteAttr("{}.__control__".format(pivotctrlHierarchy[-1]))
                mc.delete(mc.listRelatives(pivotctrlHierarchy[-1],c=True,shapes=True))
            rigrepo.libs.attribute.lockAndHide(pivotctrlHierarchy[-1],
                                            ['tx', 'ty','tz','v','sx','sy','sz'])

            pivotMatrix = mc.xform(pivot, q=True, ws=True, matrix=True)
            mc.xform(pivotctrlHierarchy[0], ws=True, matrix=pivotMatrix)
            mc.parent(pivot, pivotctrlHierarchy[-1])

            ikControlList.append(pivotctrlHierarchy[-1])

            if parent:
                mc.parent(pivotctrlHierarchy[0], parent)

            if pivot == pivotList[-2]:
                continue

            parent = pivot

        # turn of the joint display on the anklePivot
        if mc.nodeType(self._anklePivot) == "joint":
                mc.setAttr("{}.drawStyle".format(self._anklePivot), 2)
        handles = self.ikfkSystem.getHandles()
        # turn off the visibility of handles
        for handle in handles:
            mc.setAttr("{}.v".format(handle), 0)

        # create setDriven keys for the ball roll
        bankCtrl = bankctrlHierarchy[-1]
        ballNul = mc.listRelatives(ikControlList[-2], p=True)[0]
        heelNul = mc.listRelatives(ikControlList[-4], p=True)[0]
        toeNul = mc.listRelatives(ikControlList[-3], p=True)[0]
        mc.setDrivenKeyframe("{}.rx".format(ballNul), cd="{}.tz".format(bankCtrl), v=0, dv=0)
        mc.setDrivenKeyframe("{}.rx".format(ballNul), cd="{}.tz".format(bankCtrl), v=60, dv=5)
        mc.setDrivenKeyframe("{}.rx".format(ballNul), cd="{}.tz".format(bankCtrl), v=0, dv=10)
        mc.setDrivenKeyframe("{}.rx".format(heelNul), cd="{}.tz".format(bankCtrl), v=0, dv=0)
        mc.setDrivenKeyframe("{}.rx".format(heelNul), cd="{}.tz".format(bankCtrl), v=-90, dv=-10)
        mc.setDrivenKeyframe("{}.rx".format(toeNul), cd="{}.tz".format(bankCtrl), v=0, dv=5)
        mc.setDrivenKeyframe("{}.rx".format(toeNul), cd="{}.tz".format(bankCtrl), v=90, dv=10)
               

        # if the param node that is past in exists then we will add attributes to it.
        # if not, we will make one of our own and put them on the controls
        ikfkAttr ="{}.ikfk".format(paramNode)
        if not mc.objExists(paramNode):
            paramNode = mc.createNode("locator", name=paramNodeName)
            paramNodeTrs = mc.listRelatives(paramNode, p=True)[0]
            mc.select(cl=True)
            # lock and hide attributes on the Param node that we don't need.
            rigrepo.libs.attribute.lockAndHide(paramNode, ['lpx','lpy','lpz','lsx','lsy','lsz'])

            mc.setAttr("{0}.v".format(paramNode), 0)
            mc.addAttr(paramNode, ln="ikfk", at="double", min=0, max=1, dv=0, keyable=True)

        # create ikfk reverse node to connect the ikfk attribute
        reverseNode = mc.createNode("reverse", name="{0}_rvr".format(self.name))
        mc.connectAttr(ikfkAttr, "{0}.inputX".format(reverseNode), f=True)

        cst=mc.parentConstraint(pivotList[-3], self._fkAnchor, ballFkctrlHierarchy[1], mo=True)[0]
        weightAlias = mc.parentConstraint(cst,q=True,wal=True)
        mc.connectAttr(ikfkAttr, "{}.{}".format(cst,weightAlias[1]), f=True)
        mc.connectAttr("{}.outputX".format(reverseNode), "{}.{}".format(cst,weightAlias[0]), f=True)
        mc.parent(handles[-1],w=True)
        mc.xform(pivotList[-1], ws=True, matrix=mc.xform(ballFkctrlHierarchy[-1], q=True, ws=True, matrix=True))
        mc.parent(handles[-1], pivotList[-1])
        mc.orientConstraint(ballFkctrlHierarchy[-1], pivotList[-1], mo=True)

        # create the offset joint for the matching to work
        ballOffsetJoint = mc.joint(name="{}_offset".format(ikControlList[-1]))
        mc.setAttr("{}.v".format(ballOffsetJoint), 0)
        mc.parent(ballOffsetJoint, ballFkctrlHierarchy[-1])
        mc.xform(ballOffsetJoint, ws=True, matrix=mc.xform(ikControlList[-1], q=True, ws=True, matrix=True))

        #------------------------------------------------------------------------------------------
        #Setup attributes on the param node for the ikfk switch.
        #------------------------------------------------------------------------------------------
        # fk match attributes needed to the switch
        mc.addAttr(paramNode, ln="footFkMatchTransform", dt="string")
        mc.setAttr("{}.footFkMatchTransform".format(paramNode), 
                '"{0}"'.format(ballOffsetJoint), 
                type="string")

        mc.addAttr(paramNode, ln="footFkControl", dt="string")
        mc.setAttr("{}.footFkControl".format(paramNode), 
                '"{0}"'.format(ballFkctrlHierarchy[-1]), 
                type="string")

        # ik match attributes needed for the switch
        mc.addAttr(paramNode, ln="footIkMatchTransform", dt="string")
        mc.setAttr("{}.footIkMatchTransform".format(paramNode), 
                '"{0}"'.format(ikJointList[1]), 
                type="string")
        mc.addAttr(paramNode, ln="footIkControls", dt="string")
        mc.setAttr("{}.footIkControls".format(paramNode), 
                '["{0}","{1}","{2}","{3}","{4}"]'.format(*ikControlList), 
                type="string")

        # command to be called when switch is being used.
        mc.addAttr(paramNode, ln="footSwitchCommand", dt="string")
        mc.setAttr("{}.switchCommand".format(paramNode), "rigrepo.parts.foot.Foot.switch", 
                    type="string")

        # --------------------
        # Foot Scale
        # --------------------
        # Turn off scale compensate on children of bind joint
        children = mc.listRelatives(self._jointList[0], c=1, type='joint')
        if children:
            for c in children:
                mc.setAttr(c+'.segmentScaleCompensate', 0)

    def postBuild(self):
        '''
        '''
        for joint in (self.ikfkSystem.getFkJointList()[0], self.ikfkSystem.getBlendJointList()[0], self.ikfkSystem.getIkJointList()[0]):
            mc.setAttr("{}.v".format(joint), 0)


    @staticmethod
    def switch(paramNode, value):
        '''
        This will handle the switching between the fk and ik control
        :param paramNode: Param node that is holding the data for the switch
        :type paramNode: str

        :param value: The value of the switch bewteen ik and fk
        :type value: int
        '''
        if not mc.objExists(paramNode):
            raise RuntimeError("{} doesn't exist in the current Maya session".format(paramNode))
        # if we're in ik modes, we will match fk to the ik position and switch it to fk
        mc.undoInfo(openChunk=1)
        if value == 0:
            fkControl = eval(mc.getAttr("{}.footFkControl".format(paramNode)))
            ikMatchTransform = eval(mc.getAttr("{}.footIkMatchTransform".format(paramNode)))
            mc.xform(fkControl, ws=True, matrix=mc.xform(ikMatchTransform, q=True, ws=True, matrix=True))
            mc.setAttr("{}.ikfk".format(paramNode), 1)
        elif value == 1:
            # get the ik controls
            ikControls = eval(mc.getAttr("{}.footIkControls".format(paramNode)))
            # get the fk transforms
            fkMatchTransform = eval(mc.getAttr("{}.footFkMatchTransform".format(paramNode)))
            for control in ikControls:
                attrs = mc.listAttr(control, keyable=True)
                for attr in attrs:
                    mc.setAttr("{}.{}".format(control, attr), 0)
            mc.xform(ikControls[-1], ws=True, matrix=mc.xform(fkMatchTransform, q=True, ws=True, matrix=True))
            mc.setAttr("{}.ikfk".format(paramNode), 0)
        mc.undoInfo(closeChunk=1)
