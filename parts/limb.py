'''
This is the limb base class.

Anything that uses a three joint chain ik/fk setup
should start with this class.
'''

import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.ikfk
import rigrepo.libs.control
import rigrepo.libs.attribute
import rigrepo.libs.common
import rigrepo.libs.joint
reload(rigrepo.libs.ikfk)



class Limb(part.Part):
    '''
    '''
    def __init__(self, name, jointList, anchor=None, dataObj=None, side="l"):
        '''
        This is the constructor.
        '''
        super(Limb, self).__init__(name, dataObj) 
        self._fkControls = list()
        self._ikControls = list()
        self._anchorGrp = str()
        self.addAttribute("anchor", anchor, attrType=str)
        self.addAttribute("side", side, attrType=str)
        self.addAttribute("fkControls", ["{}_shoulder".format(side),
                                        "{}_elbow".format(side), 
                                        "{}_wrist".format(side)], 
                            attrType=list)
        self.addAttribute("ikControls", ["{}_limb_pv".format(side),
                                        "{}_limb_ik".format(side)],
                            attrType=list)
        side.capitalize()
        self.addAttribute("paramNode", "limb_{}".format(side.capitalize()), attrType=str)
        self.jointList = jointList
        self._stretchTargetJointList = list()

    def build(self):
        '''
        This will build the limb part
        '''
        side = self.getAttributeByName("side").getValue()
        paramNodeName = self.getAttributeByName("paramNode").getValue()
        fkControlNames = self.getAttributeByName("fkControls").getValue()
        ikControlNames = self.getAttributeByName("ikControls").getValue()

        super(Limb, self).build()

        # create the param node and ikfk attribute for it
        paramNode = mc.createNode("locator", name=paramNodeName)
        paramNodeTrs = mc.listRelatives(paramNode, p=True)[0]
        mc.select(cl=True)
        grp = mc.createNode("transform", name="{}_ikfk_grp".format(self.name))
        mc.parent(grp, self.name)
        # lock and hide attributes on the Param node that we don't need.
        rigrepo.libs.attribute.lockAndHide(paramNode, ['lpx','lpy','lpz','lsx','lsy','lsz'])

        mc.setAttr("{0}.v".format(paramNode), 0)
        mc.addAttr(paramNode, ln="ikfk", at="double", min=0, max=1, dv=0, keyable=True)

        mc.addAttr(grp, ln="ikfk", at="double", min=0, max=1, dv=0, keyable=True)
        ikfkAttr = "{0}.ikfk".format(paramNode)

        mc.connectAttr(ikfkAttr, "{0}.ikfk".format(grp), f=True)


        # create ikfk reverse node to connect the ikfk attribute
        reverseNode = mc.createNode("reverse", name="{0}_rvr".format(self.name))
        mc.connectAttr(ikfkAttr, "{0}.inputX".format(reverseNode), f=True)

        #-------------------------------------------------------------------------------------------
        #FK Setup for the limb
        #-------------------------------------------------------------------------------------------
        fkControlsNulList = list()
        parent = grp
        for jnt, fkCtrl in zip(self.jointList,fkControlNames):
            # create the fk control hierarchy
            fkCtrlHierarchy = rigrepo.libs.control.create(name=fkCtrl, 
                                                controlType="cube",
                                                hierarchy=[],
                                                transformType="joint",
                                                hideAttrs=["tx", "ty", "tz", "sx", "sy", "sz", "v"])

            ctrl = fkCtrlHierarchy[0]

            # make sure that the control is in the same position as the joint
            fkJntMatrix = mc.xform(jnt, q=True, ws=True, matrix=True)
            mc.xform(ctrl, ws=True, matrix=fkJntMatrix)

            # setup the constraints from the control to the joint
            mc.pointConstraint(ctrl, jnt)
            mc.orientConstraint(ctrl, jnt)

            # add the param node to the control and connect it
            mc.parent(paramNode, ctrl, add=True, s=True, r=True)

            #parent the control to the parent node
            mc.parent(ctrl,parent)
            parent = ctrl
            mc.connectAttr(ikfkAttr, "{0}.v".format(ctrl), f=True)
            self._fkControls.append(str(ctrl))


        rigrepo.libs.joint.rotateToOrient(self._fkControls)
        mc.setAttr("{}.preferredAngleZ".format(self._fkControls[1]), -90)

        
        handle = mc.ikHandle(sj=self._fkControls[0],  ee=self._fkControls[-1], 
                                        sol="ikRPsolver", 
                                        name="{0}_hdl".format(self._fkControls[-1]))[0]

        poleVectorPos = rigrepo.libs.ikfk.IKFKLimb.getPoleVectorFromHandle(handle, self._fkControls)

        pvCtrlHierarchy = rigrepo.libs.control.create(name=ikControlNames[0], 
                                                controlType="diamond",
                                                hierarchy=['nul','ort'],
                                                position=poleVectorPos,
                                                hideAttrs=["v", "rx", "ry", "rz", "sx", "sy", "sz"],
                                                color=rigrepo.libs.common.GREEN)

        # get the handle and pv control
        pvCtrl = pvCtrlHierarchy[-1]
        mc.parent(paramNode, pvCtrl, s=True, r=True)
        mc.poleVectorConstraint(pvCtrl, handle)

        # set the pvMatch node attribute on the paramNode
        mc.addAttr(paramNode, ln="pvMatch", dt="string")
        pvMatchNode = mc.duplicate(pvCtrl, po=True, rr=True, name="{}_match".format(pvCtrl))[0]
        mc.setAttr("{}.pvMatch".format(paramNode), pvMatchNode, type="string")

        mc.parent(pvMatchNode, self._fkControls[0])



        # set the parent of the controls to be the rig group
        parent = grp

        endJointPos = mc.xform(self._fkControls[-1], q=True, ws=True, t=True)
        ikCtrlHierarchy = rigrepo.libs.control.create(name=ikControlNames[1], 
                                                controlType="cube",
                                                hierarchy=['nul','ort'],
                                                position=endJointPos,
                                                color=rigrepo.libs.common.GREEN)     

        ikCtrl = ikCtrlHierarchy[-1]
        mc.parent(paramNode, ikCtrl, add=True, s=True, r=True)
        


        # duplicate the end ik joint and make it offset joint for the 
        # ik control to drive the end joint
        mc.select(clear=True)
        tempJnt = mc.joint(name="{}_offset_temp".format(self._fkControls[-1]))
        dupEndJnt = mc.joint(name="{}_offset".format(self._fkControls[-1]))
        tempUpJnt = mc.joint(name="{}_offset_tempUp".format(self._fkControls[-1]))
        mc.parent(tempUpJnt, tempJnt)
        mc.xform(tempJnt, ws=True, matrix=mc.xform(self._fkControls[-1], q=True, ws=True, matrix=True))
        mc.setAttr('{0}.tx'.format(tempUpJnt),mc.getAttr('{0}.tz'.format(dupEndJnt))+2)
        mc.setAttr('{0}.tx'.format(dupEndJnt),mc.getAttr('{0}.tx'.format(dupEndJnt))+2)
        mc.delete(mc.aimConstraint(dupEndJnt, ikCtrl, wut="object", wuo=tempUpJnt)[0], )
        mc.setAttr('{0}.drawStyle'.format(dupEndJnt), 2)
        mc.setAttr("{0}.v".format(handle), 0)
        mc.parent(dupEndJnt,ikCtrl)
        mc.setAttr("{0}.t".format(dupEndJnt),0,0,0)
        cst = mc.orientConstraint(dupEndJnt, self.jointList[-1])[0]
        wal = mc.orientConstraint(cst, q=True, wal=True)
        mc.parent(handle, dupEndJnt)
        mc.delete(tempJnt)

        # connect the switch to the constraint on the wrist
        mc.connectAttr("{0}.outputX".format(reverseNode), "{}.{}".format(cst, wal[1]), f=True)
        mc.connectAttr(ikfkAttr, "{}.{}".format(cst, wal[0]), f=True)

        # parent the controls to the parent group
        mc.parent((pvCtrlHierarchy[0],ikCtrlHierarchy[0]), parent)

        self._ikControls.extend([str(pvCtrl), str(ikCtrl)])

        # setup the visibility and switch
        for ctrl in self._ikControls:
            if not mc.isConnected("{0}.outputX".format(reverseNode), "{0}.v".format(ctrl)):
                mc.connectAttr("{0}.outputX".format(reverseNode), "{0}.v".format(ctrl), f=True)

        mc.connectAttr("{0}.outputX".format(reverseNode), "{0}.ikBlend".format(handle), f=True)
        
        # create the offset joint that will be used for ikfk switching. This is the offset of the
        # ik control from the fk control
        mc.select(clear=True)
        fkOffsetJnt = mc.joint(name="{}_offset".format(ikCtrl))
        mc.xform(fkOffsetJnt, ws=True, matrix=mc.xform(ikCtrl, q=True, ws=True, matrix=True))
        # turn off the visibility of the offset joint
        mc.setAttr('{0}.drawStyle'.format(fkOffsetJnt), 2)

        # parent the offset joint to the fk wrist control.
        mc.parent(fkOffsetJnt, self._fkControls[-1])

        # make sure the rig is in fk before adding the stretch so it doesn't move the rig
        mc.setAttr(ikfkAttr, 1)

        # create the ik stretchy system
        self._stretchTargetJointList = rigrepo.libs.ikfk.IKFKLimb.createStretchIK(handle, grp)

        #create attributes on param node and connect them to the grp node
        mc.addAttr(paramNode, ln='stretch', at='double', dv = 1, min = 0, max = 1, k=True)
        mc.addAttr(paramNode, ln='stretchTop', at='double', min=0, dv = 1, k=True)
        mc.addAttr(paramNode, ln='stretchBottom', at='double', min=0, dv = 1, k=True)
        mc.addAttr(paramNode, ln='softStretch', at='double', min=0, max=1, dv=0.2, k=True)

        rigrepo.libs.control.tagAsControl(paramNode)

        for attr in ['stretch','stretchTop', 'stretchBottom', 'softStretch']:
            mc.connectAttr('{}.{}'.format(paramNode, attr), 
                        '{}.{}'.format(grp, attr), f=True)

        mc.parent(self._stretchTargetJointList[-1], dupEndJnt)

        # delete the original tranform that came with the locator paramNode
        mc.delete(paramNodeTrs)

        # Connect to passed anchor
        #
        anchor = self.getAttributeByName('anchor').getValue() or ""
        if mc.objExists(anchor):
            anchorGrp = mc.createNode('transform', n=self.name+'_anchor_grp', p=self.name) 
            self._anchorGrp = anchorGrp
            mc.xform(anchorGrp, ws=True, matrix=mc.xform(self.jointList[0], q=True, ws=True, matrix=True))
            mc.parentConstraint(anchor, anchorGrp, mo=1)
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 

        #------------------------------------------------------------------------------------------
        #Setup attributes on the param node for the ikfk switch.
        #------------------------------------------------------------------------------------------
        # fk match attributes needed to the switch
        mc.addAttr(paramNode, ln="fkMatchTransforms", dt="string")
        mc.setAttr("{}.fkMatchTransforms".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(self._fkControls[0], self._fkControls[1], fkOffsetJnt), 
                type="string")

        mc.addAttr(paramNode, ln="fkControls", dt="string")
        mc.setAttr("{}.fkControls".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(*self._fkControls), 
                type="string")

        # ik match attributes needed for the switch
        mc.addAttr(paramNode, ln="ikMatchTransforms", dt="string")
        mc.setAttr("{}.ikMatchTransforms".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(*self.jointList), 
                type="string")
        mc.addAttr(paramNode, ln="ikControls", dt="string")
        mc.setAttr("{}.ikControls".format(paramNode), 
                '["{0}","{1}"]'.format(*self._ikControls), 
                type="string")

        # command to be called when switch is being used.
        mc.addAttr(paramNode, ln="switchCommand", dt="string")
        mc.setAttr("{}.switchCommand".format(paramNode), "rigrepo.parts.limb.Limb.switch", 
                    type="string")

        # set softStretch to zero and zero out fk controls. This will allow the rest of the
        # rig to build properly. We will have to turn these things back on somewhere in the 
        # build later
        # zero out controls
        for control in self._fkControls:
            mc.setAttr("{}.r".format(control), 0, 0, 0)
        # set the param node to zero
        mc.setAttr("{}.softStretch".format(paramNode), .001)
        

    def postBuild(self):
        '''
        '''
        #turn of the visibility of the ikfk system
        #mc.setAttr("{0}.v".format(self.ikfkSystem.getGroup()), 0)

        # NO TWIST JOINT
        side = self.getAttributeByName("side").getValue()
        nameSplit = self.jointList[0].split('_{}_'.format(side))
        noTwist = '{}NoTwist_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        target = self.jointList[1]
        aimVector = (1, 0, 0)
        if side is 'r':
            aimVector = (-1, 0, 0)
        if mc.objExists(noTwist):
            mc.aimConstraint(target, noTwist, mo=1, weight=1, aimVector=aimVector, upVector=(0, 0, 0), worldUpType='none')
        else:
            print('noTwist not found', noTwist)
        # TWIST JOINT
        joint = self.jointList[-1]
        nameSplit = joint.split('_{}_'.format(side))
        twistJoint = '{}Twist_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        if mc.objExists(twistJoint):
            deompose = rigrepo.libs.transform.decomposeRotation(joint)
            mc.connectAttr(joint + '.decomposeTwist', twistJoint + '.rx', f=1)
        else:
            print('No twist joint found', noTwist)

    @staticmethod
    def switch(paramNode, value):
        '''
        '''
        if not mc.objExists(paramNode):
            raise RuntimeError("{} doesn't exist in the current Maya session".format(paramNode))
        # if we're in ik modes, we will match fk to the ik position and switch it to fk
        mc.undoInfo(openChunk=1)
        if value == 0:
            fkControls = eval(mc.getAttr("{}.fkControls".format(paramNode)))
            ikMatchTransforms = eval(mc.getAttr("{}.ikMatchTransforms".format(paramNode)))
            rigrepo.libs.ikfk.IKFKLimb.fkMatchIk(fkControls, ikMatchTransforms)
            mc.setAttr("{}.ikfk".format(paramNode), 1)
        elif value == 1:
            # get the ik controls
            ikControls = eval(mc.getAttr("{}.ikControls".format(paramNode)))
            # get the fk transforms
            fkMatchTransforms = eval(mc.getAttr("{}.fkMatchTransforms".format(paramNode)))
            # get the match node for the pole vector node
            matchNode = mc.getAttr("{}.pvMatch".format(paramNode))
            # get the current distance between the joints
            currentDistance = mc.getAttr("{}.tx".format(fkMatchTransforms[1])) + mc.getAttr("{}.tx".format(fkMatchTransforms[2]))
            # check to see if the distance in negative, which means we have to treat the matching differently
            flip = False
            if currentDistance < 0:
                flip=True
            rigrepo.libs.ikfk.IKFKLimb.ikMatchFk(fkMatchTransforms, ikControls[1], ikControls[0], matchNode)
            mc.setAttr("{}.ikfk".format(paramNode), 0)
            newDistance = mc.getAttr("{}.tx".format(fkMatchTransforms[1])) + mc.getAttr("{}.tx".format(fkMatchTransforms[2]))
            updatedDistance = (newDistance - currentDistance) / 2
            # get the new distance
            # check what direction the delta is in. If we need to flip it we will use abs to match
            if flip:
                if updatedDistance < 0:
                    for attr in ["stretchTop", "stretchBottom"]:
                        mc.setAttr("{}.{}".format(paramNode, attr), mc.getAttr("{}.{}".format(paramNode, attr)) - abs(updatedDistance))
            elif updatedDistance > 0:
                for attr in ["stretchTop", "stretchBottom"]:
                    mc.setAttr("{}.{}".format(paramNode, attr), mc.getAttr("{}.{}".format(paramNode, attr)) - updatedDistance)
            #print "current distance: ", currentDistance, "\nupdated distance: ", updatedDistance, "\nnew distance: ", newDistance

        mc.undoInfo(closeChunk=1)


