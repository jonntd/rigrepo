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
        
        ikControl = self._ikControls[-1]

        offsetJoint = mc.listRelatives(ikControl, c=True, type="joint")[0]
        mc.parent(offsetJoint, w=True)
        mc.setAttr("{}.r".format(ikControl), 0,0,0)
        mc.parent(offsetJoint, ikControl)





