'''
This is the leg class
'''

import maya.cmds as mc
import rigrepo.parts.arm as arm

class Leg(arm.Arm):
    '''
    '''
    def __init__(self, name, jointList, anchor='hip_swivel', dataObj=None):
        '''
        This is the constructor.
        '''

        super(Leg, self).__init__(name, jointList, anchor, dataObj) 


    def build(self):
        '''
        '''
        super(Leg, self).build()
        
        ikAnkleControl = self._ikControls[-1]
        fkAnkleControl = self._fkControls[-1]

        offsetJoint = mc.listRelatives(ikAnkleControl, c=True, type="joint")[0]
        fkOffsetJoint = mc.listRelatives(fkAnkleControl, c=True, type="joint")[0]
        mc.parent(offsetJoint, w=True)
        mc.setAttr("{}.r".format(ikAnkleControl), 0,0,0)
        mc.parent(offsetJoint, ikAnkleControl)
        ikAnkleMatrix=mc.xform(self._ikControls[-1],q=True, ws=True, matrix=True)
        mc.xform(fkOffsetJoint, ws=True, matrix=ikAnkleMatrix)