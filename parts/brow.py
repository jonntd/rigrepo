'''
This is the brow module. 

This contains class that handles the construction of the brow rig based on 
parameters passed in by the user.
'''
import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.control as control
import rigrepo.libs.common as common

class Brow(part.Part):
    '''
    This class will handle the construction rig for the brows.
    '''
    def __init__(self, name, side="l", anchor="head_tip"):
        '''
        This is the constructor for the class.

        :param name: Name of the node
        :type name: str

        :param side: The side which you will be using for the name of the rig
        :type side: str

        :param anchor: This will be what drives the rig
        :type anchor: str
        '''
        super(Brow, self).__init__(name)
        self.addAttribute("anchor", anchor, attrType=str)
        self.addAttribute("side", side, attrType=str)
        self.addAttribute("browInner", "brow_inner_{side}", attrType=str)
        self.addAttribute("browMain", "brow_main_{side}", attrType=str)
        self.addAttribute("browPeak", "brow_peak_{side}", attrType=str)
        self.addAttribute("browInnerJoint", "{browInner}_bind", attrType=str)
        self.addAttribute("browMainJoint", "{browMain}_bind", attrType=str)
        self.addAttribute("browPeakJoint", "{browPeak}_bind", attrType=str)
        self.addAttribute("driverParent", "face_upper", attrType=str)
        
    def build(self):
        '''
        This is where the builds will happen.
        '''
        super(Brow, self).build()

        # get all of the inputs to the node.
        side = self.getAttributeByName("side").getValue()
        anchor = self.getAttributeByName("anchor").getValue()
        browInner = self.getAttributeByName("browInner").getValue().format(side=side)
        browMain = self.getAttributeByName("browMain").getValue().format(side=side)
        browPeak = self.getAttributeByName("browPeak").getValue().format(side=side)
        browInnerJoint = self.getAttributeByName("browInnerJoint").getValue().format(browInner=browInner)
        browMainJoint = self.getAttributeByName("browMainJoint").getValue().format(browMain=browMain)
        browPeakJoint = self.getAttributeByName("browPeakJoint").getValue().format(browPeak=browPeak)
        driverParent = self.getAttributeByName("driverParent").getValue()
        mc.parent(self.name, driverParent)
        # going to create the control hierarchies.
        browMainNul, browMainOrient, browMainCtrl = control.create(name=browMain, 
                                                                    controlType="null", 
                                                                    hierarchy=['nul','ort'], 
                                                                    color=common.BLUE,
                                                                    parent=anchor)

        browInnerNul, browInnerOrient, browInnerCtrl = control.create(name=browInner, 
                                                                    controlType="null", 
                                                                    hierarchy=['nul','ort'], 
                                                                    color=common.BLUE,
                                                                    parent=browMainCtrl)

        browPeakNul, browPeakOrient, browPeakCtrl = control.create(name=browPeak, 
                                                                    controlType="null", 
                                                                    hierarchy=['nul','ort'], 
                                                                    color=common.BLUE,
                                                                    parent=browMainCtrl)


        # position the controls
        mc.xform(browMainNul, ws=True, matrix=mc.xform(browMainJoint, q=True, ws=True, matrix=True))
        mc.xform(browInnerNul, ws=True, matrix=mc.xform(browInnerJoint, q=True, ws=True, matrix=True))
        mc.xform(browPeakNul, ws=True, matrix=mc.xform(browPeakJoint, q=True, ws=True, matrix=True))

        # create the driver nodes
        browMainDriverNul = mc.createNode("transform", name="{}_driver_nul".format(browMain), parent=self.name)
        browMainDriverOrt = mc.createNode("transform", name="{}_driver_ort".format(browMain), parent=browMainDriverNul)
        browMainDriver = mc.createNode("joint", name="{}_driver".format(browMain), parent=browMainDriverOrt)

        # position the driver
        mc.xform(browMainDriverNul, ws=True, matrix=mc.xform(browMainNul, q=True, ws=True, matrix=True))
        for attr in ['t', 'r', 's']:
            mc.connectAttr("{}.{}".format(browMainOrient, attr), "{}.{}".format(browMainDriverOrt, attr), f=True)
            mc.connectAttr("{}.{}".format(browMainOrient, attr), "{}.{}".format(browMainDriverOrt, attr), f=True)
            mc.connectAttr("{}.{}".format(browMainOrient, attr), "{}.{}".format(browMainDriverOrt, attr), f=True)

        mc.pointConstraint(browMainCtrl, browMainDriver)

        browInnerDriverNul = mc.createNode("transform", name="{}_driver_nul".format(browInner), parent=self.name)
        browInnerDriverOrt = mc.createNode("transform", name="{}_driver_ort".format(browInner), parent=browInnerDriverNul)
        browInnerDriver = mc.createNode("joint", name="{}_driver".format(browInner), parent=browInnerDriverOrt)

        # position the driver
        mc.xform(browInnerDriverNul, ws=True, matrix=mc.xform(browInnerNul, q=True, ws=True, matrix=True))

        for attr in ['t', 'r', 's']:
            mc.connectAttr("{}.{}".format(browInnerOrient, attr), "{}.{}".format(browInnerDriverOrt, attr), f=True)
            mc.connectAttr("{}.{}".format(browInnerOrient, attr), "{}.{}".format(browInnerDriverOrt, attr), f=True)
            mc.connectAttr("{}.{}".format(browInnerOrient, attr), "{}.{}".format(browInnerDriverOrt, attr), f=True)

        mc.pointConstraint(browInnerCtrl, browInnerDriver)

        browPeakDriverNul = mc.createNode("transform", name="{}_driver_nul".format(browPeak), parent=self.name)
        browPeakDriverOrt = mc.createNode("transform", name="{}_driver_ort".format(browPeak), parent=browPeakDriverNul)
        browPeakDriver = mc.createNode("joint", name="{}_driver".format(browPeak), parent=browPeakDriverOrt)

        # position the driver
        mc.xform(browPeakDriverNul, ws=True, matrix=mc.xform(browPeakNul, q=True, ws=True, matrix=True))

        for attr in ['t', 'r', 's']:
            mc.connectAttr("{}.{}".format(browPeakOrient, attr), "{}.{}".format(browPeakDriverOrt, attr), f=True)
            mc.connectAttr("{}.{}".format(browPeakOrient, attr), "{}.{}".format(browPeakDriverOrt, attr), f=True)
            mc.connectAttr("{}.{}".format(browPeakOrient, attr), "{}.{}".format(browPeakDriverOrt, attr), f=True)

        mc.pointConstraint(browPeakCtrl, browPeakDriver)

        # create the set driven key nodes.
        browMainSdkNul = mc.createNode("transform", name="{}_sdk_nul".format(browMain), parent=self.name)
        browMainSdkDefAuto = mc.createNode("transform", name="{}_sdk_def_auto".format(browMain), parent=browMainSdkNul)
        browMainSdkRotDefAuto = mc.createNode("transform", name="{}_sdk_rot_def_auto".format(browMain), parent=browMainSdkDefAuto)
        browMainSdk = mc.createNode("transform", name="{}_sdk".format(browMain), parent=browMainSdkRotDefAuto)

        # position the SDK nodes
        mc.xform(browMainSdkNul, ws=True, matrix=mc.xform(browMainDriverOrt, q=True, ws=True, matrix=True))
        mc.connectAttr("{}.s".format(browMainDriverOrt), "{}.s".format(browMainSdkNul), f=True)
        
        # create the keys for the brow main sdk nodes
        for attribute in ['x','y','z']:
            mc.setDrivenKeyframe("{}.t{}".format(browMainSdkDefAuto,attribute), 
                                cd="{}.t{}".format(browMainDriver,attribute), v=0, dv=0)
            mc.setDrivenKeyframe("{}.t{}".format(browMainSdkDefAuto,attribute), 
                                cd="{}.t{}".format(browMainDriver,attribute), v=1, dv=1)
            mc.setDrivenKeyframe("{}.t{}".format(browMainSdkDefAuto,attribute), 
                                cd="{}.t{}".format(browMainDriver,attribute), v=-1, dv=-1)
            mc.setDrivenKeyframe("{}.r{}".format(browMainSdkRotDefAuto,attribute), 
                                cd="{}.t{}".format(browMainDriver,attribute), v=0, dv=0)
            mc.setDrivenKeyframe("{}.r{}".format(browMainSdkRotDefAuto,attribute), 
                                cd="{}.t{}".format(browMainDriver,attribute), v=.1, dv=1)
            mc.setDrivenKeyframe("{}.r{}".format(browMainSdkRotDefAuto,attribute), 
                                cd="{}.t{}".format(browMainDriver,attribute), v=-.1, dv=-1)

        # create the set driven key nodes.
        browInnerSdkNul = mc.createNode("transform", name="{}_sdk_nul".format(browInner), parent=self.name)
        browInnerSdkDefAuto = mc.createNode("transform", name="{}_sdk_def_auto".format(browInner), parent=browInnerSdkNul)
        browInnerSdkRotDefAuto = mc.createNode("transform", name="{}_sdk_rot_def_auto".format(browInner), parent=browInnerSdkDefAuto)
        browInnerSdk = mc.createNode("transform", name="{}_sdk".format(browInner), parent=browInnerSdkRotDefAuto)

        # position the SDK nodes
        mc.xform(browInnerSdkNul, ws=True, matrix=mc.xform(browInnerDriverOrt, q=True, ws=True, matrix=True))
        mc.connectAttr("{}.s".format(browInnerDriverOrt), "{}.s".format(browInnerSdkNul), f=True)
        
        # create the keys for the brow inner sdk nodes
        for attribute in ['x','y','z']:
            mc.setDrivenKeyframe("{}.t{}".format(browInnerSdkDefAuto,attribute), 
                                cd="{}.t{}".format(browInnerDriver,attribute), v=0, dv=0)
            mc.setDrivenKeyframe("{}.t{}".format(browInnerSdkDefAuto,attribute), 
                                cd="{}.t{}".format(browInnerDriver,attribute), v=1, dv=1)
            mc.setDrivenKeyframe("{}.t{}".format(browInnerSdkDefAuto,attribute), 
                                cd="{}.t{}".format(browInnerDriver,attribute), v=-1, dv=-1)
            mc.setDrivenKeyframe("{}.r{}".format(browInnerSdkRotDefAuto,attribute), 
                                cd="{}.t{}".format(browInnerDriver,attribute), v=0, dv=0)
            mc.setDrivenKeyframe("{}.r{}".format(browInnerSdkRotDefAuto,attribute), 
                                cd="{}.t{}".format(browInnerDriver,attribute), v=.1, dv=1)
            mc.setDrivenKeyframe("{}.r{}".format(browInnerSdkRotDefAuto,attribute), 
                                cd="{}.t{}".format(browInnerDriver,attribute), v=-.1, dv=-1)


        # create the set driven key nodes.
        browPeakSdkNul = mc.createNode("transform", name="{}_sdk_nul".format(browPeak), parent=self.name)
        browPeakSdkDefAuto = mc.createNode("transform", name="{}_sdk_def_auto".format(browPeak), parent=browPeakSdkNul)
        browPeakSdkRotDefAuto = mc.createNode("transform", name="{}_sdk_rot_def_auto".format(browPeak), parent=browPeakSdkDefAuto)
        browPeakSdk = mc.createNode("transform", name="{}_sdk".format(browPeak), parent=browPeakSdkDefAuto)

        # position the SDK nodes
        mc.xform(browPeakSdkNul, ws=True, matrix=mc.xform(browPeakDriverOrt, q=True, ws=True, matrix=True))
        mc.connectAttr("{}.s".format(browPeakDriverOrt), "{}.s".format(browPeakSdkNul), f=True)
        
        # create the keys for the brow peak sdk nodes
        for attribute in ['x','y','z']:
            mc.setDrivenKeyframe("{}.t{}".format(browPeakSdkDefAuto,attribute), 
                                cd="{}.t{}".format(browPeakDriver,attribute), v=0, dv=0)
            mc.setDrivenKeyframe("{}.t{}".format(browPeakSdkDefAuto,attribute), 
                                cd="{}.t{}".format(browPeakDriver,attribute), v=1, dv=1)
            mc.setDrivenKeyframe("{}.t{}".format(browPeakSdkDefAuto,attribute), 
                                cd="{}.t{}".format(browPeakDriver,attribute), v=-1, dv=-1)
            mc.setDrivenKeyframe("{}.r{}".format(browPeakSdkRotDefAuto,attribute), 
                                cd="{}.t{}".format(browPeakDriver,attribute), v=0, dv=0)
            mc.setDrivenKeyframe("{}.r{}".format(browPeakSdkRotDefAuto,attribute), 
                                cd="{}.t{}".format(browPeakDriver,attribute), v=.1, dv=1)
            mc.setDrivenKeyframe("{}.r{}".format(browPeakSdkRotDefAuto,attribute), 
                                cd="{}.t{}".format(browPeakDriver,attribute), v=-.1, dv=-1)

        # constrain the bind joints to the sdk nodes
        for jnt, sdkNode in zip((browMainJoint, browInnerJoint, browPeakJoint), (browMainSdk, browInnerSdk, browPeakSdk)):
            mc.pointConstraint(sdkNode, jnt)
            mc.orientConstraint(sdkNode, jnt)



    def postBuild(self):
        '''
        This will turn off driver visibility
        '''
        for driver in mc.ls("brow*_driver", type="joint"):
            mc.setAttr("{}.drawStyle".format(driver), 2)
