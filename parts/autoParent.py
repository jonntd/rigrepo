'''
This is the AutoParent base class.
'''

import maya.cmds as mc
import rigrepo.parts.part as part
import rigrepo.libs.ikfk
import rigrepo.libs.control
import rigrepo.libs.attribute
import rigrepo.libs.common as common
import rigrepo.libs.psd as psd
import rigrepo.libs.joint

class AutoParent(part.Part):
    '''
    Builds a system so the child can affect the parent's movement
    '''
    def __init__(self, name, parentControl, inputControls, ikJointList=None,
                 fkJointList=None, ikBlendAttr=None, autoBlendAttr=None, anchor=None, side='l'):
        '''
        This is the constructor.
        '''
        super(AutoParent, self).__init__(name, parentControl)
        self.addAttribute("parentControl", parentControl, attrType=str)
        self.addAttribute("inputControls", inputControls, attrType=list)
        self.addAttribute("anchor", anchor, attrType=str)
        self.addAttribute("ikBlendAttr", ikBlendAttr, attrType=str)
        self.addAttribute("autoBlendAttr", autoBlendAttr, attrType=str)
        self.addAttribute("side", side, attrType=str)
        self.addAttribute("ikJointList", ikJointList,
                            attrType=list)

    def build(self):
        parentControl = self.getAttributeByName('parentControl').getValue()
        inputControls = self.getAttributeByName('inputControls').getValue()
        anchor = self.getAttributeByName('anchor').getValue()
        ikBlendAttr = self.getAttributeByName('ikBlendAttr').getValue()
        autoBlendAttr = self.getAttributeByName('autoBlendAttr').getValue()
        side = self.getAttributeByName("side").getValue()
        ikJointList = self.getAttributeByName("ikJointList").getValue()

        names = ['start', 'mid', 'end']
        names = [parentControl+'_auto_'+x for x in names]
        group = self.name
        mc.hide(group)
        mc.parent(group, anchor)
        if not ikJointList:
            return
        self.jointList = rigrepo.libs.joint.duplicateChain(ikJointList, names=names, parent=group)
        for j in self.jointList:
            mc.setAttr(j+'.rotateOrder', 0)
        autoIkHandle = mc.ikHandle(sj=self.jointList[0],  ee=self.jointList[-1],
                                  sol="ikRPsolver", name=parentControl+'_auto_ikHandle')[0]
        mc.hide(autoIkHandle)
        mc.parent(autoIkHandle, group)

        # Combine the rotation of the input controls
        addRotationMatrix = mc.createNode('multMatrix', n=parentControl+'_addRotation_multMatrix')
        # Matrix multiplication is done in reverse order of hierarchy
        inputControls.reverse()
        for inputControl, i in zip(inputControls, xrange(len(inputControls))):
            mc.connectAttr(inputControl+'.matrix', addRotationMatrix+'.matrixIn[{}]'.format(i))
        addRotation = mc.createNode('decomposeMatrix', n=parentControl+'_addRotation_dcmpMatrix')
        mc.connectAttr(addRotationMatrix+'.matrixSum', addRotation+'.inputMatrix')

        # Drive the auto ik upper joint with driven keys so it sill works with ik blend
        fk = addRotation+'.outputRotate'
        auto = self.jointList[0]
        for axis in ['X', 'Y', 'Z']:
            mc.setDrivenKeyframe(auto+'.rotate'+axis, currentDriver=fk+axis,
                                 dv=-180, itt="spline", ott= "spline", value=-180)
            mc.setDrivenKeyframe(auto+'.rotate'+axis, currentDriver=fk+axis,
                                 dv=180, itt="spline", ott="spline", value=180)
            key = mc.listConnections(auto+'.rotate'+axis, s=1, d=0)[0]
            mc.setAttr(key+'.preInfinity', 1)
            mc.setAttr(key+'.postInfinity', 1)

        inputIkHandle = mc.listConnections(ikJointList[0]+'.message', type='ikHandle')
        # Copy input ik connections
        if inputIkHandle:
            inputIkHandle = inputIkHandle[0]
            par = mc.listRelatives(inputIkHandle, p=1)
            if par:
                mc.parent(autoIkHandle, par[0])
            mc.connectAttr(ikBlendAttr, autoIkHandle+'.ikBlend')
            # Pole vector constraint
            pvCon = mc.listConnections(inputIkHandle+'.poleVectorX')
            if pvCon:
                pvTarget = mc.poleVectorConstraint(pvCon[0], q=1, targetList=1)[0]
                mc.poleVectorConstraint(pvTarget, autoIkHandle)

        # Add blend attributes
        mc.addAttr(parentControl, ln=autoBlendAttr, at='double', min=0, max=1, dv=1, k=1)

        # Joint for inserting auto rotation into the parent controls hierarchy
        driver = self.jointList[0]

        # Make a joint the is only the swing of the auto joint
        # Aim constrain it to the middle auto joint
        autoJointSwing = mc.duplicate(driver, n=driver+'_swing', po=1)[0]
        vector = [1, 0, 0]
        if side == 'r':
            vector = [-1, 0, 0]
        mc.aimConstraint(self.jointList[1], autoJointSwing,
                         weight=1, aimVector=vector,
                         worldUpType="none", mo=1,
                         upVector=[0, 0, 0])

        # Pair blend - blends the auto rotation
        pb = mc.createNode('pairBlend')
        mc.setAttr(pb+'.rotInterpolation', 1)
        mc.connectAttr(autoJointSwing+'.rotate', pb+'.inRotate2')

        # Connect rotation
        parentControlPar = mc.listRelatives(parentControl, p=1)[0]
        # Go up one more to the nul, because the ort is getting inverted
        parentControlPar = mc.listRelatives(parentControlPar, p=1)[0]
        mc.connectAttr(pb+'.outRotateX', parentControlPar+'.rotateAxisX')
        mc.connectAttr(pb+'.outRotateY', parentControlPar+'.rotateAxisY')
        mc.connectAttr(pb+'.outRotateZ', parentControlPar+'.rotateAxisZ')
        mc.setAttr(parentControlPar+'.rotateAxisX', k=1)
        mc.setAttr(parentControlPar+'.rotateAxisY', k=1)
        mc.setAttr(parentControlPar+'.rotateAxisZ', k=1)

        # Make a pose interpolator to control the strength of the auto behaviour in different poses
        poseInterp = psd.addPoseInterp(parentControl+'_auto_poseInterpolator', driver=driver,
                                       createNeutralPose=0)
        mc.setAttr(poseInterp+'.interpolation', 1)
        mc.setAttr(poseInterp+'.outputSmoothing', 1)
        mc.setAttr(poseInterp+'.regularization', 100)

        # Add upper fk as the pose control
        poseControl = inputControls[0]
        psd.addPoseControl(poseInterp, poseControl+'.rotate')

        # Create a mesh plane to hold the blendShape the poseInterpolators connect to
        psdNumericGeo = 'numericPSD_geo'
        psdNumericBS = 'numeric_psd'
        if not mc.objExists(psdNumericGeo):
            psdNumericGeo = mc.polyPlane(n=psdNumericGeo, sx=1, sy=1, ch=0)[0]
            mc.hide(psdNumericGeo)
        if not mc.objExists(psdNumericBS):
            mc.blendShape(psdNumericGeo, n=psdNumericBS)

        # Ensure the neutral pose comes first
        neutralPose = 'neutral'
        psd.addPose(poseInterp, neutralPose)

        # poses
        poseDict = {
            'neutral':           ('r',  (0,    0,    0),  0),
            'down_90':           ('r',  (0,   90,    0),  0),
            'up_90':             ('r',  (0,  -90,    0),  2),
            'front_90':          ('r',  (0,    0,  -90),  1),
            'front_179':         ('r',  (0,    0, -140),  2),
            'back_90':           ('r',  (0,    0,   90),  1),
            'back_179':          ('r',  (0,    0,  140),  2),
            'back_90__down_35':  ('r',  (0,   35,   90),  0),
            'front90__down_35':  ('r',  (0,   35,  -90),  0)
        }

        # Used to combine psd output into one numeric value
        add = mc.createNode('plusMinusAverage', n=parentControl+'_poseInterp_add')

        for pose in poseDict:
            poseName = parentControl+'_'+pose
            if pose == 'neutral':
                poseName = pose
            attr = poseDict[pose][0]
            value = poseDict[pose][1]
            drivenKeyValue = poseDict[pose][2]

            # Add pose
            mc.setAttr(poseControl+'.'+attr, *value)
            poseIndex = psd.addPose(poseInterp, poseName)
            if pose != 'neutral':
                psd.addShape(poseInterp, poseName, psdNumericBS)
            mc.setAttr(poseControl+'.'+attr, *(0, 0, 0))

            # Create driven key
            driver = poseInterp+'.output[{}]'.format(poseIndex)
            driven = add+'.input1D[{}]'.format(poseIndex)
            mc.setDrivenKeyframe(driven, cd=driver, value=0, dv=0, itt="linear", ott="linear")
            mc.setDrivenKeyframe(driven, cd=driver, value=drivenKeyValue, dv=1, itt="linear", ott="linear")
            node = mc.listConnections(driven)[0]
            mc.rename(node, '{}_driven_key'.format(poseName))

        # Connect blend attr
        mulDive = mc.createNode('multiplyDivide', n=parentControl+'_blend_mul')
        mc.setDrivenKeyframe(mulDive+'.input1X', cd=parentControl+'.'+autoBlendAttr, value=0, dv=0, itt="linear", ott="linear")
        mc.setDrivenKeyframe(mulDive+'.input1X', cd=parentControl+'.'+autoBlendAttr, value=.3, dv=1, itt="linear", ott="linear")

        mc.connectAttr(add+'.output1D', mulDive+'.input2X')
        mc.connectAttr(mulDive+'.outputX', pb+'.weight')

        # info attribute that displays the current auto contribution
        autoInfoAttr = autoBlendAttr+'AmountInfo'
        mc.addAttr(parentControl, ln=autoInfoAttr, at='double', min=0, max=1)
        mc.setAttr(parentControl+'.'+autoInfoAttr, cb=1)
        mc.connectAttr(mulDive+'.outputX', parentControl+'.'+autoInfoAttr)

        # Display attrs on poseControl also
        mc.addAttr(poseControl, ln=autoBlendAttr, proxy=parentControl+'.'+autoBlendAttr)
        mc.addAttr(poseControl, ln=autoInfoAttr, proxy=parentControl+'.'+autoInfoAttr)

