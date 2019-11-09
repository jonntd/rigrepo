'''
This is the arm class extending the limb class.

This is expecting one more joint then the limb to use as the clavicle joint.
'''

import maya.cmds as mc
import rigrepo.parts.limb as limb
import rigrepo.libs.ikfk as ikfk
import rigrepo.libs.control as control
import rigrepo.libs.attribute

class Arm(limb.Limb):
    '''
    '''
    def __init__(self, name, jointList, anchor='chest', dataObj=None, side='l'):
        '''
        This is the constructor.
        '''
        if len(jointList) != 4:
            raise RuntimeError("""{0} must be an array of 4 elements
                that exists in Maya.""".format(jointList))

        self._clavicleJoint = jointList.pop(0)
        self._side = side
        
        super(Arm, self).__init__(name, jointList, anchor, dataObj, side) 
        self.addAttribute("clavicleCtrl", "clavicle_{}".format(side), attrType=str)
        self.addAttribute("swingCtrl", "shoulderSwing_{}".format(side), attrType=str)
        self.addAttribute("MirrorSwing", False, attrType=bool)

    def build(self):
        '''
        '''
        super(Arm, self).build()
        # get the values from the user. Node attributes in the graph.
        clavicleCtrl = self.getAttributeByName('clavicleCtrl').getValue()
        swingCtrl = self.getAttributeByName('swingCtrl').getValue()
        MirrorSwing = self.getAttributeByName('MirrorSwing').getValue()
        paramNodeName = self.getAttributeByName("paramNode").getValue()

        swingNul, swingMirrorOrt, swingOrt, swingCtrl = control.create(name=swingCtrl, 
                                                controlType="square",
                                                hierarchy=['nul','mirror_ort','ort'])
        clavicleNul, clavicleOrt, clavicleCtrl = control.create(name=clavicleCtrl, 
                                                                controlType="square",
                                                                hierarchy=['nul','ort'])

        # position the clavicle in the correct location
        clavicleJointMatrix = mc.xform(self._clavicleJoint, q=True, ws=True, matrix=True)
        mc.xform(clavicleNul, ws=True, matrix=clavicleJointMatrix)
        
        # get the aim direction
        aimDistance = mc.getAttr("{}.t".format(self.jointList[1]))[0]
        aimAttr, aimVector = self._getDistanceVector(aimDistance)
        sidePos = mc.xform(self.jointList[1], q=True, ws=True, t=True)

        # set the Ort node to be mirrored from the other side
        if sidePos[0] < 0:            
            mc.setAttr("{}.r{}".format(clavicleOrt, aimAttr.strip("-")), 180)
            mc.setAttr("{}.s{}".format(clavicleOrt, aimAttr.strip("-")), -1)

            # mirror the swing also if it is required by the build
            if MirrorSwing:
                mc.setAttr("{}.r{}".format(swingMirrorOrt, aimAttr.strip("-")), 180)
                mc.setAttr("{}.s{}".format(swingMirrorOrt, aimAttr.strip("-")), -1)

        # move the shoulderSwing control to the correct location.
        shoulderCtrlMatrix = mc.xform(self._fkControls[0], q=True, ws=True, matrix=True)
        mc.xform(swingNul, ws=True, matrix=shoulderCtrlMatrix)

        # Hookup clavicle connect nul, the direct connection for the rotate allow keeps the auto
        # clav from causint a double rotation on the shoulder
        clavicleConnect = mc.duplicate(clavicleCtrl, po=1, n=clavicleCtrl+'_connect')[0]
        mc.parent(clavicleConnect, clavicleNul)
        mc.connectAttr(clavicleCtrl+'.r', clavicleConnect+'.r')
        mc.connectAttr(clavicleCtrl+'.s', clavicleConnect+'.s')

        # This allows the translates to come through with auto clav
        clavicleConnectTranslate = mc.duplicate(swingNul, po=1, n=clavicleCtrl+'_connect_trans')[0]
        mc.parent(clavicleConnectTranslate, clavicleCtrl)
        mc.pointConstraint(clavicleConnectTranslate, clavicleConnect)

        # getting rid of the point constraint for now. Not sure we need it.
        #mc.pointConstraint(clavicleCtrl, self._clavicleJoint)
        mc.orientConstraint(clavicleCtrl, self._clavicleJoint)

        # parent the shoulderSwing control to the clavicle control.
        mc.parent((self._fkControls[0], self._stretchTargetJointList[0]), swingCtrl)
        ikJointList = self.ikfkSystem.getIkJointList()
        mc.parentConstraint(swingCtrl, ikJointList[0], mo=True)
        mc.parent(swingNul, clavicleConnect)
        
        # Connect to passed anchor
        #
        anchor = self.getAttributeByName('anchor').getValue()
        if mc.objExists(anchor):
            mc.parent(clavicleNul, anchor) 
        else:
            # parent the clavicle to the group of this part.
            mc.parent(clavicleNul, self.name)
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 


        # set the rotate order for the shoulder control
        #mc.setAttr("{}.rotateOrder".format(self._fkControls[0]), 0)
        # set the rotate order for the swing control
        #mc.setAttr("{}.rotateOrder".format(swingCtrl), 0)
        #self._fkControls.extend([clavicleCtrl,swingCtrl])

        # PSD driver - transform that picks up the auto clav and anim control rotation
        clavicleDriverPar = mc.duplicate(clavicleConnect, po=1, n=clavicleCtrl+'_driver_par')[0]
        clavicleDriver = mc.duplicate(clavicleConnect, po=1, n=clavicleCtrl+'_driver')[0]
        rigrepo.libs.control.untagAsControl(clavicleDriverPar)
        rigrepo.libs.control.untagAsControl(clavicleDriver)

        # make the node we can aim the wrist pv driver at for pv space switching to follow hand.
        clavicleDuplicate = mc.duplicate(clavicleNul, po=True, rr=True, name=clavicleNul.replace("_nul","_pvSpaceAim"))[0]
        self._pvSpaceAimNode = clavicleDuplicate

        # add the swing control to the string attribute for switching fk controls
        '''
        if mc.objExists("{}.fkControls".format(paramNodeName)):
            mc.setAttr("{}.fkControls".format(paramNodeName), 
                '["{}",{}","{}","{}"]'.format(swingCtrl,*self._fkControls), type="string")
        '''
        

    def postBuild(self):
        '''
        '''
        clavicleCtrl = self.getAttributeByName('clavicleCtrl').getValue()
        swingCtrl = self.getAttributeByName('swingCtrl').getValue()
        side = self.getAttributeByName("side").getValue()
        anchor = self.getAttributeByName("anchor").getValue()

        super(Arm, self).postBuild()
        rigrepo.libs.attribute.lockAndHide(swingCtrl,["sx","sy", "sz", "v"])
        rigrepo.libs.attribute.lockAndHide(clavicleCtrl,["sx","sy", "sz", "v"])
        nameSplit = self._clavicleJoint.split('_{}_'.format(side))
        transBind = '{}_trans_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        distanceUpperJnt = "{}_upper_dist_jnt".format(self.name)
        aimVector = (-1, 0, 0)
        if side is 'r':
            aimVector = (1, 0, 0)
        if mc.objExists(transBind):
            mc.aimConstraint(self._clavicleJoint, transBind, mo=0, weight=1, aimVector=aimVector, upVector=(0, 0, 0), worldUpType='none')
            mc.pointConstraint(self.jointList[0], transBind, mo=0)
            if mc.objExists(distanceUpperJnt):
                mc.pointConstraint(distanceUpperJnt, transBind, mo=0)
        else:
            print('clavicle translate not found', transBind)

        # Connect psd driver
        mc.parent(clavicleCtrl+'_driver', clavicleCtrl+'_driver_par')
        mc.parent(clavicleCtrl+'_driver_par', anchor)
        mc.delete(mc.orientConstraint('clavicle_trans_'+self._side+'_bind', clavicleCtrl+'_driver_par'))
        mc.orientConstraint('clavicle_trans_'+self._side+'_bind', clavicleCtrl+'_driver')
        

