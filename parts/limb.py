'''
This is the limb base class.

Anything that uses a three joint chain ik/fk setup
should start with this class.
'''

import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.parts.part as part
import rigrepo.libs.ikfk
import rigrepo.libs.control
import rigrepo.libs.attribute
import rigrepo.libs.common
import rigrepo.libs.joint
import rigrepo.libs.curve
import rigrepo.libs.bindmesh
import rigrepo.libs.skinCluster

class Limb(part.Part):
    '''
    '''
    def __init__(self, name, jointList, anchor=None, dataObj=None, side="l"):
        '''
        This is the constructor.
        '''
        super(Limb, self).__init__(name, dataObj) 
        self.addAttribute("anchor", anchor, attrType=str)
        self.addAttribute("side", side, attrType=str)
        self.addAttribute("fkControls", ["{}_shoulder".format(side),
                                        "{}_elbow".format(side), 
                                        "{}_wrist".format(side)], 
                            attrType=list)
        self.addAttribute("ikControls", ["{}_limb_pv".format(side),
                                        "{}_limb_ik".format(side)],
                            attrType=list)
        side.capitalize()
        self.addAttribute("paramNode", "limb_{}".format(side.capitalize()), attrType=str)
        self.addAttribute("createBendyLimb", True, attrType=bool)
        self.addAttribute("displayLine", False, attrType=bool)
        self.addAttribute("createProxyAttributes", True, attrType=bool)
        self.addAttribute("geometry", "body_geo", attrType=str)
        self.jointList = jointList
        self._stretchTargetJointList = list()

    def build(self):
        '''
        This will build the limb part
        '''
        self._fkControls = list()
        self._ikControls = list()
        self._anchorGrp = str()
        side = self.getAttributeByName("side").getValue()
        paramNodeName = self.getAttributeByName("paramNode").getValue()
        fkControlNames = self.getAttributeByName("fkControls").getValue()
        ikControlNames = self.getAttributeByName("ikControls").getValue()
        createBendyLimb = self.getAttributeByName("createBendyLimb").getValue()
        createDisplayLine = self.getAttributeByName("displayLine").getValue()
        geometry = self.getAttributeByName("geometry").getValue()

        super(Limb, self).build()

        # create the param node and ikfk attribute for it
        paramNode = rigrepo.libs.control.create(name=paramNodeName, 
                                                controlType="cube",
                                                hierarchy=[],
                                                transformType="joint")[0]

        mc.parentConstraint(self.jointList[-1], paramNode,mo=False)
        mc.setAttr("{}.v".format(mc.listRelatives(paramNode, c=True, shapes=True)[0]), 0)
        rigrepo.libs.attribute.lockAndHide(paramNode, ("tx","ty","tz","rx","ry","rz","sx","sy","sz","v"))
        mc.select(cl=True)
        grp = mc.createNode("transform", name="{}_ikfk_grp".format(self.name))
        mc.parent(grp, self.name)
        # lock and hide attributes on the Param node that we don't need.
        mc.addAttr(paramNode, ln="ikfk", at="double", min=0, max=1, dv=0, keyable=True)

        mc.addAttr(grp, ln="ikfk", at="double", min=0, max=1, dv=0, keyable=True)
        ikfkAttr = "{0}.ikfk".format(paramNode)

        mc.connectAttr(ikfkAttr, "{0}.ikfk".format(grp), f=True)


        # create ikfk reverse node to connect the ikfk attribute
        reverseNode = mc.createNode("reverse", name="{0}_rvr".format(self.name))
        mc.connectAttr(ikfkAttr, "{0}.inputX".format(reverseNode), f=True)

        #-------------------------------------------------------------------------------------------
        #FK Setup for the limb
        #-------------------------------------------------------------------------------------------
        fkControlsNulList = list()
        parent = grp
        for jnt, fkCtrl in zip(self.jointList,fkControlNames):
            # make sure that the control is in the same position as the joint
            fkJntMatrix = mc.xform(jnt, q=True, ws=True, matrix=True)
            #append the fk control to the self._fkControls list
            self._fkControls.append(fkCtrl)
            # create the fk control hierarchy
            if fkCtrl == fkControlNames[-1]:
                rigrepo.libs.control.create(name=fkCtrl, 
                                                controlType="cube",
                                                hierarchy=[],
                                                transformType="joint",
                                                hideAttrs=["tx", "ty", "tz","v"],
                                                parent=parent)

                # create the gimbal control for the end control
                fkGimbalCtrl = rigrepo.libs.control.create(name=fkCtrl.replace("_{}".format(side), "_gimbal_{}".format(side)), 
                                                controlType="sphere",
                                                hierarchy=[],
                                                transformType="joint",
                                                hideAttrs=["tx", "ty", "tz","v"],
                                                parent=fkCtrl)[0]

                # move the gimbal ctrl to the correct location
                mc.xform(fkGimbalCtrl,ws=True,matrix=mc.xform(fkCtrl,q=True,ws=True,matrix=True))
                mc.xform(fkCtrl, ws=True, matrix=fkJntMatrix)
                cstCtrl = fkGimbalCtrl
            else:
                rigrepo.libs.control.create(name=fkCtrl, 
                                                controlType="cube",
                                                hierarchy=[],
                                                transformType="joint",
                                                hideAttrs=["tx", "ty", "tz", "sx", "sy", "sz", "v"],
                                                parent=parent)
                mc.xform(fkCtrl, ws=True, matrix=fkJntMatrix)
                cstCtrl = fkCtrl
                # setup the constraints from the control to the joint
            
            mc.pointConstraint(cstCtrl, jnt)
            mc.orientConstraint(cstCtrl, jnt)

            # add the param node to the control and connect it
            #mc.parent(paramNode, ctrl, add=True, s=True, r=True)
            parent = fkCtrl
            mc.connectAttr(ikfkAttr, "{0}.v".format(fkCtrl), f=True)

        rigrepo.libs.joint.rotateToOrient(self._fkControls)
        mc.setAttr("{}.preferredAngle".format(self._fkControls[1]), *mc.getAttr("{}.preferredAngle".format(self.jointList[1]))[0])
        
        handle = mc.ikHandle(sj=self._fkControls[0],  ee=self._fkControls[-1], 
                                        sol="ikRPsolver", 
                                        name="{0}_hdl".format(self._fkControls[-1]))[0]

        # create the polevector control
        poleVectorPos = rigrepo.libs.ikfk.IKFKLimb.getPoleVectorFromHandle(handle, self._fkControls)
        pvCtrlHierarchy = rigrepo.libs.control.create(name=ikControlNames[0], 
                                                controlType="diamond",
                                                hierarchy=['nul','ort'],
                                                position=poleVectorPos,
                                                hideAttrs=["v", "rx", "ry", "rz", "sx", "sy", "sz"],
                                                color=rigrepo.libs.common.GREEN)

        # get the handle and pv control
        pvCtrl = pvCtrlHierarchy[-1]
        pvCst = mc.poleVectorConstraint(pvCtrl, handle)[0]
        
        # set the pvMatch node attribute on the paramNode
        mc.addAttr(paramNode, ln="pvMatch", dt="string")
        pvMatchNode = mc.duplicate(pvCtrl, po=True, rr=True, name="{}_match".format(pvCtrl))[0]
        mc.setAttr("{}.pvMatch".format(paramNode), pvMatchNode, type="string")

        mc.parent(pvMatchNode, self._fkControls[0])

        # set the parent of the controls to be the rig group
        parent = grp

        endJointPos = mc.xform(self._fkControls[-1], q=True, ws=True, t=True)
        ikCtrlHierarchy = rigrepo.libs.control.create(name=ikControlNames[1], 
                                                controlType="cube",
                                                hierarchy=['nul','ort'],
                                                position=endJointPos,
                                                color=rigrepo.libs.common.GREEN)     

        ikCtrl = ikCtrlHierarchy[-1]
        rigrepo.libs.attribute.lockAndHide(ikCtrl, ["sx","sy","sz"])

        # add the gimbal control

        ikGimbalCtrl = rigrepo.libs.control.create(name=ikControlNames[1].replace("_{}".format(side), "_gimbal_{}".format(side)), 
                                                controlType="sphere",
                                                hierarchy=[],
                                                position=endJointPos,
                                                color=rigrepo.libs.common.MIDBLUE,
                                                parent=ikCtrl)[-1]

        mc.xform(ikGimbalCtrl,ws=True,matrix=mc.xform(ikCtrl,q=True,ws=True,matrix=True))

        # duplicate the end ik joint and make it offset joint for the 
        # ik control to drive the end joint
        mc.select(clear=True)
        dupEndJnt = mc.joint(name="{}_offset".format(self._fkControls[-1]))
        tempJnt = mc.joint(name="{}_offset_temp".format(self._fkControls[-1]))
        tempUpJnt = mc.joint(name="{}_offset_tempUp".format(self._fkControls[-1]))
        mc.parent(tempUpJnt, dupEndJnt)
        # get the aim vector we will be using to set the ik control default rotation

        distance = mc.getAttr("{}.t".format(self._fkControls[-1]))[0]
        aimAttr, aimVector = self._getDistanceVector(distance)
        # move the dupJnt and setup the tmp joints
        mc.xform(dupEndJnt, ws=True, matrix=mc.xform(self._fkControls[-1], q=True, ws=True, matrix=True))
        mc.setAttr('{}.t{}'.format(tempJnt, aimAttr.strip("-")),mc.getAttr('{}.t{}'.format(self._fkControls[-1], aimAttr.strip("-")))+2)
        mc.setAttr('{0}.ty'.format(tempUpJnt), 2)
        mc.parent([tempUpJnt,tempJnt], ikCtrl)
        upDistance = mc.getAttr("{}.t".format(tempUpJnt))[0]
        upAttr, upVector = self._getDistanceVector(upDistance)
        mc.parent([tempUpJnt,tempJnt], w=True)
        mc.delete(mc.aimConstraint(tempJnt, ikCtrl, wut="object", wuo=tempUpJnt,  aimVector=aimVector ,upVector=upVector)[0])
        mc.setAttr('{0}.drawStyle'.format(dupEndJnt), 2)
        mc.setAttr("{0}.v".format(handle), 0)
        mc.parent(dupEndJnt,ikGimbalCtrl)
        mc.setAttr("{0}.t".format(dupEndJnt),0,0,0)
        cst = mc.orientConstraint(dupEndJnt, self.jointList[-1])[0]
        wal = mc.orientConstraint(cst, q=True, wal=True)
        mc.parent(handle, dupEndJnt)
        mc.delete([tempUpJnt,tempJnt])

        # connect the switch to the constraint on the wrist
        mc.connectAttr("{0}.outputX".format(reverseNode), "{}.{}".format(cst, wal[1]), f=True)
        mc.connectAttr(ikfkAttr, "{}.{}".format(cst, wal[0]), f=True)

        # parent the controls to the parent group
        mc.parent((pvCtrlHierarchy[0],ikCtrlHierarchy[0]), parent)

        self._ikControls.extend([str(pvCtrl), str(ikCtrl),str(ikGimbalCtrl)])

        # setup the visibility and switch
        for ctrl in self._ikControls:
            if not mc.isConnected("{0}.outputX".format(reverseNode), "{0}.v".format(ctrl)):
                mc.connectAttr("{0}.outputX".format(reverseNode), "{0}.v".format(ctrl), f=True)

        # lock the scale attribute on the ikGimbal control
        rigrepo.libs.attribute.lockAndHide(ikGimbalCtrl, ["sx", "sy", "sz"])
        
        mc.connectAttr("{0}.outputX".format(reverseNode), "{0}.ikBlend".format(handle), f=True)
        # create the offset joint that will be used for ikfk switching. This is the offset of the
        # ik control from the fk control
        mc.select(clear=True)
        fkOffsetJnt = mc.joint(name="{}_offset".format(ikCtrl))
        mc.xform(fkOffsetJnt, ws=True, matrix=mc.xform(ikCtrl, q=True, ws=True, matrix=True))
        # turn off the visibility of the offset joint
        mc.setAttr('{0}.drawStyle'.format(fkOffsetJnt), 2)

        # parent the offset joint to the fk wrist control.
        mc.parent(fkOffsetJnt, fkGimbalCtrl)

        # make sure the rig is in fk before adding the stretch so it doesn't move the rig
        mc.setAttr(ikfkAttr, 1)

        # create the ik stretchy system
        self._stretchTargetJointList = rigrepo.libs.ikfk.IKFKLimb.createStretchIK(handle, grp)

        #create attributes on param node and connect them to the grp node
        mc.addAttr(paramNode, ln='stretch', at='double', dv = 1, min = 0, max = 1, k=True)
        mc.addAttr(paramNode, ln='stretchTop', at='double', min=0, dv = 1, k=True)
        mc.addAttr(paramNode, ln='stretchBottom', at='double', min=0, dv = 1, k=True)
        mc.addAttr(paramNode, ln='softStretch', at='double', min=0, max=1, dv=0.2, k=True)
        mc.addAttr(paramNode, ln='pvPin', at='double', min=0, max=1, dv=0, k=True)
        mc.addAttr(paramNode, ln='pvVis', at='long', min=0, max=1, dv=1, k=True)
        #rigrepo.libs.control.tagAsControl(paramNode)
        # add twist attribute to the param node
        mc.addAttr(paramNode, ln="twist", at="double", dv=0, keyable=True)
        mc.connectAttr("{}.twist".format(paramNode), "{}.twist".format(handle), f=True)
        for attr in ['stretch','stretchTop', 'stretchBottom', 'softStretch']:
            mc.connectAttr('{}.{}'.format(paramNode, attr), 
                        '{}.{}'.format(grp, attr), f=True)

        # connect pvVis to the visibility of the hierarchy of poleVector
        mc.connectAttr("{}.pvVis".format(paramNode), "{}.lodv".format(pvCtrlHierarchy[0]),f=True)        

        blendNode = mc.ls(mc.listConnections(self._fkControls[1], source=True),type="blendColors")[0]
        multiplyNode = mc.createNode("multDoubleLinear", n="{}_stretch_mdn".format(paramNode))
        mc.connectAttr("{}.stretch".format(paramNode), "{}.input1".format(multiplyNode),f=True)
        mc.connectAttr("{}.outputX".format(reverseNode), "{}.input2".format(multiplyNode), f=True)
        mc.connectAttr("{}.output".format(multiplyNode), "{}.blender".format(blendNode), f=True)

        # create pvPinning node network ---------------------------------------------------------
        # create the upper and lower distance between nodes.
        upperLimbDecomp = mc.createNode('decomposeMatrix', n="{}_upperPvPin_dcm".format(self.name))
        pvDecomp = mc.createNode('decomposeMatrix', n="{}_PvPin_dcm".format(self.name))
        upperDistanceBetweenNode = mc.createNode('distanceBetween', n="{}_upperPvPin_dst".format(self.name))
        # make a jnt to use as distance location for upper limb and put it in the same location as upper limb
        upperDistJnt = mc.joint(n="{}_upper_dist_jnt".format(self.name))
        mc.xform(upperDistJnt, ws=True, matrix=mc.xform(self._fkControls[0], q=True, ws=True, matrix=True))
        mc.parent(upperDistJnt, mc.listRelatives(self._fkControls[0],p=True)[0])
        mc.connectAttr("{}.worldMatrix[0]".format(upperDistJnt), "{}.inputMatrix".format(upperLimbDecomp), f=True)
        mc.connectAttr("{}.worldMatrix[0]".format(pvCtrl), "{}.inputMatrix".format(pvDecomp), f=True)
        mc.connectAttr("{}.outputTranslate".format(upperLimbDecomp), "{}.point1".format(upperDistanceBetweenNode), f=True)
        mc.connectAttr("{}.outputTranslate".format(pvDecomp), "{}.point2".format(upperDistanceBetweenNode), f=True)

        lowerLimbDecomp = mc.createNode('decomposeMatrix', n="{}_lowerPvPin_dcm".format(self.name))
        lowerDistanceBetweenNode = mc.createNode('distanceBetween', n="{}_lowerPvPin_dst".format(self.name))
        mc.connectAttr("{}.worldMatrix[0]".format(ikCtrl), "{}.inputMatrix".format(lowerLimbDecomp), f=True)
        mc.connectAttr("{}.outputTranslate".format(lowerLimbDecomp), "{}.point1".format(lowerDistanceBetweenNode), f=True)
        mc.connectAttr("{}.outputTranslate".format(pvDecomp), "{}.point2".format(lowerDistanceBetweenNode), f=True)


        # create the blendColor node for the pvPinning to override the stretch in the limb.
        pvPinBlendNode = mc.createNode("blendColors", n="{}_pvPin_bcn".format(self.name))
        # normalize the outputs so we can put it into the stretch attribute on the joint.
        multDivideNormalize = mc.createNode("multiplyDivide", n="{}_pvPin_mdn".format(self.name))
        mc.connectAttr("{}.outputR".format(blendNode), "{}.input1X".format(multDivideNormalize), f=True)
        mc.connectAttr("{}.outputG".format(blendNode), "{}.input1Y".format(multDivideNormalize), f=True)

        # set the attributes to normalize the value before it goes into the blend colors node.
        mc.setAttr("{}.input2X".format(multDivideNormalize), mc.getAttr("{}.input1X".format(multDivideNormalize)))
        mc.setAttr("{}.input2Y".format(multDivideNormalize), mc.getAttr("{}.input1Y".format(multDivideNormalize)))

        # set the operation to divide.
        mc.setAttr("{}.operation".format(multDivideNormalize), 2)

        # connect the attributes to the blend colors node.
        mc.connectAttr("{}.outputX".format(multDivideNormalize), "{}.color2R".format(pvPinBlendNode), f=True)
        mc.connectAttr("{}.outputY".format(multDivideNormalize), "{}.color2G".format(pvPinBlendNode), f=True)

        # get the aimVector and aim Attr
        aimDistance = mc.getAttr("{}.t".format(self.jointList[1]))[0]
        aimAttr, aimVector = self._getDistanceVector(aimDistance)
        # disconnect the translates. We will have to fix this in the stretch later.
        mc.disconnectAttr("{}.outputR".format(blendNode), "{}.t{}".format(self._fkControls[1], aimAttr.strip("-")))
        mc.disconnectAttr("{}.outputG".format(blendNode), "{}.t{}".format(self._fkControls[2], aimAttr.strip("-")))

        # make sure if it is a negative direction that we account for that and invert the values
        # coming into the pinning blend node.
        multDivideDistanceNormalize = mc.createNode("multiplyDivide", n="{}_pvDistance_mdn".format(self.name))
        mc.setAttr("{}.operation".format(multDivideDistanceNormalize), 2)
        if "-" in aimAttr:
            pvPinUpperRvrMultDouble = mc.createNode("multDoubleLinear", n="{}_PvPinUpperRvr_mdl".format(self.name))
            pvPinLowerRvrMultDouble = mc.createNode("multDoubleLinear", n="{}_PvPinLowerRvr_mdl".format(self.name))
            mc.connectAttr("{}.distance".format(upperDistanceBetweenNode), "{}.input1".format(pvPinUpperRvrMultDouble), f=True)
            mc.connectAttr("{}.distance".format(lowerDistanceBetweenNode), "{}.input1".format(pvPinLowerRvrMultDouble), f=True)
            for node in (pvPinLowerRvrMultDouble, pvPinUpperRvrMultDouble):
                mc.setAttr("{}.input2".format(node), -1)
            mc.connectAttr("{}.output".format(pvPinUpperRvrMultDouble), "{}.input1X".format(multDivideDistanceNormalize), f=True)
            mc.connectAttr("{}.output".format(pvPinLowerRvrMultDouble), "{}.input1Y".format(multDivideDistanceNormalize), f=True)
        else:
            mc.connectAttr("{}.distance".format(upperDistanceBetweenNode), "{}.input1X".format(multDivideDistanceNormalize), f=True)
            mc.connectAttr("{}.distance".format(lowerDistanceBetweenNode), "{}.input1Y".format(multDivideDistanceNormalize), f=True)

        mc.connectAttr("{}.outputX".format(multDivideDistanceNormalize), "{}.color1R".format(pvPinBlendNode), f=True)
        mc.connectAttr("{}.outputY".format(multDivideDistanceNormalize), "{}.color1G".format(pvPinBlendNode), f=True)
        # set the attributes to normalize the value before it goes into the blend colors node.
        mc.setAttr("{}.input2X".format(multDivideDistanceNormalize), mc.getAttr("{}.input1X".format(multDivideNormalize)))
        mc.setAttr("{}.input2Y".format(multDivideDistanceNormalize), mc.getAttr("{}.input1Y".format(multDivideNormalize)))

        # set the operation to divide.
        mc.setAttr("{}.operation".format(multDivideNormalize), 2)

        # create the multiplier to have pvPinning on during IK only and pinning on
        pvPinMultDouble = mc.createNode("multDoubleLinear", n="{}_PvPin_mdl".format(self.name))
        mc.connectAttr("{}.pvPin".format(paramNode), "{}.input1".format(pvPinMultDouble), f=True)
        mc.connectAttr("{}.outputX".format(reverseNode), "{}.input2".format(pvPinMultDouble), f=True)
        mc.connectAttr("{}.output".format(pvPinMultDouble), "{}.blender".format(pvPinBlendNode), f=True)
        mc.connectAttr("{}.outputR".format(pvPinBlendNode), "{}.s{}".format(self._fkControls[0], aimAttr.strip("-")), f=True)
        mc.connectAttr("{}.outputG".format(pvPinBlendNode), "{}.s{}".format(self._fkControls[1], aimAttr.strip("-")), f=True)

        mc.parent(self._stretchTargetJointList[-1], dupEndJnt)

        # delete the original tranform that came with the locator paramNode
        #mc.delete(paramNodeTrs)
        mc.parent(paramNode, self.name)

        # Connect to passed anchor
        #
        anchor = self.getAttributeByName('anchor').getValue() or ""
        if mc.objExists(anchor):
            anchorGrp = mc.createNode('transform', n=self.name+'_anchor_grp', p=self.name) 
            self._anchorGrp = anchorGrp
            mc.xform(anchorGrp, ws=True, matrix=mc.xform(self.jointList[0], q=True, ws=True, matrix=True))
            mc.parentConstraint(anchor, anchorGrp, mo=1)
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 
        
        # create the curve that will be used for the bendy limb
        if createBendyLimb:
            pointList = list()
            for jnt in self.jointList:
                pointList.append(mc.xform(jnt, q=True, ws=True, t=True))
            pointList.insert(1, (om.MVector(*pointList[0])-om.MVector(*pointList[1]))/2 + om.MVector(*pointList[1]))
            pointList.insert(3, (om.MVector(*pointList[2])-om.MVector(*pointList[3]))/2 + om.MVector(*pointList[3]))
            curve = rigrepo.libs.curve.createCurveFromPoints(pointList, degree=2, name='{}_curve'.format(self.name))
            bindmeshGeometry, follicleList, controlHieracrchyList, jointList = self.__buildCurveRig(curve, name='{}_bend'.format(self.getName()),parent=self.name)

            if mc.objExists(geometry):
                #deform the lid bindmesh with the lid curve using a wire deformer.
                wireDeformer = mc.wire(geometry, gw=False, en=1.00, ce=0.00, li=0.00, 
                        w=curve, name="{}_wire".format(curve))[0]
                baseCurveJointList=list()
                for jnt, controlList in zip(jointList, controlHieracrchyList):
                    # create the joint that we will use later to deform the base wire.
                    baseCurveJoint = mc.joint(name=jnt.replace("_jnt","_baseCurve_jnt"))
                    baseCurveJointList.append(baseCurveJoint)
                    # hide the base curve joint. Then parent it under the null node
                    mc.setAttr("{}.v".format(baseCurveJoint), 0)
                    mc.parent(baseCurveJoint, controlList[1])
                    mc.setAttr("{}.t".format(baseCurveJoint), 0, 0, 0)

                baseCurve = "{}BaseWire".format(curve)
                mc.parent([curve,baseCurve], self.name)
                baseCurveSkin = mc.skinCluster(*[baseCurveJointList]+mc.ls(baseCurve), 
                                            n="{}_skinCluster".format(baseCurve),
                                            tsb=True)[0]

                # set the default values for the wire deformer
                #mc.setAttr("{}.rotation".format(wireDeformer), 0)
                mc.setAttr("{}.dropoffDistance[0]".format(wireDeformer), 100)

            bindMeshSkin = mc.skinCluster(*self.jointList+mc.ls(bindmeshGeometry), 
                                                n="{}_skinCluster".format(bindmeshGeometry),
                                                tsb=True)[0]

            mc.skinPercent(bindMeshSkin , '{}.vtx[0:3]'.format(bindmeshGeometry), transformValue=[(self.jointList[0], 1.0), (self.jointList[1], 0.0), (self.jointList[2],0.0)])
            mc.skinPercent(bindMeshSkin , '{}.vtx[4:7]'.format(bindmeshGeometry),  transformValue=[(self.jointList[0], 0.5), (self.jointList[1], 0.5), (self.jointList[2],0.0)])
            mc.skinPercent(bindMeshSkin , '{}.vtx[8:11]'.format(bindmeshGeometry), transformValue=[(self.jointList[0], 0.0), (self.jointList[1], 1.0), (self.jointList[2],0.0)])
            mc.skinPercent(bindMeshSkin , '{}.vtx[12:15]'.format(bindmeshGeometry), transformValue=[(self.jointList[0], 0.0), (self.jointList[1], 0.5), (self.jointList[2],0.5)])
            mc.skinPercent(bindMeshSkin , '{}.vtx[16:19]'.format(bindmeshGeometry), transformValue=[(self.jointList[0], 0.0), (self.jointList[1], 0.0), (self.jointList[2],1.0)])

            #mc.parentConstraint(self.jointList[0], baseCurveJointList[0], mo=True)
            mc.pointConstraint(self.jointList[0],self.jointList[1], baseCurveJointList[1], mo=True)
            mc.orientConstraint(self.jointList[0], baseCurveJointList[1], mo=True)
            #mc.parentConstraint(self.jointList[1], baseCurveJointList[2], mo=True)
            mc.pointConstraint(self.jointList[1],self.jointList[2], baseCurveJointList[3], mo=True)
            mc.orientConstraint(self.jointList[1], baseCurveJointList[3], mo=True)
            #mc.parentConstraint(self.jointList[2], baseCurveJointList[4], mo=True)

            #mc.parentConstraint(self.jointList[0], controlHieracrchyList[0][0], mo=True)
            mc.pointConstraint(self.jointList[0],self.jointList[1], controlHieracrchyList[1][0], mo=True)
            mc.orientConstraint(self.jointList[0], controlHieracrchyList[1][0], mo=True)
            #mc.parentConstraint(self.jointList[1], controlHieracrchyList[2][0], mo=True)
            mc.pointConstraint(self.jointList[1],self.jointList[2], controlHieracrchyList[3][0], mo=True)
            mc.orientConstraint(self.jointList[1], controlHieracrchyList[3][0], mo=True)
            #mc.parentConstraint(self.jointList[2], controlHieracrchyList[4][0], mo=True)

        #------------------------------------------------------------------------------------------
        #Setup attributes on the param node for the ikfk switch.
        #------------------------------------------------------------------------------------------
        # fk match attributes needed to the switch
        mc.addAttr(paramNode, ln="fkMatchTransforms", dt="string")
        mc.setAttr("{}.fkMatchTransforms".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(self._fkControls[0], self._fkControls[1], fkOffsetJnt), 
                type="string")

        mc.addAttr(paramNode, ln="fkControls", dt="string")
        mc.setAttr("{}.fkControls".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(*self._fkControls), 
                type="string")

        # ik match attributes needed for the switch
        mc.addAttr(paramNode, ln="ikMatchTransforms", dt="string")
        mc.setAttr("{}.ikMatchTransforms".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(*self.jointList), 
                type="string")
        mc.addAttr(paramNode, ln="ikControls", dt="string")
        mc.setAttr("{}.ikControls".format(paramNode), 
                '["{0}","{1}"]'.format(*self._ikControls[:-1]), 
                type="string")

        # command to be called when switch is being used.
        mc.addAttr(paramNode, ln="switchCommand", dt="string")
        mc.setAttr("{}.switchCommand".format(paramNode), "rigrepo.parts.limb.Limb.switch", 
                    type="string")

        # set softStretch to zero and zero out fk controls. This will allow the rest of the
        # rig to build properly. We will have to turn these things back on somewhere in the 
        # build later
        # zero out controls
        for control in self._fkControls:
            mc.setAttr("{}.r".format(control), 0, 0, 0)
        # set the param node to zero
        mc.setAttr("{}.softStretch".format(paramNode), .001)

        # lock and hide attributes for the fk controls
        #rigrepo.libs.attribute.lockAndHide(self._fkControls, ["tx", "ty", "tz", "sx", "sy", "sz", "v"])
        # add fk gimbal control to the fk control list
        self._fkControls.append(fkGimbalCtrl)
        if createDisplayLine:
            elbow = self.jointList[1]
            if createBendyLimb:
                elbow = controlHieracrchyList[2][-1]
            curve = rigrepo.libs.control.displayLine(elbow, pvCtrl, 
                                        name='{}_display_line'.format(pvCtrl), 
                                        parent=self.name, 
                                        displayType=1)
            mc.connectAttr("{0}.outputX".format(reverseNode), "{0}.v".format(curve), f=True)
            # connect the display line lodVis to the pvVis attribute
            mc.connectAttr("{}.pvVis".format(paramNode), "{}.lodv".format(curve), f=True)

        # Locking translates because of anim issue
        mc.setAttr(handle+'.tx', l=1)
        mc.setAttr(handle+'.ty', l=1)
        mc.setAttr(handle+'.tz', l=1)


    def postBuild(self):
        '''
        '''
        #turn of the visibility of the ikfk system
        #mc.setAttr("{0}.v".format(self.ikfkSystem.getGroup()), 0)
        paramNodeName = self.getAttributeByName("paramNode").getValue()
        createProxyAttributes = self.getAttributeByName("createProxyAttributes").getValue()

        
        # NO TWIST JOINT
        side = self.getAttributeByName("side").getValue()
        nameSplit = self.jointList[0].split('_{}_'.format(side))
        noTwist = '{}NoTwist_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        target = self.jointList[1]
        aimDistance = mc.getAttr("{}.t".format(self.jointList[1]))[0]
        aimAttr, aimVector = self._getDistanceVector(aimDistance)
        if mc.objExists(noTwist):
            mc.aimConstraint(target, noTwist, mo=1, weight=1, aimVector=aimVector, upVector=(0, 0, 0), worldUpType='none')            
            distanceUpperJnt = "{}_upper_dist_jnt".format(self.name)
            
            if mc.objExists(distanceUpperJnt):
                mc.pointConstraint(noTwist, distanceUpperJnt, mo=0)
                mc.setAttr("{}.v".format(distanceUpperJnt), 0 )
        else:
            print('noTwist not found', noTwist)

        # TWIST JOINTS ------------------------------------------------------------
        # FIRSY JOINT twist setup
        joint = self.jointList[1]
        target = self.jointList[0]
        nameSplit = joint.split('_{}_'.format(side))
        aimVector = [value * -1 for value in aimVector]
        elbowTwistJoint = '{}Twist_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        if mc.objExists(noTwist):
            mc.aimConstraint(target, elbowTwistJoint, mo=1, weight=1, aimVector=aimVector, upVector=(0, 0, 0), worldUpType='none')
        else:
            print('noTwist not found', elbowTwistJoint)

        # LAST JOINT twist setup
        joint = self.jointList[-1]
        nameSplit = joint.split('_{}_'.format(side))
        twistJoint = '{}Twist_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        if mc.objExists(twistJoint):
            if "-" in aimAttr:
                decompAimAttr = aimAttr.strip("-")
            else:
                decompAimAttr = "-{}".format(aimAttr)
            rigrepo.libs.transform.decomposeRotation(joint, twistAxis=decompAimAttr)
            # make sure we create a node for the pv foot space. We need to make a twist joint 
            # that follows the ik control
            offsetJoint = "{}_offset".format(self._fkControls[-2])
            
            if mc.objExists(offsetJoint):
                # create the pvSpaceNode and make sure it's in the correct space
                pvSpaceNode = mc.createNode("joint", name="{}_pv".format(offsetJoint))
                #cstJoint = mc.createNode("joint", name="{}_cst_jnt".format(offsetJoint))
                #mc.parent((cstJoint,pvSpaceNode), mc.listRelatives(self._ikControls[1], p=True)[0])
                mc.parent(pvSpaceNode, offsetJoint)
                mc.setAttr("{}.t".format(pvSpaceNode),0,0,0)
                mc.setAttr("{}.r".format(pvSpaceNode),0,0,0)
                # turn off the visibility of the joint
                mc.setAttr("{}.v".format(pvSpaceNode), 0)
                mc.aimConstraint(self._fkControls[0], pvSpaceNode, mo=0, weight=1, aimVector=aimVector, upVector=(0, 0, 0), worldUpType='none')
                #mc.connectAttr("{}.t".format(self._ikControls[1]), "{}.t".format(pvSpaceNode), f=True)
                #mc.pointConstraint(offsetJoint, mc.listRelatives(self._fkControls[0],p=True)[0] , cstJoint,mo=False)
                #mc.orientConstraint(offsetJoint,cstJoint,mo=False)
                # decompose the rotation
                #rigrepo.libs.transform.decomposeRotation(cstJoint, twistAxis=decompAimAttr)
                #mc.connectAttr('{}.decomposeTwist'.format(cstJoint), '{}.r{}'.format(pvSpaceNode, aimAttr.strip("-")), f=1)
            mc.connectAttr('{}.decomposeTwist'.format(joint), '{}.r{}'.format(twistJoint, aimAttr.strip("-")), f=1)
        else:
            print('No twist joint found', twistJoint)

        if createProxyAttributes:
            for control in self._ikControls + self._fkControls:
                mc.addAttr(control, ln="settings", at="enum", enumName="settings",keyable=True)
                rigrepo.libs.attribute.lock(control, ['settings'])
                mc.addAttr(control, ln="ikfk", at="double", min=0, max=1, dv=0, keyable=True, proxy='{}.ikfk'.format(paramNodeName))
                mc.addAttr(control, ln='stretch', at='double', dv = 1, min = 0, max = 1, k=True, proxy='{}.stretch'.format(paramNodeName))
                mc.addAttr(control, ln='stretchTop', at='double', min=0, dv = 1, k=True, proxy='{}.stretchTop'.format(paramNodeName))
                mc.addAttr(control, ln='stretchBottom', at='double', min=0, dv = 1, k=True, proxy='{}.stretchBottom'.format(paramNodeName))
                mc.addAttr(control, ln='softStretch', at='double', min=0, max=1, dv=0.2, k=True, proxy='{}.softStretch'.format(paramNodeName))
                mc.addAttr(control, ln='pvPin', at='double', min=0, max=1, dv=1, k=True, proxy='{}.pvPin'.format(paramNodeName))

        # get the bindmesh skinCluster if it exists.
        bindmesh = "{}_bend_bindmesh".format(self.name)
        bindMeshSkinCluster = None
        if mc.objExists(bindmesh):
            bindMeshSkinCluster = rigrepo.libs.skinCluster.getSkinCluster(bindmesh)

        if bindMeshSkinCluster:
            for jnt in (noTwist ,twistJoint, elbowTwistJoint):
                mc.skinCluster(bindMeshSkinCluster, e=True, ai=jnt)
            bindmeshGeometry = mc.skinCluster(bindMeshSkinCluster, q=True, geometry=True)[0]
            mc.skinPercent(bindMeshSkinCluster , '{}.vtx[0:3]'.format(bindmeshGeometry), 
                            transformValue=[(noTwist, 1.0), 
                                            (elbowTwistJoint, 0.0), 
                                            (self.jointList[0], 0.0), 
                                            (self.jointList[1], 0.0), 
                                            (self.jointList[2],0.0), 
                                            (twistJoint, 0.0)])
            mc.skinPercent(bindMeshSkinCluster , '{}.vtx[4:7]'.format(bindmeshGeometry), 
                            transformValue=[(noTwist, 0.5), 
                                            (elbowTwistJoint, 0.5), 
                                            (self.jointList[0], 0.0), 
                                            (self.jointList[1], 0.0), 
                                            (self.jointList[2],0.0), 
                                            (twistJoint, 0.0)])
            mc.skinPercent(bindMeshSkinCluster , '{}.vtx[8:11]'.format(bindmeshGeometry), 
                            transformValue=[(noTwist, 0.0), 
                                            (elbowTwistJoint, 0.5), 
                                            (self.jointList[0], 0.0), 
                                            (self.jointList[1], 0.5), 
                                            (self.jointList[2],0.0), 
                                            (twistJoint, 0.0)])
            mc.skinPercent(bindMeshSkinCluster , '{}.vtx[12:15]'.format(bindmeshGeometry), 
                            transformValue=[(noTwist, 0.0), 
                                            (elbowTwistJoint, 0.0), 
                                            (self.jointList[0], 0.0), 
                                            (self.jointList[1], 0.5), 
                                            (self.jointList[2],0.0), 
                                            (twistJoint, 0.5)])
            mc.skinPercent(bindMeshSkinCluster , '{}.vtx[16:19]'.format(bindmeshGeometry), 
                            transformValue=[(noTwist, 0.0), 
                                            (elbowTwistJoint, 0.0), 
                                            (self.jointList[0], 0.0), 
                                            (self.jointList[1], 0.0), 
                                            (self.jointList[2],0.0), 
                                            (twistJoint, 1.0)])

        rigrepo.libs.attribute.lockAndHide(self._fkControls,["tx","ty", "tz"])

    def __buildCurveRig(self, curve, name='limb_bend', parent=None):
        '''
        This will build a rig setup based on the curve that is passed in.

        :param joints: NurbsCurve name you want to build the rig on.
        :type joints: list |tuple

        :param name: This will be used to name the control hierachy and joints in the rig.
        :type name: str

        :return: This method will return the data needed to make adjustments to rig.
        :rtype: tuple
        '''

        # If the name passed in doesn't exist, we will create a transform as the parent group
        # for the rig.
        if not mc.objExists(name):
            mc.createNode("transform", n=name)
        # create the bindmesh 
        #
        # follicleList = (follicle transform, follicle shape) 
        # bindmeshGeometry = geometry name of bindmesh
        #
        bindmeshGeometry, follicleList = rigrepo.libs.bindmesh.createFromCurve(name, curve)
        # emptry list to append controls to in the loop
        controlHieracrchyList = list()
        jointList = list()

        # loop through and create controls on the follicles so we have controls to deform the wire.
        for follicle in follicleList:
            # get the follicle transform so we can use it to parent the control to it.
            follicleIndex = follicleList.index(follicle)
            # create the control with a large enough hierarchy to create proper SDK's
            ctrlHierarchy = rigrepo.libs.control.create(name="{}_{}".format(name, follicleIndex), 
                controlType="circle", 
                hierarchy=['nul','ort','def_auto'], 
                parent=follicle)

            # this is meant to translate only. So we will lock and hide all other attributes.
            rigrepo.libs.attribute.lockAndHide(ctrlHierarchy[-1], ['rx', 'ry', 'rz', 'r', 
                                                                   'sx', 'sy', 'sz', 's'])

            # create the joint that will drive the curve.
            jnt = mc.joint(n="{}_{}_jnt".format(name, follicleIndex))
            # make sure the joint is in the correct space
            mc.setAttr("{}.translate".format(jnt), 0,0,0)
            mc.setAttr("{}.rotate".format(jnt), 0,0,0)
            mc.setAttr("{}.drawStyle".format(jnt),2)
            mc.setAttr("{}.displayHandle".format(ctrlHierarchy[-1]), 1)
            #mc.delete(mc.listRelatives(ctrlHierarchy[-1], c=True, shapes=True)[0])

            # zero out the nul for the control hierarchy so it's in the correct position.
            mc.setAttr("{}.translate".format(ctrlHierarchy[0]), 0,0,0)
            #mc.setAttr("{}.rotate".format(ctrlHierarchy[0]), 0,0,0)
            # set the visibility of the shape node for the follicle to be off.
            # append the control and the follicle transform to their lists
            controlHieracrchyList.append(ctrlHierarchy)
            jointList.append(jnt)

        # This will parent all of the data for the rig to the system group "name"
        for data in (bindmeshGeometry, follicleList):
            mc.parent(data, name)

        # This is dumb but the most consitent way for me to get the right behavior
        # parenting the last joint to the first on to grab the axis I want to use for aiming
        mc.parent(jointList[-1], jointList[0])
        # get the axis we want to use to aim. 
        aimDistance = mc.getAttr("{}.t".format(jointList[-1]))[0]
        aimAttr, aimVector = self._getDistanceVector(aimDistance)
        # parent the joint back to the control
        mc.parent(jointList[-1], controlHieracrchyList[-1][-1])
        mc.pointConstraint(controlHieracrchyList[0][-1],controlHieracrchyList[2][-1], controlHieracrchyList[1][2], mo=True)
        mc.aimConstraint(jointList[2], controlHieracrchyList[1][2], mo=True, w=1, upVector=(0,0,0), aimVector=aimVector, wut="none")
        mc.aimConstraint(jointList[1], jointList[0], upVector=(0,0,0), mo=True, w=1, aimVector=aimVector, wut="none")


        # This is dumb but the most consitent way for me to get the right behavior
        # parenting the last joint to the first on to grab the axis I want to use for aiming
        mc.parent(jointList[0], jointList[-1])
        aimDistance = mc.getAttr("{}.t".format(jointList[0]))[0]
        aimAttr, aimVector = self._getDistanceVector(aimDistance)
        # parent the joint back to the control
        mc.parent(jointList[0], controlHieracrchyList[0][-1])
        mc.pointConstraint(controlHieracrchyList[2][-1],controlHieracrchyList[4][-1], controlHieracrchyList[3][2], mo=True)
        mc.aimConstraint(jointList[2], controlHieracrchyList[3][2], mo=True, w=1, upVector=(0,0,0), aimVector=aimVector, wut="none")
        mc.aimConstraint(jointList[-2], jointList[-1], upVector=(0,0,0), mo=True, w=1, aimVector=aimVector, wut="none")


        # If parent the parent is passed in we will parent the system to the parent.
        if parent:
            if not mc.objExists(parent):
                mc.warning('Created the system but the current parent "{}" does not exist in the \
                    current Maya session.'.format(parent))
            else:
                mc.parent(name, parent)

        # create the skinCluster for the curve
        mc.skinCluster(*jointList + [curve], tsb=True, name="{}_skinCluster".format(curve))

        # set the visibility of the bindmesh.
        mc.setAttr("{}.v".format(bindmeshGeometry), 0 )
        mc.setAttr("{}.v".format(curve), 0 )        
        return bindmeshGeometry, follicleList, controlHieracrchyList, jointList

    @staticmethod
    def switch(paramNode, value):
        '''
        '''
        if not mc.objExists(paramNode):
            raise RuntimeError("{} doesn't exist in the current Maya session".format(paramNode))
        # if we're in ik modes, we will match fk to the ik position and switch it to fk
        mc.undoInfo(openChunk=1)
        if value == 0:
            fkControls = eval(mc.getAttr("{}.fkControls".format(paramNode)))
            ikMatchTransforms = eval(mc.getAttr("{}.ikMatchTransforms".format(paramNode)))
            rigrepo.libs.ikfk.IKFKLimb.fkMatchIk(fkControls, ikMatchTransforms)
            mc.setAttr("{}.ikfk".format(paramNode), 1)
        elif value == 1:
            # get the ik controls
            ikControls = eval(mc.getAttr("{}.ikControls".format(paramNode)))
            # get the fk transforms
            fkMatchTransforms = eval(mc.getAttr("{}.fkMatchTransforms".format(paramNode)))
            # get the match node for the pole vector node
            matchNode = mc.getAttr("{}.pvMatch".format(paramNode))
            # get the current distance between the joints
            currentDistance = mc.getAttr("{}.tx".format(fkMatchTransforms[1])) + mc.getAttr("{}.tx".format(fkMatchTransforms[2]))
            # check to see if the distance in negative, which means we have to treat the matching differently
            flip = False
            if currentDistance < 0:
                flip=True
            rigrepo.libs.ikfk.IKFKLimb.ikMatchFk(fkMatchTransforms, ikControls[1], ikControls[0], matchNode)
            mc.setAttr("{}.ikfk".format(paramNode), 0)
            newDistance = mc.getAttr("{}.tx".format(fkMatchTransforms[1])) + mc.getAttr("{}.tx".format(fkMatchTransforms[2]))
            updatedDistance = (newDistance - currentDistance) / 2
            # get the new distance
            # check what direction the delta is in. If we need to flip it we will use abs to match
            if flip:
                if updatedDistance < 0:
                    for attr in ["stretchTop", "stretchBottom"]:
                        mc.setAttr("{}.{}".format(paramNode, attr), mc.getAttr("{}.{}".format(paramNode, attr)) - abs(updatedDistance))
            elif updatedDistance > 0:
                for attr in ["stretchTop", "stretchBottom"]:
                    mc.setAttr("{}.{}".format(paramNode, attr), mc.getAttr("{}.{}".format(paramNode, attr)) - updatedDistance)

        mc.undoInfo(closeChunk=1)

    def _getDistanceVector(self, distance):
        '''
        '''
        distanceValue = max(distance, key=abs)
        index = distance.index(distanceValue)
        attr = ["x","y","z"][index]
        value = round(distance[index], 4)
        if attr == "x":
            if value < 0:
                attr = "-x"
                vector = [-1,0,0]
            else:
                vector = [1,0,0]
        elif attr == "y":
            if value < 0:
                attr = "-y"
                vector = [0,-1,0]
            else:
                vector = [0,1,0]
        elif attr == "z":
            if value < 0:
                attr = "-z"
                vector = [0,0,-1]
            else:
                vector = [0,0,1]

        return (attr, vector)
