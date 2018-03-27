'''
This is the arm class extending the limb class.

This is expecting one more joint then the limb to use as the clavicle joint.
'''

import maya.cmds as mc
import rigrepo.parts.limb as limb
import rigrepo.libs.ikfk as ikfk
import rigrepo.libs.control as control

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
        
        super(Arm, self).__init__(name, jointList, anchor, dataObj, side) 
        self.addAttribute("clavicleCtrl", "clavicle_{}".format(side), attrType=str)
        self.addAttribute("swingCtrl", "shoulderSwing_{}".format(side), attrType=str)

    def build(self):
        '''
        '''
        super(Arm, self).build()
        clavicleCtrl = self.getAttributeByName('clavicleCtrl').getValue()
        swingCtrl = self.getAttributeByName('swingCtrl').getValue()
        swingCtrlHierarchy = control.create(name=swingCtrl, 
                                                controlType="square",
                                                hierarchy=['nul','ort'])
        clavicleCtrlHierarchy = control.create(name=clavicleCtrl, 
                                                controlType="square",
                                                hierarchy=['nul','ort'])

        clavicleCtrl = clavicleCtrlHierarchy[-1]
        clavicleNul = clavicleCtrlHierarchy[0]
        swingCtrl = swingCtrlHierarchy[-1]
        swingNul = swingCtrlHierarchy[0]
        clavicleJointMatrix = mc.xform(self._clavicleJoint, q=True, ws=True, matrix=True)
        mc.xform(clavicleNul, ws=True, matrix=clavicleJointMatrix)
        # move the shoulderSwing control to the correct location.
        shoulderCtrlMatrix = mc.xform(self._fkControls[0], q=True, ws=True, matrix=True)
        mc.xform(swingNul, ws=True, matrix=shoulderCtrlMatrix)

        mc.pointConstraint(clavicleCtrl, self._clavicleJoint)
        mc.orientConstraint(clavicleCtrl, self._clavicleJoint)

        # parent the shoulderSwing control to the clavicle control.
        mc.parent(("{}_nul".format(self._fkControls[0]), self._stretchTargetJointList[0]), swingCtrl)
        mc.parent(swingNul, clavicleCtrl)

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





        
