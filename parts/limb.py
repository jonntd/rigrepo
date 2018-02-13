'''
This is the limb base class.

Anything that uses a three joint chain ik/fk setup
should start with this class.
'''

import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.ikfk as ikfk
import rigrepo.libs.control as control

class Limb(part.Part):
    '''
    '''
    def __init__(self, name, jointList, anchor='chest'):
        '''
        This is the constructor.
        '''
        super(Limb, self).__init__(name) 
        self.ikfkSystem = ikfk.IKFKLimb(jointList)
        self._fkControls = list()
        self._ikControls = list()
        self._anchorGrp = str()
        self.addAttribute("anchor", anchor, attrType='str')

    def build(self):
        '''
        '''
        super(Limb, self).build()

        self.ikfkSystem.create()

        # create the param node and ikfk attribute for it
        paramNode = mc.createNode("locator", name="{0}_param".format(self.name))
        paramNodeTrs = mc.listRelatives(paramNode, p=True)[0]
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
        poleVectorPos = self.ikfkSystem.getPoleVectorFromHandle()

        pvCtrlHierarchy = control.create(name="{0}_pv".format(self.name), 
                                                controlType="diamond",
                                                hierarchy=['nul','ort'],
                                                position=poleVectorPos)

        # get the handle and pv control
        pvCtrl = pvCtrlHierarchy[-1]
        mc.parent(paramNode, pvCtrl, s=True, r=True)
        handle = self.ikfkSystem.getHandle()
        mc.poleVectorConstraint(pvCtrl, handle)


        # set the parent of the controls to be the rig group
        parent = self.name

        endJointPos = mc.xform(ikJointList[-1], q=True, ws=True, t=True)
        ikCtrlHierarchy = control.create(name="{0}_ik".format(self.name), 
                                                controlType="cube",
                                                hierarchy=['nul','ort'],
                                                position=endJointPos)     

        ikCtrl = ikCtrlHierarchy[-1]
        mc.parent(paramNode, ikCtrl, add=True, s=True, r=True)

        dupEndJnt = mc.duplicate(ikJointList[-1],po=True, rr=True)[0]
        mc.setAttr('{0}.tx'.format(dupEndJnt),mc.getAttr('{0}.tx'.format(dupEndJnt))*2)
        mc.delete(mc.aimConstraint(dupEndJnt, ikCtrl)[0])

        
        mc.setAttr("{0}.v".format(handle), 0)
        mc.parent(dupEndJnt,ikCtrl)
        mc.setAttr("{0}.t".format(dupEndJnt),0,0,0)
        mc.parent(handle, dupEndJnt)
        mc.orientConstraint(dupEndJnt, ikJointList[-1])

        # parent the controls to the parent group
        mc.parent((pvCtrlHierarchy[0],ikCtrlHierarchy[0]), parent)

        self._ikControls.extend([pvCtrl, ikCtrl])

        for ctrl in self._ikControls:
            mc.connectAttr("{0}.outputX".format(reverseNode), "{0}.v".format(ctrl), f=True)

        #-------------------------------------------------------------------------------------------
        #FK Setup for the limb
        #-------------------------------------------------------------------------------------------
        fkCtrlNul = str()
        for fkJnt in fkJointList:
            # create the fk control hierarchy
            fkCtrlHierarchy = control.create(name="{0}_ctrl".format(fkJnt), 
                                                controlType="cube",
                                                hierarchy=['nul','ort'])

            ctrl = fkCtrlHierarchy[-1]
            nul = fkCtrlHierarchy[0]
            fkCtrlNul = nul

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
            self._fkControls.append(ctrl)
            

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
            con = mc.parentConstraint(ikJointList[0], anchorGrp)
            mc.delete(con)
            mc.parentConstraint(anchor, anchorGrp, mo=1)
            mc.parent(self.ikfkSystem.getGroup(), fkCtrlNul, anchorGrp)
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 

        for jnt,blendJnt in zip(self.ikfkSystem.getJointList(), self.ikfkSystem.getBlendJointList()):
            mc.pointConstraint(blendJnt, jnt)
            mc.orientConstraint(blendJnt, jnt)


    def postBuild(self):
        '''
        '''
        #turn of the visibility of the ikfk system
        mc.setAttr("{0}.v".format(self.ikfkSystem.getGroup()), 0)
