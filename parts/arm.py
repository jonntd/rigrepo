'''
This is the limb base class.

Anything that uses a three joint chain ik/fk setup
should start with this class.
'''

import maya.cmds as mc
import rigrepo.parts.limb as limb
import rigrepo.libs.ikfk as ikfk
import rigrepo.libs.control as control

class Arm(limb.Limb):
    '''
    '''
    def __init__(self, name, jointList):
        '''
        This is the constructor.
        '''
        if len(jointList) != 4:
            raise RuntimeError("""{0} must be an array of 4 elements
                that exists in Maya.""".format(jointList))

        self._clavicleJoint = jointList.pop(0)
        super(Arm, self).__init__(name, jointList) 


    def build(self):
        '''
        '''
        super(Arm, self).build()
        clavicleCtrlHierarchy = control.createControl(name="{0}_ctrl".format(self._clavicleJoint), 
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





        