'''
This is the brow module. 

This contains class that handles the construction of the brow rig based on 
parameters passed in by the user.
'''
import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.control as control
import rigrepo.libs.common as common
import rigrepo.libs.cluster as cluster
import rigrepo.libs.attribute
import rigrepo.libs.wire

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
        self.addAttribute("curve", "brow_{side}_curve", attrType=str)
        self.addAttribute("geometry", "body_geo", attrType=str)
        
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
        curve = self.getAttributeByName("curve").getValue().format(side=side)
        browInnerJoint = self.getAttributeByName("browInnerJoint").getValue().format(browInner=browInner)
        browMainJoint = self.getAttributeByName("browMainJoint").getValue().format(browMain=browMain)
        browPeakJoint = self.getAttributeByName("browPeakJoint").getValue().format(browPeak=browPeak)
        driverParent = self.getAttributeByName("driverParent").getValue()
        geometry = self.getAttributeByName("geometry").getValue()
        mc.parent(self.name, driverParent)
        # going to create the control hierarchies.
        browMainNul, browMainOrient, browMainCtrl = control.create(name=browMain, 
                                                                    controlType="null", 
                                                                    hierarchy=['nul','ort'], 
                                                                    color=common.BLUE,
                                                                    parent=anchor,
                                                                    type='face')

        browInnerNul, browInnerOrient, browInnerCtrl = control.create(name=browInner, 
                                                                    controlType="null", 
                                                                    hierarchy=['nul','ort'], 
                                                                    color=common.BLUE,
                                                                    parent=anchor,
                                                                    type='face')

        browPeakNul, browPeakOrient, browPeakCtrl = control.create(name=browPeak, 
                                                                    controlType="null", 
                                                                    hierarchy=['nul','ort'], 
                                                                    color=common.BLUE,
                                                                    parent=anchor,
                                                                    type='face')


        # Position the controls
        #
        # Main
        mc.xform(browMainNul, ws=1, t=mc.xform(browMainJoint, q=1, ws=1, t=1))
        con = mc.orientConstraint(browMainJoint, browMainOrient)[0]
        if '_r_' in browMainJoint:
            mc.setAttr(con+'.offsetZ', -180)
            mc.setAttr(browMainNul+'.ry', -180)
            mc.setAttr(browMainNul+'.sz', -1)
        mc.delete(con)

        # Inner
        mc.xform(browInnerNul, ws=1, t=mc.xform(browInnerJoint, q=1, ws=1, t=1))
        con = mc.orientConstraint(browInnerJoint, browInnerOrient)[0]
        if '_r_' in browInnerJoint:
            mc.setAttr(con+'.offsetZ', -180)
            mc.setAttr(browInnerNul+'.ry', -180)
            mc.setAttr(browInnerNul+'.sz', -1)
        mc.delete(con)

        mc.xform(browPeakNul, ws=1, t=mc.xform(browPeakJoint, q=1, ws=1, t=1))
        con = mc.orientConstraint(browPeakJoint, browPeakOrient)[0]
        if '_r_' in browPeakJoint:
            mc.setAttr(con+'.offsetZ', -180)
            mc.setAttr(browPeakNul+'.ry', -180)
            mc.setAttr(browPeakNul+'.sz', -1)
        mc.delete(con)

        mc.parent(browInnerNul, browMainCtrl)
        mc.parent(browPeakNul, browMainCtrl)

        # create the driver nodes
        browMainDriverNul = mc.createNode("transform", name="{}_driver_nul".format(browMain), parent=self.name)
        browMainDriverOrt = mc.createNode("transform", name="{}_driver_ort".format(browMain), parent=browMainDriverNul)
        browMainDriver = mc.createNode("joint", name="{}_driver".format(browMain), parent=browMainDriverOrt)

        # position the driver
        mc.xform(browMainDriverNul, ws=True, matrix=mc.xform(browMainNul, q=True, ws=True, matrix=True))
        for attr in ['t', 'r', 's']:
            mc.connectAttr("{}.{}".format(browMainOrient, attr), "{}.{}".format(browMainDriverOrt, attr), f=True)

        mc.pointConstraint(browMainCtrl, browMainDriver)

        # TX and TY isolated drivers
        browMain_TX_driver = mc.duplicate(browMainDriver, po=1, name="{}_TX_driver".format(browMain))[0]
        browMain_TY_driver = mc.duplicate(browMainDriver, po=1, name="{}_TY_driver".format(browMain))[0]
        mc.connectAttr(browMainDriver+'.tx', browMain_TX_driver+'.tx')
        mc.connectAttr(browMainDriver+'.ty', browMain_TY_driver+'.ty')

        browInnerDriverNul = mc.createNode("transform", name="{}_driver_nul".format(browInner), parent=self.name)
        browInnerDriverOrt = mc.createNode("transform", name="{}_driver_ort".format(browInner), parent=browInnerDriverNul)
        browInnerDriver = mc.createNode("joint", name="{}_driver".format(browInner), parent=browInnerDriverOrt)

        # position the driver
        mc.xform(browInnerDriverNul, ws=True, matrix=mc.xform(browInnerNul, q=True, ws=True, matrix=True))

        for attr in ['t', 'r', 's']:
            mc.connectAttr("{}.{}".format(browInnerOrient, attr), "{}.{}".format(browInnerDriverOrt, attr), f=True)

        mc.pointConstraint(browInnerCtrl, browInnerDriver)

        # TX and TY isolated drivers
        browInner_TX_driver = mc.duplicate(browInnerDriver, po=1, name="{}_TX_driver".format(browInner))[0]
        browInner_TY_driver = mc.duplicate(browInnerDriver, po=1, name="{}_TY_driver".format(browInner))[0]
        mc.connectAttr(browInnerDriver+'.tx', browInner_TX_driver+'.tx')
        mc.connectAttr(browInnerDriver+'.ty', browInner_TY_driver+'.ty')

        browPeakDriverNul = mc.createNode("transform", name="{}_driver_nul".format(browPeak), parent=self.name)
        browPeakDriverOrt = mc.createNode("transform", name="{}_driver_ort".format(browPeak), parent=browPeakDriverNul)
        browPeakDriver = mc.createNode("joint", name="{}_driver".format(browPeak), parent=browPeakDriverOrt)

        # position the driver
        mc.xform(browPeakDriverNul, ws=True, matrix=mc.xform(browPeakNul, q=True, ws=True, matrix=True))

        for attr in ['t', 'r', 's']:
            mc.connectAttr("{}.{}".format(browPeakOrient, attr), "{}.{}".format(browPeakDriverOrt, attr), f=True)

        mc.pointConstraint(browPeakCtrl, browPeakDriver)

        # create the set driven key nodes.
        browMainSdkNul = mc.createNode("transform", name="{}_sdk_nul".format(browMain), parent=self.name)
        browMainSdkDefAuto = mc.createNode("transform", name="{}_sdk_def_auto".format(browMain), parent=browMainSdkNul)
        browMainSdkRotDefAuto = mc.createNode("transform", name="{}_sdk_rot_def_auto".format(browMain), parent=browMainSdkDefAuto)
        browMainSdk = mc.createNode("transform", name="{}_sdk".format(browMain), parent=browMainSdkRotDefAuto)

        # position the SDK nodes thanks
        mc.xform(browMainSdkNul, ws=True, matrix=mc.xform(browMainDriverOrt, q=True, ws=True, matrix=True))

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

        # create the corrugator 
        corrugatorName = "brow_corrugator_{}".format(side)
        cluster.create(geometry, name=corrugatorName, parent=browInnerCtrl)

        # rename the cluster and control                                    
        mc.rename(corrugatorName, '{}_cluster'.format(corrugatorName))
        mc.rename('{}_ctrl'.format(corrugatorName), corrugatorName)
        mc.xform("{}_nul".format(corrugatorName), ws=True, matrix=mc.xform(browInnerCtrl, q=True, ws=True, matrix=True))
        mc.setAttr("{}.displayHandle".format(corrugatorName), 1)
        control.tagAsControl(corrugatorName, type='face')

        # lock and hide scale and rotates for all of the brow controls
        rigrepo.libs.attribute.lockAndHide([browMainCtrl, browInnerCtrl, browPeakCtrl, corrugatorName], ['r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz'])

        # Set driven keys to be post and pre infinity
        driven_keys = mc.listConnections(browMainDriver, type='animCurveUA')
        driven_keys += mc.listConnections(browMainDriver, type='animCurveUL')
        driven_keys += mc.listConnections(browInnerDriver, type='animCurveUA')
        driven_keys += mc.listConnections(browInnerDriver, type='animCurveUL')
        driven_keys += mc.listConnections(browPeakDriver, type='animCurveUA')
        driven_keys += mc.listConnections(browPeakDriver, type='animCurveUL')

        for x in driven_keys:
            mc.setAttr(x + '.preInfinity', 1)
            mc.setAttr(x + '.postInfinity', 1)
            mc.keyTangent(x, index=(0, 0), inTangentType='spline')
            mc.keyTangent(x, index=(0, 0), outTangentType='spline')
            mc.keyTangent(x, index=(2, 2), inTangentType='spline')
            mc.keyTangent(x, index=(2, 2), outTangentType='spline')

        # create the curve rig for the brows.
        curveControlNames = ['brow_bend_{}_{}'.format(index, side) for index in range(len(mc.ls('{}.cv'.format(curve), fl=True)))]
        curveRig = rigrepo.libs.wire.buildCurveRig(curve, 
                                            name='brow_bend_{}'.format(side), 
                                            ctrl_names=curveControlNames, 
                                            parent=self.rigGroup, 
                                            control_type='face',
                                            control_color=rigrepo.libs.common.RED)
        bindmeshGeometry, follicleList, controlHieracrchyList, jointList, baseCurveJointList = curveRig

        for controlHieracrchy in controlHieracrchyList:
            shapeNode = mc.listRelatives(controlHieracrchy[-1], c=True, shapes=True)[0]
            mc.setAttr('{}.lodv'.format(shapeNode), 0)

        # create the wire deformer.
        # create the skinCluster for the curve
        wireDeformer = mc.wire(geometry, gw=False, en=1.00, ce=0.00, li=0.00,
                w=curve, name="{}_wire".format(curve))[0]
        # set the default values for the wire deformer
        mc.setAttr("{}.rotation".format(wireDeformer), 0)
        mc.setAttr("{}.dropoffDistance[0]".format(wireDeformer), 100)

        # create skinCluster for the base wire
        baseCurve = "{}BaseWire".format(curve)
        baseCurveSkin = mc.skinCluster(*baseCurveJointList+mc.ls(baseCurve),
                                    n="{}_skinCluster".format(baseCurve),
                                    tsb=True)[0]

        # parent the curves into the hiearchy.
        mc.parent([curve, baseCurve], 'brow_bend_{}_grp'.format(side))

    def postBuild(self):
        '''
        This will turn off driver visibility
        '''
        for driver in mc.ls("brow*_driver", type="joint"):
            mc.setAttr("{}.drawStyle".format(driver), 2)
