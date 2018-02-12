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
    def __init__(self, name, jointList, anchor=None):
        '''
        This is the constructor.
        '''
        if len(jointList) != 4:
            raise RuntimeError("""{0} must be an array of 4 elements
                that exists in Maya.""".format(jointList))

        self._clavicleJoint = jointList.pop(0)
        super(Arm, self).__init__(name, jointList, anchor) 
        self.addAttribute("anchor", "chest", attrType='str')


    def build(self):
        '''
        '''
        super(Arm, self).build()
        clavicleCtrlHierarchy = control.create(name="{0}_ctrl".format(self._clavicleJoint), 
                                                controlType="square",
                                                hierarchy=['nul','ort'])

        clavicleCtrl = clavicleCtrlHierarchy[-1]
        clavicleNul = clavicleCtrlHierarchy[0]
        clavicleJointMatrix = mc.xform(self._clavicleJoint, q=True, ws=True, matrix=True)
        mc.xform(clavicleNul, ws=True, matrix=clavicleJointMatrix)

        mc.pointConstraint(clavicleCtrl, self._clavicleJoint)
        mc.orientConstraint(clavicleCtrl, self._clavicleJoint)

        mc.parent(self._fkControls[0], clavicleCtrl)

        mc.parentConstraint(self._clavicleJoint, self.ikfkSystem.getIkJointList()[0], mo=True)

        mc.parent(clavicleNul, self.name)
  
        if self._anchorGrp:
            mc.parent(clavicleNul, self._anchorGrp) 





        
