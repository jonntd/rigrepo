'''
This is the hand class
'''

import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.control as control

class Hand(part.Part):
    '''
    '''
    def __init__(self, name, jointList, anchor="wrist_l_bind_blend", dataObj=None):
        '''
        This is the constructor.

        :param jointList: First joint for every finger. 
        :type jointList: list | tuple

        :param anchor: What we will anchor this part to.
        :type anchor: str
        '''
        super(Hand, self).__init__(name, dataObj)         
        self.jointList = jointList
        self._group = "{}_grp".format(self.name)
        self.addAttribute('anchor', anchor, attrType=str)

    def setGroup(self, value):
        '''
        This will set the name of the _group attribute on the class.
        If the value passed in doesn't exists and isn't equal to the _group
        attribute we will re-name the group.

        :param value:
        '''
        if mc.objExists(self._group) and value != self._group:
            mc.rename(self._group, value)

        self._group = value

    def build(self):
        '''
        This executes the build section of the part.
        '''
        super(Hand, self).build()
        anchor = self.getAttributeByName('anchor').getValue()

        if not mc.objExists(self._group):
            mc.createNode("transform", n=self._group)

        # check to see if the anchor exists in the scene
        if mc.objExists(anchor):
            mc.pointConstraint(anchor, self._group)
            mc.orientConstraint(anchor, self._group)
        else:
            mc.warning("{} doesn't exists in the current Maya session!".format(anchor))


        # loop through all of the parent joints in the fingers. 
        parent = self._group
        for jnt in self.jointList:
            children = mc.listRelatives(jnt, ad=True, type="joint")
            children.reverse()
            fingerCtrlHierarchy = control.create(name="{0}_ctrl".format(jnt), 
                                                controlType="square",
                                                hierarchy=['nul','ort'],
                                                parent=parent)
            jntPosition = mc.xform(jnt, q=True, ws=True, matrix=True)
            mc.xform(fingerCtrlHierarchy[0], ws=True, matrix=jntPosition)
            mc.pointConstraint(fingerCtrlHierarchy[-1], jnt)
            mc.orientConstraint(fingerCtrlHierarchy[-1], jnt)

            parent = fingerCtrlHierarchy[-1]

            for childJoint in children:
                childCtrlierarchy = control.create(name="{0}_ctrl".format(childJoint), 
                                                controlType="square",
                                                hierarchy=['nul','ort'],
                                                parent=parent)
                childJointPosition = mc.xform(childJoint, q=True, ws=True, matrix=True)
                mc.xform(childCtrlierarchy[0], ws=True, matrix=childJointPosition)
                mc.pointConstraint(childCtrlierarchy[-1], childJoint)
                mc.orientConstraint(childCtrlierarchy[-1], childJoint)
                parent = childJoint
                if childJoint == children[-1]:
                    parent = self._group

        # parent the group the the name of this part
        mc.parent(self._group, self.name)










        
