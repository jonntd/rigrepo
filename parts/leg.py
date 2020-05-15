'''
This is the leg class
'''

import maya.cmds as mc
import rigrepo.parts.arm as arm
import rigrepo.libs.joint


class Leg(arm.Arm):
    '''
    '''
    def __init__(self, name, jointList, anchor='hip_swivel', dataObj=None, side='l'):
        '''
        This is the constructor.
        '''

        super(Leg, self).__init__(name, jointList, anchor, dataObj, side) 

        self.getAttributeByName("clavicleCtrl").setValue("pelvis_{}".format(side))
        self.getAttributeByName("swingCtrl").setValue("thighSwing_{}".format(side))


    def build(self):
        '''
        '''
        super(Leg, self).build()

        ikAnkleControl = self._ikControls[-2]
        ikGimbleControl = self._ikControls[-1]
        fkAnkleControl = self._fkControls[-2]
        fkGimbalControl = self._fkControls[-1]

        offsetJoint = mc.listRelatives(ikGimbleControl, ad=True, type="joint")[-1]
        fkOffsetJoint = mc.listRelatives(fkGimbalControl, c=True, type="joint")[0]
        mc.setAttr("{}.r".format(ikAnkleControl), 0,0,0)
        fkAnkleMatrix=mc.xform(fkAnkleControl,q=True, ws=True, matrix=True)
        # Put fkankle matrix data into the orient of the offset joint
        mc.xform(offsetJoint, ws=True, matrix=fkAnkleMatrix)
        rigrepo.libs.joint.rotateToOrient(offsetJoint)
        ikAnkleMatrix=mc.xform(ikAnkleControl,q=True, ws=True, matrix=True)
        mc.xform(fkOffsetJoint, ws=True, matrix=ikAnkleMatrix)
        self._pvSpaceAimNode = self._fkControls[0]
