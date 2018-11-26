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
        self.addAttribute("faceMidJoint", "face_mid_bind", attrType=str)
        self.addAttribute("noseBridge", "nose_bridge_bind", attrType=str)
        self.addAttribute("upperTeeth", "teeth_upper_bind", attrType=str)
        self.addAttribute("lowerTeeth", "teeth_upper_bind", attrType=str)
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
        faceMidJoint = self.getAttributeByName("faceMidJoint").getValue()
        noseBridgeJoint = self.getAttributeByName("noseBridge").getValue()
        noseJoint = self.getAttributeByName("nose").getValue()
        anchor = self.getAttributeByName("anchor").getValue()
        upperTeeth = self.getAttributeByName("upperTeeth").getValue()
        lowerTeeth = self.getAttributeByName("lowerTeeth").getValue()


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

            # setup the jaw compression
            jawCompressionJnt = "jaw_compression_driver"
            if not mc.objExists(jawCompressionJnt):
                jawCompressionJnt = mc.joint(name="jaw_compression_driver")
                mc.xform(jawCompressionJnt, ws=True, q=True, rotation=mc.xform(faceLowerJoint, q=True, ws=True, rotation=True))
                mc.xform(jawCompressionJnt, ws=True, t=rigrpeo.libs.transform.getAveragePosition([upperTeeth, lowerTeeth]))

            # create the faceDiff joint and parent it to the faceUpperCtrl
            faceDiff = mc.duplicate("jaw_compression_driver", po=True, name="face_upper_diff")[0]
            mc.parent(faceDiff, faceUpperCtrl)
            parent = self.rigGroup
            groupList = ["jaw_compression_grp", "jaw_compression_nul", "jaw_compression_cnt", "jaw_compressiong_offset"]
            for group in groupList:
                mc.createNode("transform", name=group)
                mc.parent(group, parent)
                parent = group

            # position the jaw groups 
            mc.parentConstraint("skull_bind", groupList[0], mo=False)
            mc.xform(groupList[1], ws=True, matrix=mc.xform(jawJoint, q=True, ws=True, matrix=True))
            for attr in ['t', 'r', 's']:
                mc.connectAttr("{}.{}".format(jawCtrl,attr), "{}.{}".format(groupList[2],attr), f=True)

            mc.xform(groupList[-1], ws=True, matrix=mc.xform(jawCompressionJnt, q=True, ws=True, matrix=True))
            # parent the jawCompression joint to the last of the group nodes
            mc.parent(jawCompressionJnt, groupList[-1])
            # point constrain the jawCompression joint to the faceDiff joint
            mc.pointConstraint(faceDiff, jawCompressionJnt, mo=False)

            # turn off the visibility of the joints
            for jnt in [faceDiff, jawCompressionJnt]:
                mc.setAttr("{}.v".format(jnt), 0)

        if mc.objExists(noseBridgeJoint):
            # Create the faceLower and jaw control
            noseBridgeNul, noseBridgeDefAuto, noseBridgeRotDefAuto, noseBridgeCtrl = rigrepo.libs.control.create(name="nose_bridge", 
                                              controlType="null",
                                              color=rigrepo.libs.common.YELLOW,
                                              hierarchy=['nul', 'def_auto', 'rot_def_auto'])

            if mc.objExists(faceUpperJoint):
                mc.parent(noseBridgeNul, faceUpperCtrl)
                # create the setDriven keys for the jaw control
                mc.setDrivenKeyframe("{}.rx".format(noseBridgeRotDefAuto), 
                                cd="{}.ty".format(jawCompressionJnt), v=15, dv=-0.7)
                mc.setDrivenKeyframe("{}.rx".format(noseBridgeRotDefAuto), 
                                cd="{}.ty".format(jawCompressionJnt), v=-0, dv=0)
                for attr in ['y', 'z']:
                    mc.setDrivenKeyframe("{}.t{}".format(noseBridgeDefAuto,attr), 
                                    cd="{}.ty".format(jawCompressionJnt), v=.01, dv=-0.7)
                    mc.setDrivenKeyframe("{}.t{}".format(noseBridgeDefAuto,attr), 
                                    cd="{}.ty".format(jawCompressionJnt), v=0, dv=0)
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

        if mc.objExists(faceMidJoint):
            parent = faceLowerCtrl
            groupList = ["face_mid_nul", "face_upper_driver", "face_mid_offset", "face_mid_ort", "face_mid_def_auto"]
            for group in groupList:
                mc.createNode("transform", name=group)
                mc.parent(group, parent)
                parent = group

            # make the driver joint and parent it to the def auto and turn off visibility
            midDriver = mc.joint(name="face_mid_driver")
            mc.setAttr("{}.v".format(midDriver), 0 )

            mc.xform(groupList[0], ws=True, matrix=mc.xform(faceUpperCtrl, q=True, ws=True, matrix=True))
            for attr in ['t', 'r', 's']:
                mc.connectAttr("{}.{}".format(faceUpperCtrl,attr), "{}.{}".format(groupList[1],attr), f=True)
            mc.xform(groupList[2], ws=True, matrix=mc.xform(faceMidJoint, q=True, ws=True, matrix=True))
            # create the set drivens
            if mc.objExists(faceUpperJoint):
                # create the setDriven keys for the jaw control
                mc.setDrivenKeyframe("{}.rx".format(groupList[-1]), 
                                cd="{}.ty".format(jawCompressionJnt), v=10, dv=-0.7)
                mc.setDrivenKeyframe("{}.rx".format(groupList[-1]), 
                                cd="{}.ty".format(jawCompressionJnt), v=-0, dv=0)
                for attr in ['y', 'z']:
                    mc.setDrivenKeyframe("{}.t{}".format(groupList[-1],attr), 
                                    cd="{}.ty".format(jawCompressionJnt), v=-1, dv=-0.7)
                    mc.setDrivenKeyframe("{}.t{}".format(groupList[-1],attr), 
                                    cd="{}.ty".format(jawCompressionJnt), v=0, dv=0)

            # constrain the joint to the driver
            mc.pointConstraint(midDriver, faceMidJoint, mo=False)
            mc.orientConstraint(midDriver, faceMidJoint, mo=False)
            # parent the noseBridge to the proper group
            mc.parent(noseBridgeNul, groupList[-1])
            




    def postBuild(self):
        '''
        '''
        super(Face, self).postBuild()