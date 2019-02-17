'''
This is the hand class
'''

import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.control as control

class Hand(part.Part):
    '''
    '''
    def __init__(self, name, jointList, anchor="wrist_l_bind", dataObj=None):
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

        # check to make sure the group for this part has been created.
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
            # get all of the children of the main finger joints we're using. We have to reverse the 
            # list to get the order we want.
            children = mc.listRelatives(jnt, ad=True, type="joint")
            children.reverse()

            # create the first finger control
            fingerCtrlHierarchy = control.create(name="{0}_ctrl".format(jnt), 
                                                controlType="square",
                                                hierarchy=['nul','ort'],
                                                parent=parent)

            # move the control and then constrain the joint to the control.
            jntPosition = mc.xform(jnt, q=True, ws=True, matrix=True)
            mc.xform(fingerCtrlHierarchy[0], ws=True, matrix=jntPosition)
            mc.pointConstraint(fingerCtrlHierarchy[-1], jnt)
            mc.orientConstraint(fingerCtrlHierarchy[-1], jnt)

            # reset the parent hierarchy to be the control.
            parent = fingerCtrlHierarchy[-1]

            # loop throught the children to create controls for them
            for childJoint in children:
                if childJoint == children[-1]:
                    parent = self._group
                    break
                # create the control for the child joints.
                childCtrlierarchy = control.create(name="{0}_ctrl".format(childJoint), 
                                                controlType="square",
                                                hierarchy=['nul','ort'],
                                                parent=parent)
                childJointPosition = mc.xform(childJoint, q=True, ws=True, matrix=True)

                # move the control and then create the constraints.
                mc.xform(childCtrlierarchy[0], ws=True, matrix=childJointPosition)
                mc.pointConstraint(childCtrlierarchy[-1], childJoint)
                mc.orientConstraint(childCtrlierarchy[-1], childJoint)

                # set the parent to be the control we just created.
                parent = childCtrlierarchy[-1]

        # parent the group the the name of this part
        mc.parent(self._group, self.name)










        