class LimbOld(part.Part):
    '''
    '''
    def __init__(self, name, jointList, anchor=None, dataObj=None, side="l"):
        '''
        This is the constructor.
        '''
        super(LimbOld, self).__init__(name, dataObj) 
        self._fkControls = list()
        self._ikControls = list()
        self._anchorGrp = str()
        self.addAttribute("anchor", anchor, attrType=str)
        self.addAttribute("side", side, attrType=str)
        self.addAttribute("fkControls", ["{}_shoulder".format(side),
                                        "{}_elbow".format(side), 
                                        "{}_wrist".format(side)], 
                            attrType=list)
        self.addAttribute("ikControls", ["{}_limb_pv".format(side),
                                        "{}_limb_ik".format(side)],
                            attrType=list)
        side.capitalize()
        self.addAttribute("paramNode", "limb_{}".format(side), attrType=str)
        self.jointList = jointList
        self._stretchTargetJointList = list()

    def build(self):
        '''
        This will build the limb part
        '''
        self.ikfkSystem = rigrepo.libs.ikfk.IKFKLimb(self.jointList)
        side = self.getAttributeByName("side").getValue()
        paramNodeName = self.getAttributeByName("paramNode").getValue()
        fkControlNames = self.getAttributeByName("fkControls").getValue()
        ikControlNames = self.getAttributeByName("ikControls").getValue()

        super(Limb, self).build()

        self.ikfkSystem.create()

        # create the param node and ikfk attribute for it
        paramNode = mc.createNode("locator", name=paramNodeName)
        paramNodeTrs = mc.listRelatives(paramNode, p=True)[0]

        # lock and hide attributes on the Param node that we don't need.
        rigrepo.libs.attribute.lockAndHide(paramNode, ['lpx','lpy','lpz','lsx','lsy','lsz'])

        mc.setAttr("{0}.v".format(paramNode), 0)
        mc.addAttr(paramNode, ln="ikfk", at="double", min=0, max=1, dv=0, keyable=True)
        ikfkAttr = "{0}.ikfk".format(paramNode)


        #connect the param ikfk attr to the ikfk system group ikfk attribute
        mc.connectAttr(ikfkAttr, "{0}.ikfk".format(self.ikfkSystem.getGroup()), f=True)


        # create ikfk reverse node to connect the ikfk attribute
        reverseNode = mc.createNode("reverse", name="{0}_rvr".format(self.name))
        mc.connectAttr(ikfkAttr, "{0}.inputX".format(reverseNode), f=True)


        # get handle and create poleVector
        fkJointList = self.ikfkSystem.getFkJointList()
        ikJointList = self.ikfkSystem.getIkJointList()
        #poleVectorPos = self.ikfkSystem.getPoleVectorPosition(fkJointList)
        poleVectorPos = self.ikfkSystem.getPoleVectorFromHandle(self.ikfkSystem.getHandle(), fkJointList)

        pvCtrlHierarchy = rigrepo.libs.control.create(name=ikControlNames[0], 
                                                controlType="diamond",
                                                hierarchy=['nul','ort'],
                                                position=poleVectorPos,
                                                color=rigrepo.libs.common.GREEN)

        # get the handle and pv control
        pvCtrl = pvCtrlHierarchy[-1]
        mc.parent(paramNode, pvCtrl, s=True, r=True)
        handle = self.ikfkSystem.getHandle()
        mc.poleVectorConstraint(pvCtrl, handle)

        # set the parent of the controls to be the rig group
        parent = self.name

        endJointPos = mc.xform(ikJointList[-1], q=True, ws=True, t=True)
        ikCtrlHierarchy = rigrepo.libs.control.create(name=ikControlNames[1], 
                                                controlType="cube",
                                                hierarchy=['nul','ort'],
                                                position=endJointPos,
                                                color=rigrepo.libs.common.GREEN)     

        ikCtrl = ikCtrlHierarchy[-1]
        mc.parent(paramNode, ikCtrl, add=True, s=True, r=True)
        

        # duplicate the end ik joint and make it offset joint for the 
        # ik control to drive the end joint
        dupEndJnt = mc.duplicate(ikJointList[-1],
                                po=True, 
                                rr=True, 
                                name="{}_offset".format(ikJointList[-1]))[0]

        mc.setAttr('{0}.tx'.format(dupEndJnt),mc.getAttr('{0}.tx'.format(dupEndJnt))+2)
        mc.delete(mc.aimConstraint(dupEndJnt, ikCtrl)[0])
        mc.setAttr('{0}.drawStyle'.format(dupEndJnt), 2)

        mc.setAttr("{0}.v".format(handle), 0)
        mc.parent(dupEndJnt,ikCtrl)
        mc.setAttr("{0}.t".format(dupEndJnt),0,0,0)
        mc.orientConstraint(dupEndJnt, ikJointList[-1])

        # parent the controls to the parent group
        mc.parent((pvCtrlHierarchy[0],ikCtrlHierarchy[0]), parent)

        self._ikControls.extend([str(pvCtrl), str(ikCtrl)])

        # create the ik stretchy system
        self._stretchTargetJointList = self.ikfkSystem.createStretchIK(handle, self.ikfkSystem.getGroup())


        #create attributes on param node and connect them to the grp node
        mc.addAttr(paramNode, ln='stretch', at='double', dv = 1, min = 0, max = 1, k=True)
        mc.addAttr(paramNode, ln='stretchTop', at='double', min=0, dv = 1, k=True)
        mc.addAttr(paramNode, ln='stretchBottom', at='double', min=0, dv = 1, k=True)
        mc.addAttr(paramNode, ln='softStretch', at='double', min=0, max=1, dv=0.2, k=True)

        rigrepo.libs.control.tagAsControl(paramNode)

        grp = self.ikfkSystem.getGroup()
        for attr in ['stretch','stretchTop', 'stretchBottom', 'softStretch']:
            mc.connectAttr('{}.{}'.format(paramNode, attr), 
                        '{}.{}'.format(grp, attr), f=True)

        #mc.parent(handle, dupEndJnt)
        mc.parent(self._stretchTargetJointList[-1], dupEndJnt)


        for ctrl in self._ikControls:
            if not mc.isConnected("{0}.outputX".format(reverseNode), "{0}.v".format(ctrl)):
                mc.connectAttr("{0}.outputX".format(reverseNode), "{0}.v".format(ctrl), f=True)

        #-------------------------------------------------------------------------------------------
        #FK Setup for the limb
        #-------------------------------------------------------------------------------------------
        fkControlsNulList = list()
        for fkJnt, fkCtrl in zip(fkJointList,fkControlNames):
            # create the fk control hierarchy
            fkCtrlHierarchy = rigrepo.libs.control.create(name=fkCtrl, 
                                                controlType="cube",
                                                hierarchy=['nul','ort'])

            ctrl = fkCtrlHierarchy[-1]
            nul = fkCtrlHierarchy[0]

            #append nul to the nul list in case we need to use it for other things.
            fkControlsNulList.append(nul)

            # make sure that the control is in the same position as the joint
            fkJntMatrix = mc.xform(fkJnt, q=True, ws=True, matrix=True)
            mc.xform(nul, ws=True, matrix=fkJntMatrix)

            # setup the constraints from the control to the joint
            mc.pointConstraint(ctrl, fkJnt)
            mc.orientConstraint(ctrl, fkJnt)

            # add the param node to the control and connect it
            mc.parent(paramNode, ctrl, add=True, s=True, r=True)

            #parent the control to the parent node
            mc.parent(nul,parent)
            parent = ctrl
            mc.connectAttr(ikfkAttr, "{0}.v".format(ctrl), f=True)
            self._fkControls.append(str(ctrl))

        # create the offset joint that will be used for ikfk switching. This is the offset of the
        # ik control from the fk control
        mc.select(clear=True)
        fkOffsetJnt = mc.joint(name="{}_offset".format(fkJointList[-1]))
        mc.xform(fkOffsetJnt, ws=True, matrix=mc.xform(ikCtrl, q=True, ws=True, matrix=True))
        # turn off the visibility of the offset joint
        mc.setAttr('{0}.drawStyle'.format(fkOffsetJnt), 2)

        # parent the offset joint to the fk wrist control.
        mc.parent(fkOffsetJnt, self._fkControls[-1])

        # delete the original tranform that came with the locator paramNode
        mc.delete(paramNodeTrs)

        #rename ikfk group and parent it under the part name group
        self.ikfkSystem.setGroup("{0}_{1}".format(self.name,self.ikfkSystem.getGroup()))
        mc.parent(self.ikfkSystem.getGroup(), self.name)

        # Connect to passed anchor
        #
        anchor = self.getAttributeByName('anchor').getValue()
        if mc.objExists(anchor):
            anchorGrp = mc.createNode('transform', n=self.name+'_anchor_grp', p=self.name) 
            self._anchorGrp = anchorGrp
            mc.xform(anchorGrp, ws=True, matrix=mc.xform(ikJointList[0], q=True, ws=True, matrix=True))
            mc.parentConstraint(anchor, anchorGrp, mo=1)
            mc.parent(self.ikfkSystem.getGroup(), fkControlsNulList[0], anchorGrp)
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 

        for jnt,blendJnt in zip(self.ikfkSystem.getJointList(), self.ikfkSystem.getBlendJointList()):
            mc.pointConstraint(blendJnt, jnt)
            mc.orientConstraint(blendJnt, jnt)

        #------------------------------------------------------------------------------------------
        #Setup attributes on the param node for the ikfk switch.
        #------------------------------------------------------------------------------------------
        # fk match attributes needed to the switch
        mc.addAttr(paramNode, ln="fkMatchTransforms", dt="string")
        mc.setAttr("{}.fkMatchTransforms".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(fkJointList[0], fkJointList[1], fkOffsetJnt), 
                type="string")

        mc.addAttr(paramNode, ln="fkControls", dt="string")
        mc.setAttr("{}.fkControls".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(*self._fkControls), 
                type="string")

        # ik match attributes needed for the switch
        mc.addAttr(paramNode, ln="ikMatchTransforms", dt="string")
        mc.setAttr("{}.ikMatchTransforms".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(*ikJointList), 
                type="string")
        mc.addAttr(paramNode, ln="ikControls", dt="string")
        mc.setAttr("{}.ikControls".format(paramNode), 
                '["{0}","{1}"]'.format(*self._ikControls), 
                type="string")

        # command to be called when switch is being used.
        mc.addAttr(paramNode, ln="switchCommand", dt="string")
        mc.setAttr("{}.switchCommand".format(paramNode), "rigrepo.parts.limb.Limb.switch", 
                    type="string")

    def postBuild(self):
        '''
        '''
        #turn of the visibility of the ikfk system
        mc.setAttr("{0}.v".format(self.ikfkSystem.getGroup()), 0)

        # NO TWIST JOINT
        side = self.getAttributeByName("side").getValue()
        nameSplit = self.jointList[0].split('_{}_'.format(side))
        noTwist = '{}NoTwist_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        target = self.jointList[1]
        aimVector = (1, 0, 0)
        if side is 'r':
            aimVector = (-1, 0, 0)
        if mc.objExists(noTwist):
            mc.aimConstraint(target, noTwist, mo=1, weight=1, aimVector=aimVector, upVector=(0, 0, 0), worldUpType='none')
        else:
            print('noTwist not found', noTwist)
        # TWIST JOINT
        joint = self.jointList[-1]
        nameSplit = joint.split('_{}_'.format(side))
        twistJoint = '{}Twist_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        if mc.objExists(twistJoint):
            deompose = rigrepo.libs.transform.decomposeRotation(joint)
            mc.connectAttr(joint + '.decomposeTwist', twistJoint + '.rx', f=1)
        else:
            print('No twist joint found', noTwist)

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
        if value == 0:
            fkControls = eval(mc.getAttr("{}.fkControls".format(paramNode)))
            ikMatchTransforms = eval(mc.getAttr("{}.ikMatchTransforms".format(paramNode)))
            rigrepo.libs.ikfk.IKFKLimb.fkMatchIk(fkControls, ikMatchTransforms)
            mc.setAttr("{}.ikfk".format(paramNode), 1)
        elif value == 1:
            ikControls = eval(mc.getAttr("{}.ikControls".format(paramNode)))
            fkMatchTransforms = eval(mc.getAttr("{}.fkMatchTransforms".format(paramNode)))
            rigrepo.libs.ikfk.IKFKLimb.ikMatchFk(fkMatchTransforms, ikControls[1], ikControls[0])
            mc.setAttr("{}.ikfk".format(paramNode), 0)
