'''
This part will handle the look at rig for the eyes
'''
import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.control
import rigrepo.libs.common
import rigrepo.libs.transform
import rigrepo.libs.attribute

class LookAt(part.Part):
    '''
    LookAt class is to control how the eye rig is created.
    '''
    def __init__(self, name, anchor="face_upper"):
        '''
        This is the constructor

        :param name: Name of the part
        :type name: str

        :param anchor: What the system will be parented to.
        :type anchor: str
        '''
        super(LookAt, self).__init__(name)
        self.addAttribute("anchor", anchor, attrType=str)
        self.addAttribute("eyeJoints", '["eye_l_bind", "eye_r_bind"]', attrType=str)
        self.addAttribute("eyeAnchors", '["eyeSocket_l", "eyeSocket_r"]', attrType=str)
        self.addAttribute("eyeControlNames", '["eye_l", "eye_r"]', attrType=str)
        
    def build(self):
        '''
        This is where we build the eye rig.
        '''
        super(LookAt, self).build()

        eyeJointList = eval(self.getAttributeByName("eyeJoints").getValue())
        eyeAnchorList = eval(self.getAttributeByName("eyeAnchors").getValue())
        eyeControlNameList = eval(self.getAttributeByName("eyeControlNames").getValue())
        anchor = self.getAttributeByName("anchor").getValue()

        # create the main lookAt controls. 
        lookAtNul, lookAtOrt, lookAtCtrl = rigrepo.libs.control.create(name="lookAt_trs", 
                                                              controlType="square",
                                                              color=rigrepo.libs.common.GREEN,
                                                              hierarchy=['nul', 'ort'],
                                                              parent=self.name)

        lookAtRotNul, lookAtRotAim, lookAtRotCtrl = rigrepo.libs.control.create(name="lookAt_rot", 
                                                              controlType="diamond",
                                                              color=rigrepo.libs.common.GREEN,
                                                              hierarchy=['nul', 'aim'],
                                                              parent=self.name)


        rigrepo.libs.attribute.lockAndHide(lookAtRotCtrl, ['t', 'tx', 'ty', 'tz', 's', 'sx', 'sy', 'sz'])
        rigrepo.libs.attribute.lockAndHide(lookAtCtrl, ['r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz'])

        # put both lookAt and lookAt rot at the loaction between the eyes
        for nul in (lookAtNul, lookAtRotNul):
            eyePosition = rigrepo.libs.transform.getAveragePosition(eyeJointList)
            mc.xform(nul, ws=True, t=eyePosition)
        # move the lookAt out in positive Z space
        mc.xform(lookAtOrt, relative=True, t=(0, 0, 2))

        # aim constraint the lookAtRot control to the lookAt control
        mc.aimConstraint(lookAtCtrl, lookAtRotAim, offset=(0, 0 ,0), weight=1, aimVector=(0, 0, 1), 
                            upVector= (0, 1, 0), wut="none")

        # make the individual eye controls
        for i, joint in enumerate(eyeJointList):
            eyeNul, eyeOrt, eyeDefAuto, eyeCtrl = rigrepo.libs.control.create(name=eyeControlNameList[i], 
                                                                      controlType="circle",
                                                                      color=rigrepo.libs.common.BLUE,
                                                                      hierarchy=['nul', 'ort', 'def_auto'],
                                                                      parent=eyeAnchorList[i])

            rigrepo.libs.attribute.lockAndHide(eyeCtrl,['t', 'tx', 'ty', 'tz', 's', 'sx', 'sy', 'sz'])

            mc.xform(eyeNul, ws=True, matrix=mc.xform(joint, q=True, ws=True, matrix=True))
            #mc.pointConstraint(eyeCtrl, joint)
            mc.orientConstraint(eyeCtrl, joint)

            offsetJoint = mc.duplicate(joint, name="{}_offset".format(joint), rr=True, po=True)[0]
            mc.setAttr("{}.drawStyle".format(offsetJoint), 2)
            mc.parent(offsetJoint, lookAtRotCtrl)
            mc.orientConstraint(offsetJoint, eyeOrt)



        # parent the lookAt to the anchor
        mc.parent(self.name, anchor)   