class ArmOld(limb.Limb):
    '''
    '''
    def __init__(self, name, jointList, anchor='chest', dataObj=None, side='l'):
        '''
        This is the constructor.
        '''
        if len(jointList) != 4:
            raise RuntimeError("""{0} must be an array of 4 elements
                that exists in Maya.""".format(jointList))

        self._clavicleJoint = jointList.pop(0)
        
        super(ArmOld, self).__init__(name, jointList, anchor, dataObj, side) 
        self.addAttribute("clavicleCtrl", "clavicle_{}".format(side), attrType=str)
        self.addAttribute("swingCtrl", "shoulderSwing_{}".format(side), attrType=str)

    def build(self):
        '''
        '''
        super(ArmOld, self).build()
        clavicleCtrl = self.getAttributeByName('clavicleCtrl').getValue()
        swingCtrl = self.getAttributeByName('swingCtrl').getValue()
        swingCtrlHierarchy = control.create(name=swingCtrl, 
                                                controlType="square",
                                                hierarchy=['nul','ort'])
        clavicleCtrlHierarchy = control.create(name=clavicleCtrl, 
                                                controlType="square",
                                                hierarchy=['nul','ort'])

        

        '''
        clavicle = 'clavicle_l'
        child = 'shoulderSwing_l_nul'

        aimTarget = mc.duplicate(clavicle, po=1, n=clavicle + '_aim_target')[0]
        aim = mc.duplicate(clavicle, po=1, n=clavicle + '_aim')[0]

        mc.delete(mc.pointConstraint(child, aimTarget))
        mc.parent(aimTarget, clavicle)
        mc.setAttr(aimTarget + '.tx', 1)

        mc.aimConstraint(aimTarget, aim, offset=[0, 0, 0],
                         weight=1, aimVector=[1, 0, 0],
                         worldUpType="none",
                         upVector=[0, 0, 0])

        mc.pointConstraint(aimTarget, child)
        '''

        clavicleCtrl = clavicleCtrlHierarchy[-1]
        clavicleNul = clavicleCtrlHierarchy[0]
        swingCtrl = swingCtrlHierarchy[-1]
        swingNul = swingCtrlHierarchy[0]
        clavicleJointMatrix = mc.xform(self._clavicleJoint, q=True, ws=True, matrix=True)
        mc.xform(clavicleNul, ws=True, matrix=clavicleJointMatrix)

        # move the shoulderSwing control to the correct location.
        shoulderCtrlMatrix = mc.xform(self._fkControls[0], q=True, ws=True, matrix=True)
        mc.xform(swingNul, ws=True, matrix=shoulderCtrlMatrix)

        # Hookup clavicle connect nul, the direct connection for the rotate allow keeps the auto
        # clav from causint a double rotation on the shoulder
        clavicleConnect = mc.duplicate(clavicleCtrl, po=1, n=clavicleCtrl+'_connect')[0]
        rigrepo.libs.control.untagAsControl(clavicleConnect)
        mc.parent(clavicleConnect, clavicleNul)
        mc.connectAttr(clavicleCtrl+'.r', clavicleConnect+'.r')
        mc.connectAttr(clavicleCtrl+'.s', clavicleConnect+'.s')
        # PSD driver - transform that picks up the auto clav and anim control rotation
        clavicleDriver = mc.duplicate(clavicleConnect, po=1, n=clavicleCtrl+'_driver')[0]
        mc.orientConstraint(clavicleCtrl, clavicleDriver)

        # This allows the translates to come through with auto clav
        clavicleConnectTranslate = mc.duplicate(swingNul, po=1, n=clavicleCtrl+'_connect_trans')[0]
        mc.parent(clavicleConnectTranslate, clavicleCtrl)
        mc.pointConstraint(clavicleConnectTranslate, clavicleConnect)


        mc.pointConstraint(clavicleCtrl, self._clavicleJoint)
        mc.orientConstraint(clavicleCtrl, self._clavicleJoint)

        # parent the shoulderSwing control to the clavicle control.
        mc.parent(("{}_nul".format(self._fkControls[0]), self._stretchTargetJointList[0]), swingCtrl)
        mc.parent(swingNul, clavicleConnect)

        # parent constrain the shoulder ik joint to the clavicle joint.
        mc.parentConstraint(self._clavicleJoint, self.ikfkSystem.getIkJointList()[0], mo=True)

        # parent the clavicle to the group of this part.
        mc.parent(clavicleNul, self.name)
        
        # Connect to passed anchor
        #
        anchor = self.getAttributeByName('anchor').getValue()
        if mc.objExists(anchor):
            mc.parent(clavicleNul, anchor) 
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 


        # set the rotate order for the shoulder control
        mc.setAttr("{}.rotateOrder".format(self._fkControls[0]), 2)
        # set the rotate order for the swing control
        mc.setAttr("{}.rotateOrder".format(swingCtrl), 2)