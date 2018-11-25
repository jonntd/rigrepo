'''
This is the base module for all of your parts.
'''
import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.control

class Face(part.Part):
    '''
    Face class will handle specific parts of the face that don't have it's own part.
    Other parts will need controls built in this part so it can get put into the hierarchy of 
    the rig.
    '''
    def __init__(self, name, anchor="head"):
        '''
        This is the constructor for the class.
        '''
        super(Face, self).__init__(name)
        self.addAttribute("anchor", anchor, attrType=str)

        self.addAttribute("jawJoint", "jaw_bind", attrType=str)
        self.addAttribute("faceUpperJoint", "face_upper_bind", attrType=str)
        self.addAttribute("faceLowerJoint", "face_lower_bind", attrType=str)
        self.addAttribute("noseBridge", "nose_bridge_bind", attrType=str)
        self.addAttribute("nose", "nose_bind", attrType=str)

    def setup(self):
        '''
        '''
        super(Face, self).setup()
        
    def build(self):
        '''
        This is where the builds will happen.
        '''
        super(Face, self).build()

        # get all of the inputs to the node.
        jawJoint = self.getAttributeByName("jawJoint").getValue()
        faceUpperJoint = self.getAttributeByName("faceUpperJoint").getValue()
        faceLowerJoint = self.getAttributeByName("faceLowerJoint").getValue()
        noseBridgeJoint = self.getAttributeByName("noseBridge").getValue()
        noseJoint = self.getAttributeByName("nose").getValue()
        anchor = self.getAttributeByName("anchor").getValue()


        # JAW
        if mc.objExists(jawJoint):
            # create the jaw control 
            jawNul, jawDefAuto, jawCtrl = rigrepo.libs.control.create(name="jaw", 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul', 'def_auto'])

            # position the jaw control and connect the joint to the control
            mc.xform(jawNul, ws=True, matrix=mc.xform(jawJoint, q=True, ws=True, matrix=True))
            mc.pointConstraint(jawCtrl, jawJoint)
            mc.orientConstraint(jawCtrl, jawJoint)

        # FACE LOWER
        if mc.objExists(faceLowerJoint):
            # Create the faceLower and jaw control
            faceLowerNul, faceLowerCtrl = rigrepo.libs.control.create(name="face_lower", 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul'],
                                              parent=anchor)

            # position the faceLowerNul and connect the joint to the control
            mc.xform(faceLowerNul, ws=True, matrix=mc.xform(faceLowerJoint, q=True, ws=True, matrix=True))
            mc.pointConstraint(faceLowerCtrl, faceLowerJoint)
            mc.orientConstraint(faceLowerCtrl, faceLowerJoint)

            # parent the jaw to face lower control
            if mc.objExists(jawJoint):
                mc.parent(jawNul, faceLowerCtrl)
        elif mc.objExists(jawJoint) and mc.objExists(anchor):
            mc.parent(jawNul, anchor)

        if mc.objExists(faceUpperJoint):
            # Create the faceLower and jaw control
            faceUpperNul, faceUpperCtrl = rigrepo.libs.control.create(name="face_upper", 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul'],
                                              parent=anchor)

            # position the faceLowerNul and connect the joint to the control
            mc.xform(faceUpperNul, ws=True, matrix=mc.xform(faceUpperJoint, q=True, ws=True, matrix=True))
            mc.pointConstraint(faceUpperCtrl, faceUpperJoint)
            mc.orientConstraint(faceUpperCtrl, faceUpperJoint)

        if mc.objExists(noseBridgeJoint):
            # Create the faceLower and jaw control
            noseBridgeNul, noseBridgeDefAuto, noseBridgeRotDefAuto, noseBridgeCtrl = rigrepo.libs.control.create(name="nose_bridge", 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul', 'def_auto', 'rot_def_auto'])

            if mc.objExists(faceUpperJoint):
                mc.parent(noseBridgeNul, faceUpperCtrl)
            else:
                mc.parent(noseBridgeNul, anchor)
            # position the faceLowerNul and connect the joint to the control
            mc.xform(noseBridgeNul, ws=True, matrix=mc.xform(noseBridgeJoint, q=True, ws=True, matrix=True))
            mc.pointConstraint(noseBridgeCtrl, noseBridgeJoint)
            mc.orientConstraint(noseBridgeCtrl, noseBridgeJoint)

        if mc.objExists(noseJoint):
            # Create the faceLower and jaw control
            noseNul, noseDefAuto, noseCtrl = rigrepo.libs.control.create(name="nose", 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul', 'def_auto'])

            if mc.objExists(noseBridgeJoint):
                mc.parent(noseNul, noseBridgeCtrl)
            else:
                mc.parent(noseNul, anchor)
            # position the faceLowerNul and connect the joint to the control
            mc.xform(noseNul, ws=True, matrix=mc.xform(noseJoint, q=True, ws=True, matrix=True))
            mc.pointConstraint(noseCtrl, noseJoint)
            mc.orientConstraint(noseCtrl, noseJoint)




    def postBuild(self):
        '''
        '''
        super(Face, self).postBuild()