"""
class LimbOld(part.Part):
    '''
    '''
    def __init__(self, name, jointList, anchor=None, dataObj=None, side="l"):
        '''
        This is the constructor.
        '''
        super(LimbOld, self).__init__(name, dataObj) 
        self._fkControls = list()
        self._ikControls = list()
        self._anchorGrp = str()
        self.addAttribute("anchor", anchor, attrType=str)
        self.addAttribute("side", side, attrType=str)
        self.addAttribute("fkControls", ["{}_shoulder".format(side),
                                        "{}_elbow".format(side), 
                                        "{}_wrist".format(side)], 
                            attrType=list)
        self.addAttribute("ikControls", ["{}_limb_pv".format(side),
                                        "{}_limb_ik".format(side)],
                            attrType=list)
        side.capitalize()
        self.addAttribute("paramNode", "limb_{}".format(side), attrType=str)
        self.jointList = jointList
        self._stretchTargetJointList = list()

    def build(self):
        '''
        This will build the limb part
        '''
        self.ikfkSystem = rigrepo.libs.ikfk.IKFKLimb(self.jointList)
        side = self.getAttributeByName("side").getValue()
        paramNodeName = self.getAttributeByName("paramNode").getValue()
        fkControlNames = self.getAttributeByName("fkControls").getValue()
        ikControlNames = self.getAttributeByName("ikControls").getValue()

        super(Limb, self).build()

        self.ikfkSystem.create()

        # create the param node and ikfk attribute for it
        paramNode = mc.createNode("locator", name=paramNodeName)
        paramNodeTrs = mc.listRelatives(paramNode, p=True)[0]

        # lock and hide attributes on the Param node that we don't need.
        rigrepo.libs.attribute.lockAndHide(paramNode, ['lpx','lpy','lpz','lsx','lsy','lsz'])

        mc.setAttr("{0}.v".format(paramNode), 0)
        mc.addAttr(paramNode, ln="ikfk", at="double", min=0, max=1, dv=0, keyable=True)
        ikfkAttr = "{0}.ikfk".format(paramNode)


        #connect the param ikfk attr to the ikfk system group ikfk attribute
        mc.connectAttr(ikfkAttr, "{0}.ikfk".format(self.ikfkSystem.getGroup()), f=True)


        # create ikfk reverse node to connect the ikfk attribute
        reverseNode = mc.createNode("reverse", name="{0}_rvr".format(self.name))
        mc.connectAttr(ikfkAttr, "{0}.inputX".format(reverseNode), f=True)


        # get handle and create poleVector
        fkJointList = self.ikfkSystem.getFkJointList()
        ikJointList = self.ikfkSystem.getIkJointList()
        #poleVectorPos = self.ikfkSystem.getPoleVectorPosition(fkJointList)
        poleVectorPos = self.ikfkSystem.getPoleVectorFromHandle(self.ikfkSystem.getHandle(), fkJointList)

        pvCtrlHierarchy = rigrepo.libs.control.create(name=ikControlNames[0], 
                                                controlType="diamond",
                                                hierarchy=['nul','ort'],
                                                position=poleVectorPos,
                                                color=rigrepo.libs.common.GREEN)

        # get the handle and pv control
        pvCtrl = pvCtrlHierarchy[-1]
        mc.parent(paramNode, pvCtrl, s=True, r=True)
        handle = self.ikfkSystem.getHandle()
        mc.poleVectorConstraint(pvCtrl, handle)

        # set the parent of the controls to be the rig group
        parent = self.name

        endJointPos = mc.xform(ikJointList[-1], q=True, ws=True, t=True)
        ikCtrlHierarchy = rigrepo.libs.control.create(name=ikControlNames[1], 
                                                controlType="cube",
                                                hierarchy=['nul','ort'],
                                                position=endJointPos,
                                                color=rigrepo.libs.common.GREEN)     

        ikCtrl = ikCtrlHierarchy[-1]
        mc.parent(paramNode, ikCtrl, add=True, s=True, r=True)
        

        # duplicate the end ik joint and make it offset joint for the 
        # ik control to drive the end joint
        dupEndJnt = mc.duplicate(ikJointList[-1],
                                po=True, 
                                rr=True, 
                                name="{}_offset".format(ikJointList[-1]))[0]

        mc.setAttr('{0}.tx'.format(dupEndJnt),mc.getAttr('{0}.tx'.format(dupEndJnt))+2)
        mc.delete(mc.aimConstraint(dupEndJnt, ikCtrl)[0])
        mc.setAttr('{0}.drawStyle'.format(dupEndJnt), 2)

        mc.setAttr("{0}.v".format(handle), 0)
        mc.parent(dupEndJnt,ikCtrl)
        mc.setAttr("{0}.t".format(dupEndJnt),0,0,0)
        mc.orientConstraint(dupEndJnt, ikJointList[-1])

        # parent the controls to the parent group
        mc.parent((pvCtrlHierarchy[0],ikCtrlHierarchy[0]), parent)

        self._ikControls.extend([str(pvCtrl), str(ikCtrl)])

        # create the ik stretchy system
        grp = self.ikfkSystem.getGroup()
        self._stretchTargetJointList = self.ikfkSystem.createStretchIK(handle, grp)

        #create attributes on param node and connect them to the grp node
        mc.addAttr(paramNode, ln='stretch', at='double', dv = 1, min = 0, max = 1, k=True)
        mc.addAttr(paramNode, ln='stretchTop', at='double', min=0, dv = 1, k=True)
        mc.addAttr(paramNode, ln='stretchBottom', at='double', min=0, dv = 1, k=True)
        mc.addAttr(paramNode, ln='softStretch', at='double', min=0, max=1, dv=0.2, k=True)

        rigrepo.libs.control.tagAsControl(paramNode)

        for attr in ['stretch','stretchTop', 'stretchBottom', 'softStretch']:
            mc.connectAttr('{}.{}'.format(paramNode, attr), 
                        '{}.{}'.format(grp, attr), f=True)

        #mc.parent(handle, dupEndJnt)
        mc.parent(self._stretchTargetJointList[-1], dupEndJnt)

        for ctrl in self._ikControls:
            if not mc.isConnected("{0}.outputX".format(reverseNode), "{0}.v".format(ctrl)):
                mc.connectAttr("{0}.outputX".format(reverseNode), "{0}.v".format(ctrl), f=True)

        #-------------------------------------------------------------------------------------------
        #FK Setup for the limb
        #-------------------------------------------------------------------------------------------
        fkControlsNulList = list()
        for fkJnt, fkCtrl in zip(fkJointList,fkControlNames):
            # create the fk control hierarchy
            fkCtrlHierarchy = rigrepo.libs.control.create(name=fkCtrl, 
                                                controlType="cube",
                                                hierarchy=['nul','ort'])

            ctrl = fkCtrlHierarchy[-1]
            nul = fkCtrlHierarchy[0]

            #append nul to the nul list in case we need to use it for other things.
            fkControlsNulList.append(nul)

            # make sure that the control is in the same position as the joint
            fkJntMatrix = mc.xform(fkJnt, q=True, ws=True, matrix=True)
            mc.xform(nul, ws=True, matrix=fkJntMatrix)

            # setup the constraints from the control to the joint
            mc.pointConstraint(ctrl, fkJnt)
            mc.orientConstraint(ctrl, fkJnt)

            # add the param node to the control and connect it
            mc.parent(paramNode, ctrl, add=True, s=True, r=True)

            #parent the control to the parent node
            mc.parent(nul,parent)
            parent = ctrl
            mc.connectAttr(ikfkAttr, "{0}.v".format(ctrl), f=True)
            self._fkControls.append(str(ctrl))

        # create the offset joint that will be used for ikfk switching. This is the offset of the
        # ik control from the fk control
        mc.select(clear=True)
        fkOffsetJnt = mc.joint(name="{}_offset".format(fkJointList[-1]))
        mc.xform(fkOffsetJnt, ws=True, matrix=mc.xform(ikCtrl, q=True, ws=True, matrix=True))
        # turn off the visibility of the offset joint
        mc.setAttr('{0}.drawStyle'.format(fkOffsetJnt), 2)

        # parent the offset joint to the fk wrist control.
        mc.parent(fkOffsetJnt, self._fkControls[-1])

        # delete the original tranform that came with the locator paramNode
        mc.delete(paramNodeTrs)

        #rename ikfk group and parent it under the part name group
        self.ikfkSystem.setGroup("{0}_{1}".format(self.name,self.ikfkSystem.getGroup()))
        mc.parent(self.ikfkSystem.getGroup(), self.name)

        # Connect to passed anchor
        #
        anchor = self.getAttributeByName('anchor').getValue()
        if mc.objExists(anchor):
            anchorGrp = mc.createNode('transform', n=self.name+'_anchor_grp', p=self.name) 
            self._anchorGrp = anchorGrp
            mc.xform(anchorGrp, ws=True, matrix=mc.xform(ikJointList[0], q=True, ws=True, matrix=True))
            mc.parentConstraint(anchor, anchorGrp, mo=1)
            mc.parent(self.ikfkSystem.getGroup(), fkControlsNulList[0], anchorGrp)
        else:
            mc.warning('Anchor object [ {} ] does not exist.'.format(anchor)) 

        for jnt,blendJnt in zip(self.ikfkSystem.getJointList(), self.ikfkSystem.getBlendJointList()):
            mc.pointConstraint(blendJnt, jnt)
            mc.orientConstraint(blendJnt, jnt)

        #------------------------------------------------------------------------------------------
        #Setup attributes on the param node for the ikfk switch.
        #------------------------------------------------------------------------------------------
        # fk match attributes needed to the switch
        mc.addAttr(paramNode, ln="fkMatchTransforms", dt="string")
        mc.setAttr("{}.fkMatchTransforms".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(fkJointList[0], fkJointList[1], fkOffsetJnt), 
                type="string")

        mc.addAttr(paramNode, ln="fkControls", dt="string")
        mc.setAttr("{}.fkControls".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(*self._fkControls), 
                type="string")

        # ik match attributes needed for the switch
        mc.addAttr(paramNode, ln="ikMatchTransforms", dt="string")
        mc.setAttr("{}.ikMatchTransforms".format(paramNode), 
                '["{0}","{1}","{2}"]'.format(*ikJointList), 
                type="string")
        mc.addAttr(paramNode, ln="ikControls", dt="string")
        mc.setAttr("{}.ikControls".format(paramNode), 
                '["{0}","{1}"]'.format(*self._ikControls), 
                type="string")

        # command to be called when switch is being used.
        mc.addAttr(paramNode, ln="switchCommand", dt="string")
        mc.setAttr("{}.switchCommand".format(paramNode), "rigrepo.parts.limb.Limb.switch", 
                    type="string")

    def postBuild(self):
        '''
        '''
        #turn of the visibility of the ikfk system
        mc.setAttr("{0}.v".format(self.ikfkSystem.getGroup()), 0)

        # NO TWIST JOINT
        side = self.getAttributeByName("side").getValue()
        nameSplit = self.jointList[0].split('_{}_'.format(side))
        noTwist = '{}NoTwist_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        target = self.jointList[1]
        aimVector = (1, 0, 0)
        if side is 'r':
            aimVector = (-1, 0, 0)
        if mc.objExists(noTwist):
            mc.aimConstraint(target, noTwist, mo=1, weight=1, aimVector=aimVector, upVector=(0, 0, 0), worldUpType='none')
        else:
            print('noTwist not found', noTwist)
        # TWIST JOINT
        joint = self.jointList[-1]
        nameSplit = joint.split('_{}_'.format(side))
        twistJoint = '{}Twist_{}_{}'.format(nameSplit[0], side, nameSplit[1])
        if mc.objExists(twistJoint):
            deompose = rigrepo.libs.transform.decomposeRotation(joint)
            mc.connectAttr(joint + '.decomposeTwist', twistJoint + '.rx', f=1)
        else:
            print('No twist joint found', noTwist)

    @staticmethod
    def switch(paramNode, value):
        '''
        This will handle the switching between the fk and ik control
        :param paramNode: Param node that is holding the data for the switch
        :type paramNode: str

        :param value: The value of the switch bewteen ik and fk
        :type value: int
        '''
        if not mc.objExists(paramNode):
            raise RuntimeError("{} doesn't exist in the current Maya session".format(paramNode))
        # if we're in ik modes, we will match fk to the ik position and switch it to fk
        if value == 0:
            fkControls = eval(mc.getAttr("{}.fkControls".format(paramNode)))
            ikMatchTransforms = eval(mc.getAttr("{}.ikMatchTransforms".format(paramNode)))
            rigrepo.libs.ikfk.IKFKLimb.fkMatchIk(fkControls, ikMatchTransforms)
            mc.setAttr("{}.ikfk".format(paramNode), 1)
        elif value == 1:
            ikControls = eval(mc.getAttr("{}.ikControls".format(paramNode)))
            fkMatchTransforms = eval(mc.getAttr("{}.fkMatchTransforms".format(paramNode)))
            rigrepo.libs.ikfk.IKFKLimb.ikMatchFk(fkMatchTransforms, ikControls[1], ikControls[0])
            mc.setAttr("{}.ikfk".format(paramNode), 0)
"""