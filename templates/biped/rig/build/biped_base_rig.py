'''
'''
import maya.cmds as mc
import rigrepo.templates.archetype.rig.build.archetype_base_rig as archetype_base_rig
import pubs.pNode
from rigrepo.libs.fileIO import joinPath 
import rigrepo.nodes.loadFileNode
import rigrepo.nodes.newSceneNode
import rigrepo.nodes.importDataNode
import rigrepo.nodes.exportDataNode
import rigrepo.nodes.yankClusterNode
import rigrepo.nodes.utilNodes 
import rigrepo.nodes.addSpaceNode
import rigrepo.nodes.wiresToSkinClusterNode

# body parts import
import rigrepo.parts.arm
import rigrepo.parts.leg
import rigrepo.parts.spine 
import rigrepo.parts.neck
import rigrepo.parts.hand
import rigrepo.parts.foot

# face parts import
import rigrepo.parts.mouth
import rigrepo.parts.blink
import rigrepo.parts.face
import rigrepo.parts.brow
import rigrepo.parts.tongue
import rigrepo.parts.lookAt

import rigrepo.nodes.controlDefaultsNode as controlDefaultsNode
import os

class BipedBaseRig(archetype_base_rig.ArchetypeBaseRig):
    def __init__(self,name, variant='base'):
        '''
        This is the constructor for the biped template. Here is where you will put nodes onto 
        the graph. 

        :param name: Name of the element you're using this for
        :type name: str

        :param variant: Name of the variant this template is being used for.
        :type variant: str
        '''
        
        super(BipedBaseRig, self).__init__(name, variant)

        animRigNode = self.getNodeByName("animRig")

        buildPath = joinPath(os.path.dirname(__file__), self.variant)

        
        # Parts
        #-------------------------------------------------------------------------------------------
        # BODY
        #-------------------------------------------------------------------------------------------
        # center
        #
        # Spine
        spine = rigrepo.parts.spine.Spine(name='spine', jointList="mc.ls('spine_*_bind')", scaleFactor=0.5)

        # Neck
        neck = rigrepo.parts.neck.Neck(name='neck', 
                                        jointList="mc.ls('neck_?_bind')",
                                        scaleFactor=.4,
                                        anchor="chest_top")

        neckAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('addSpaces', attrNode="neck",
            constraintNode="neck_ort", parentNode='chest_top', targetList=['rig'], 
        nameList=["world"], constraintType='orient')

        headAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('addHeadSpaces', attrNode="head",
            constraintNode="head_nul", parentNode='neck', targetList=['rig'], 
        nameList=["world"], constraintType='orient', defaultTargetIndex=0)
        
        neck.addChildren([neckAddSpaceNode,headAddSpaceNode])

        # Left Arm
        l_arm = rigrepo.parts.arm.Arm("l_arm", 
                                    ['clavicle_l_bind', 
                                        'shoulder_l_bind', 
                                        'elbow_l_bind', 
                                        'wrist_l_bind'], 
                                    anchor='chest_top')
        l_arm.getAttributeByName("fkControls").setValue(["shoulder_fk_l","elbow_fk_l", "wrist_fk_l"]) 
        l_arm.getAttributeByName("ikControls").setValue(["arm_pv_l","arm_ik_l"])
        l_arm.getAttributeByName("paramNode").setValue("arm_L")
        l_arm.getAttributeByName("clavicleCtrl").setValue("clavicle_l")

        leftArmAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('addSpaces', attrNode="shoulderSwing_l",
            constraintNode="shoulderSwing_l_ort", parentNode='shoulderSwing_l_nul', targetList=['rig'],
            nameList=["world"], constraintType='orient', defaultTargetIndex=1)


        leftArmPvAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('pvAddSpaces', attrNode="arm_pv_l",
            constraintNode="arm_pv_l_nul", parentNode='l_arm', targetList=['chest_bind', 'wrist_fk_l_offset_pv'],
        nameList=["chest", "hand"], constraintType='parent')

        leftArmIkAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('ikAddSpaces', attrNode="arm_L",
            constraintNode="arm_ik_l_ort", parentNode='l_arm', targetList=['chest_bind', 'skull_bind','hip_swivel','hips_bind'], 
        nameList=["chest","head","hips","root"], constraintType='parent')

        l_hand = rigrepo.parts.hand.Hand("l_hand",
                                        ['ring_001_l_bind', 
                                        'middle_001_l_bind', 
                                        'index_001_l_bind', 
                                        'pinkyCup_l_bind', 
                                        'thumbCup_l_bind'])
        # Auto clavicle
        side = 'l'
        l_autoClav = rigrepo.parts.autoParent.AutoParent(side+'_autoClav',
                                                         parentControl='clavicle_'+side,
                                                         inputControls=['shoulderSwing_'+side,
                                                                        'shoulder_fk_'+side],
                                                         ikJointList=['shoulder_'+side+'_bind_ik',
                                                                      'elbow_'+side+'_bind_ik',
                                                                      'wrist_'+side+'_bind_ik'],
                                                         autoBlendAttr='autoClav',
                                                         side=side,
                                                         ikBlendAttr=side+'_arm_rvr.output.outputX',
                                                         anchor=side+'_arm_anchor_grp')

        # Orient arm to world for anim pose
        #
        orientToWorldNode = rigrepo.nodes.commandNode.CommandNode('worldOrient')
        world_ctrls  = [l_arm.getAttributeByName('swingCtrl').getValue()]
        world_ctrls += l_arm.getAttributeByName('fkControls').getValue()
        orientToWorldNodeCmd = 'ctrls = ' + str(world_ctrls)
        orientToWorldNodeCmdMain = '''
import maya.cmds as mc

for ctrl in ctrls:
    matrix = mc.xform(ctrl, q=1, ws=1, matrix=1)
    nul = ctrl+'_nul'
    if mc.objExists(nul):
        mc.setAttr(nul+'.r', 0, 0, 0)
        mc.xform(ctrl, ws=1, matrix=matrix)
        
        # Because of some insane refresh problem this is locking and unlocking is here.
        mc.setAttr(ctrl+'.r', l=1)
        mc.setAttr(ctrl+'.r', l=0)
        '''
        orientToWorldNodeCmd += orientToWorldNodeCmdMain

        orientToWorldNode.getAttributeByName('command').setValue(orientToWorldNodeCmd)

        # AutoClav World Orient
        #    Hook the world space of the swing into the driver for the
        #    auto clav. This is so the auto clav fires when the spine is rotated
        #    and the swing is in world space.
        #
        l_autoClavWorldDriver = rigrepo.nodes.commandNode.CommandNode('l_autoClavWorldSpaceDriver')

        side = "side = 'l' \n"
        autoClavWorldDriverCmd = '''
import maya.cmds as mc

orient = 'shoulderSwing_'+side+'_ortSpaces_world'
parent = 'chest_top'
attr = 'shoulderSwing_'+side+'.space'
add_matrix = 'clavicle_'+side+'_addRotation_multMatrix'

space_grp = mc.createNode('transform', n=orient+'_autoClav_nul', p=orient)
space = mc.createNode('transform', n=orient+'_autoClav', p=space_grp)
mc.parent(space_grp, parent)
con = mc.orientConstraint('rig', space, mo=1)[0]
mc.connectAttr(attr, con+'.rigW0')
mc.connectAttr(space+'.matrix', add_matrix+'.matrixIn[3]')
        '''
        l_autoClavWorldDriver.getAttributeByName('command').setValue(side+autoClavWorldDriverCmd)

        # Left arm nodes
        l_arm.addChildren([orientToWorldNode, l_autoClav, leftArmAddSpaceNode,
                           l_autoClavWorldDriver, leftArmPvAddSpaceNode,
                           leftArmIkAddSpaceNode, l_hand])

        # Right arm
        #
        r_arm = rigrepo.parts.arm.Arm("r_arm",
                                    ['clavicle_r_bind', 
                                     'shoulder_r_bind',
                                     'elbow_r_bind',
                                     'wrist_r_bind'],
                                    anchor='chest_top', 
                                    side='r')

        r_arm.getAttributeByName("fkControls").setValue(["shoulder_fk_r","elbow_fk_r", "wrist_fk_r"]) 
        r_arm.getAttributeByName("ikControls").setValue(["arm_pv_r","arm_ik_r"])
        r_arm.getAttributeByName("paramNode").setValue("arm_R")
        r_arm.getAttributeByName("clavicleCtrl").setValue("clavicle_r")
        
        rightArmAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('addSpaces', attrNode="shoulderSwing_r",
            constraintNode="shoulderSwing_r_ort", parentNode='shoulderSwing_r_nul', targetList=['rig'],
        nameList=["world"], constraintType='orient', defaultTargetIndex=1)

        rightArmPvAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('pvAddSpaces', attrNode="arm_pv_r",
            constraintNode="arm_pv_r_nul", parentNode='r_arm', targetList=['chest_bind', 'wrist_fk_r_offset_pv'],
        nameList=["chest", "hand"], constraintType='parent')

        rightArmIkAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('ikAddSpaces', attrNode="arm_R",
            constraintNode="arm_ik_r_ort", parentNode='r_arm', targetList=['chest_bind', 'skull_bind','hip_swivel','hips_bind'], 
        nameList=["chest","head","hips","root"], constraintType='parent')

        r_hand = rigrepo.parts.hand.Hand("r_hand",
                                        ['ring_001_r_bind', 
                                            'middle_001_r_bind', 
                                            'index_001_r_bind', 
                                            'pinkyCup_r_bind', 
                                            'thumbCup_r_bind'], 
                                        'wrist_r_bind')

        # Auto clavicle
        side = 'r'

        r_autoClav = rigrepo.parts.autoParent.AutoParent(side+'_autoClav',
                                                         parentControl='clavicle_'+side,
                                                         inputControls=['shoulderSwing_'+side,
                                                                        'shoulder_fk_'+side],
                                                         ikJointList=['shoulder_'+side+'_bind_ik',
                                                                      'elbow_'+side+'_bind_ik',
                                                                      'wrist_'+side+'_bind_ik'],
                                                         autoBlendAttr='autoClav',
                                                         side=side,
                                                         ikBlendAttr=side+'_arm_rvr.output.outputX',
                                                         anchor=side+'_arm_anchor_grp',
                                                         paramNode='arm_R')

        # Orient arm to world for anim pose
        #
        orientToWorldNode = rigrepo.nodes.commandNode.CommandNode('worldOrient')
        world_ctrls = [r_arm.getAttributeByName('swingCtrl').getValue()]
        world_ctrls += r_arm.getAttributeByName('fkControls').getValue()
        orientToWorldNodeCmd = 'ctrls = ' + str(world_ctrls)
        orientToWorldNodeCmd += orientToWorldNodeCmdMain
        orientToWorldNode.getAttributeByName('command').setValue(orientToWorldNodeCmd)

        # AutoClav World Orient
        #    Hook the world space of the swing into the driver for the
        #    auto clav. This is so the auto clav fires when the spine is rotated
        #    and the swing is in world space.
        #
        r_autoClavWorldDriver = rigrepo.nodes.commandNode.CommandNode('r_autoClavWorldSpaceDriver')
        side = "side = 'r' \n"
        r_autoClavWorldDriver.getAttributeByName('command').setValue(side+autoClavWorldDriverCmd)

        # Right arm nodes
        r_arm.addChildren([orientToWorldNode, r_autoClav, rightArmAddSpaceNode,
                           r_autoClavWorldDriver, rightArmPvAddSpaceNode,
                           rightArmIkAddSpaceNode,r_hand])

        # Leg
        l_leg = rigrepo.parts.leg.Leg("l_leg",
                                ['pelvis_l_bind', 'thigh_l_bind', 'knee_l_bind', 'ankle_l_bind'], 
                                spine.getHipSwivelCtrl)

        l_leg.getAttributeByName("side").setValue("l")
        l_leg.getAttributeByName("fkControls").setValue(["thigh_fk_l","knee_fk_l", "ankle_fk_l"])
        l_leg.getAttributeByName("ikControls").setValue(["leg_pv_l","leg_ik_l"])
        l_leg.getAttributeByName("paramNode").setValue("leg_L")
        l_leg.getAttributeByName("clavicleCtrl").setValue("pelvis_l")

        l_foot = rigrepo.parts.foot.Foot("l_foot", ['ankle_l_bind', 'ball_l_bind', 'toe_l_bind'], 
                                        'ankle_l_bind_ik_hdl',
                                        fkAnchor='ankle_fk_gimbal_l', 
                                        ikAnchor='leg_ik_gimbal_l', 
                                        anklePivot='ankle_l_pivot', 
                                        ankleStretchTarget="ankle_fk_l_offset",
                                        ikfkGroup='l_leg_ikfk_grp',
                                        paramNodeName='leg_L')
        leftLegAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('pvAddSpaces', attrNode="leg_pv_l",
            constraintNode="leg_pv_l_nul", parentNode='rig', targetList=['pelvis_l','ankle_fk_l_offset_pv'], 
            nameList=["pelvis","foot"], constraintType='parent', defaultTargetIndex=2)

        # add foot to the leg node
        l_leg.addChildren([l_foot,leftLegAddSpaceNode])

        r_leg = rigrepo.parts.leg.Leg("r_leg",
                                ['pelvis_r_bind', 'thigh_r_bind', 'knee_r_bind', 'ankle_r_bind'], 
                                spine.getHipSwivelCtrl,
                                side="r")

        r_leg.getAttributeByName("side").setValue("r")
        r_leg.getAttributeByName("fkControls").setValue(["thigh_fk_r","knee_fk_r", "ankle_fk_r"]) 
        r_leg.getAttributeByName("ikControls").setValue(["leg_pv_r","leg_ik_r"])
        r_leg.getAttributeByName("paramNode").setValue("leg_R")
        r_leg.getAttributeByName("clavicleCtrl").setValue("pelvis_r")

        r_foot = rigrepo.parts.foot.Foot("r_foot", ['ankle_r_bind', 'ball_r_bind', 'toe_r_bind'], 
                                        'ankle_r_bind_ik_hdl',
                                        fkAnchor='ankle_fk_gimbal_r', 
                                        ikAnchor='leg_ik_gimbal_r', 
                                        anklePivot='ankle_r_pivot',
                                        ankleStretchTarget="ankle_fk_r_offset",
                                        ikfkGroup='r_leg_ikfk_grp',
                                        paramNodeName='leg_R')

        rightLegAddSpaceNode = rigrepo.nodes.addSpaceNode.AddSpaceNode('pvAddSpaces',attrNode="leg_pv_r",
            constraintNode="leg_pv_r_nul", parentNode='rig', targetList=['pelvis_r','ankle_fk_r_offset_pv'], 
            nameList=["pelvis","foot"], constraintType='parent', defaultTargetIndex=2)


        # add foot to the leg node
        r_leg.addChildren([r_foot,rightLegAddSpaceNode])

        # Breathing
        breathing = rigrepo.nodes.commandNode.CommandNode('breathing')
        breathingCMD = """
import maya.cmds as mc
import rigrepo.libs.control  
node = 'chest'
if mc.objExists(node):
    # Divider attribute
    if not mc.objExists(node+'.breathing'):
        mc.addAttr(node, ln="breathing", nn="---------", at="enum", keyable=False, enumName="Breathing")
        mc.setAttr(node+'.breathing', l=1, cb=1)
    # Chest 
    attr = 'Chest'
    if not mc.objExists(node+'.'+attr):
        driven = 'skin_psd.breathing_chest'
        driver = node+'.'+attr
        if mc.objExists(driven):
            mc.addAttr(node, ln=attr, at='double', dv=0, k=1) 
            mc.setDrivenKeyframe(driven, cd=driver, value=0, dv=0, itt="spline", ott="spline")
            mc.setDrivenKeyframe(driven, cd=driver, value=1, dv=10, itt="spline", ott="spline")
            mc.setInfinity(driven, pri='linear', poi='linear')
        else:
            print('missing skin_psd.breathing_chest blendshape target')
            
    # Belly 
    attr = 'Belly'
    if not mc.objExists(node+'.'+attr):
        driven = 'skin_psd.breathing_belly'
        driver = node+'.'+attr
        if mc.objExists(driven):
            mc.addAttr(node, ln=attr, at='double', dv=0, k=1) 
            mc.setDrivenKeyframe(driven, cd=driver, value=0, dv=0, itt="spline", ott="spline")
            mc.setDrivenKeyframe(driven, cd=driver, value=1, dv=10, itt="spline", ott="spline")
            mc.setInfinity(driven, pri='linear', poi='linear')
        else:
            print('missing skin_psd.breathing_belly blendshape target')
        
    # Shoulders 
    attr = 'Shoulders'
    if not mc.objExists(node+'.'+attr):
        mc.addAttr(node, ln=attr, at='double', dv=0, k=1) 
        driver = node+'.'+attr
        sideMul = 1.0
        for side in ['l', 'r']:
            if side == 'r':
                sideMul = -1.0
                
            driven = 'shoulderSwing_'+side+'_mirror_ort.tx'
            mc.setDrivenKeyframe(driven, cd=driver, value=0, dv=0, itt="spline", ott="spline")
            mc.setDrivenKeyframe(driven, cd=driver, value=.2*sideMul, dv=10, itt="spline", ott="spline")
            mc.setInfinity(driven, pri='linear', poi='linear')
            
            driven = 'shoulderSwing_'+side+'_mirror_ort.tz'
            mc.setDrivenKeyframe(driven, cd=driver, value=0, dv=0, itt="spline", ott="spline")
            mc.setDrivenKeyframe(driven, cd=driver, value=.5*sideMul, dv=10, itt="spline", ott="spline")
            mc.setInfinity(driven, pri='linear', poi='linear')
        
        """
        breathing.getAttributeByName('command').setValue(breathingCMD)

        #-------------------------------------------------------------------------------------------
        # FACE
        #-------------------------------------------------------------------------------------------
        faceParts = rigrepo.parts.face.Face("face_parts")
        earClusterNode = rigrepo.nodes.utilNodes.ClusterControlNode("ears")
        earClusterNode.getAttributeByName("nameList").setValue("['ear_l', 'ear_r']")
        earClusterNode.getAttributeByName("geometry").setValue("body_geo")
        earClusterNode.getAttributeByName("parent").setValue("face_upper")
        tongueNode = rigrepo.parts.tongue.Tongue(name='tongue', 
                                        jointList="mc.ls('tongue_?_bind')", 
                                        anchor="jaw")
        faceParts.addChildren([earClusterNode])
        l_blink = rigrepo.parts.blink.BlinkNew("l_blink", anchor="face_upper")
        r_blink = rigrepo.parts.blink.BlinkNew("r_blink",side="r", anchor="face_upper")
        r_blink.getAttributeByName("side").setValue("r")
        lookAtNode = rigrepo.parts.lookAt.LookAt("lookAt")
        mouth = rigrepo.parts.mouth.Mouth("mouth", lipMainCurve='lip_main_curve')
        mouth.getAttributeByName("orientFile").setValue(self.resolveDataFilePath('control_orients.data', self.variant))
        mouthBindGeometry = rigrepo.nodes.commandNode.CommandNode('bindGeometry')
        mouthBindGeometryCmd = '''
import maya.cmds as mc
import rigrepo.libs.cluster
for curve in ["lip_main_curve", "lip_curve"]:
    wireDeformer = "{}_wire".format(curve)
    if mc.objExists(wireDeformer):
        mc.deformer(wireDeformer, e=1, g='body_geo')
        mc.rename(wireDeformer, curve.replace("_curve", "_wire"))
    else:
        wireDeformer = mc.wire("body_geo", gw=False, en=1.00, ce=0.00, li=0.00, 
                        w=curve, name=curve.replace("_curve", "_wire"))[0]
        # set the default values for the wire deformer
        mc.setAttr("{}.rotation".format(wireDeformer), 0)
        mc.setAttr("{}.dropoffDistance[0]".format(wireDeformer), 100)

bindJointList = list(set(mc.ls("lip_*_baseCurve_jnt")).difference(set(mc.ls("lip_main_*_baseCurve_jnt"))))
skinCluster = mc.skinCluster(*bindJointList + ["lip_curveBaseWire"],
                                rui=False,
                                tsb=True,
                                name="lip_curveBaseWire_skinCluster")[0]

for jnt in bindJointList:
    index = [int(s) for s in jnt.split("_") if s.isdigit()][0]
    mc.skinPercent(skinCluster, "lip_curveBaseWire.cv[{}]".format(index), tv=["lip_{}_baseCurve_jnt".format(index), 1])

for mesh in mc.ls(["lip_main_bindmesh", "lip_bindmesh", "mouth_corner_bindmesh"]):
    if mc.objExists(mesh) and mc.objExists("mouthMain_cls_hdl"):
        mc.select(mesh, r=True)
        cls = mc.cluster(name="{}_mouthMain_cluster".format(mesh), wn=['mouthMain_cls_hdl','mouthMain_cls_hdl'],bs=1)[0]
        rigrepo.libs.cluster.localize(cls, 'mouthMain_auto', 'model')
'''
        mouthBindGeometry.getAttributeByName('command').setValue(mouthBindGeometryCmd)
        mouth.addChildren([mouthBindGeometry])
        controlsDefaults = controlDefaultsNode.ControlDefaultsNode("control_defaults",
                                armControls=["shoulderSwing_?", "*shoulder","*elbow","*wrist"],
                                armParams=["arm_?"])
        l_brow = rigrepo.parts.brow.Brow("l_brow", anchor="head_tip")
        r_brow = rigrepo.parts.brow.Brow("r_brow", side="r", anchor="head_tip")

        cheekClusterNode = rigrepo.nodes.utilNodes.ClusterControlNode("cheeks")
        cheekClusterNode.getAttributeByName("nameList").setValue("['cheekPuff_l', 'cheekPuff_r', 'cheek_l', 'cheek_r']")
        cheekClusterNode.getAttributeByName("geometry").setValue("body_geo")
        cheekClusterNode.getAttributeByName("parent").setValue("face_mid_driver")
        leftCheekLiftClusterNode = rigrepo.nodes.utilNodes.ClusterControlNode("l_cheekLift")
        leftCheekLiftClusterNode.getAttributeByName("nameList").setValue("['cheekLift_l']")
        leftCheekLiftClusterNode.getAttributeByName("geometry").setValue("body_geo")
        leftCheekLiftClusterNode.getAttributeByName("parent").setValue("lidLower_l")
        leftCheekLiftClusterNode.getAttributeByName("displayHandle").setValue(False)

        rightCheekLiftClusterNode = rigrepo.nodes.utilNodes.ClusterControlNode("r_cheekLift")
        rightCheekLiftClusterNode.getAttributeByName("nameList").setValue("['cheekLift_r']")
        rightCheekLiftClusterNode.getAttributeByName("geometry").setValue("body_geo")
        rightCheekLiftClusterNode.getAttributeByName("parent").setValue("lidLower_r")
        rightCheekLiftClusterNode.getAttributeByName("displayHandle").setValue(False)
        mouthCornerDistanceNode = rigrepo.nodes.commandNode.CommandNode('mouthCornerDistance')
        mouthCornerDistanceNodeCmd = '''
import maya.cmds as mc
dkeys = []
distanceLocs = []
distanceNodes = []
for side in ["l","r"]:
    distanceLoc = mc.createNode("transform", n="distance_loc_{}".format(side))
    distanceLocs.append(distanceLoc)
    mc.xform(distanceLoc, ws=True, matrix=mc.xform("eye_{}_bind".format(side), q=True, ws=True, matrix=True))
    mc.parent(distanceLoc, "face_upper")
    mouthCornerDCM = mc.createNode("decomposeMatrix", name="mouth_corner_{}_decomposeMatrix".format(side))
    distanceLocDCM = mc.createNode("decomposeMatrix", name="distance_loc_{}_decomposeMatrix".format(side))
    
    mc.connectAttr("mouth_corner_{}.worldMatrix[0]".format(side), "{}.inputMatrix".format(mouthCornerDCM))
    mc.connectAttr("distance_loc_{}.worldMatrix[0]".format(side), "{}.inputMatrix".format(distanceLocDCM))
    
    distanceNode = mc.createNode("distanceBetween", n="mouth_corner_{}_distance".format(side))
    distanceNodes.append(distanceNode)
    mc.connectAttr("{}.outputTranslate".format(mouthCornerDCM), "{}.point1".format(distanceNode), f=True)
    mc.connectAttr("{}.outputTranslate".format(distanceLocDCM), "{}.point2".format(distanceNode), f=True)
        

    currentDistance = mc.getAttr("{}.distance".format(distanceNode))        
    for axis in ['x', 'y', 'z']:
        #mc.setDrivenKeyframe("cheekPuff_{}_def_auto.s{}".format(side, axis), 
        #                            cd="{}.distance".format(distanceNode), v=1, dv=currentDistance)
        #mc.setDrivenKeyframe("cheekPuff_{}_def_auto.s{}".format(side, axis), 
        #                            cd="{}.distance".format(distanceNode), v=2, dv=currentDistance-2)
                                    
                                    
        if axis == "y":
            mc.setDrivenKeyframe("cheek_{}_def_auto.t{}".format(side, axis), 
                                        cd="{}.distance".format(distanceNode), v=0, dv=currentDistance)
            mc.setDrivenKeyframe("cheek_{}_def_auto.t{}".format(side, axis), 
                                        cd="{}.distance".format(distanceNode), v=2, dv=currentDistance-2)

    # lid lower rotation
    mc.setDrivenKeyframe("lidLower_{}_def_auto.rx".format(side), 
                                    cd="{}.distance".format(distanceNode), v=0, dv=currentDistance)
    mc.setDrivenKeyframe("lidLower_{}_def_auto.rx".format(side), 
                                    cd="{}.distance".format(distanceNode), v=6, dv=currentDistance-2)

    if mc.objExists("cheekLift_{}_def_auto".format(side)):
        mc.setDrivenKeyframe("cheekLift_{}_def_auto.rx".format(side), 
                                        cd="{}.distance".format(distanceNode), v=0, dv=currentDistance)
        mc.setDrivenKeyframe("cheekLift_{}_def_auto.rx".format(side), 
                                        cd="{}.distance".format(distanceNode), v=6, dv=currentDistance-2)

        mc.addAttr("lidLower_{}".format(side), ln="cheekLift", at="double", keyable=True)
        mc.setDrivenKeyframe("cheekLift_{}.rx".format(side), 
                                        cd="lidLower_{}.cheekLift".format(side), v=0, dv=0)
        mc.setDrivenKeyframe("cheekLift_{}.rx".format(side), 
                                        cd="lidLower_{}.cheekLift".format(side), v=50, dv=10)
        mc.setDrivenKeyframe("cheekLift_{}.rx".format(side), 
                                        cd="lidLower_{}.cheekLift".format(side), v=-50, dv=-10)

        # turn off display handles for cheek lift
        mc.setAttr("cheekLift_{}_def_auto.displayHandle".format(side), 0)
        
# Rig Sets
# 
mouthDistSet = mc.sets(distanceLocs + distanceNodes, n='MouthDist')

# Driven keys 
for node in distanceNodes:
    current_dkeys = mc.listConnections(node+'.distance')
    dkeys += current_dkeys
dkeySet = mc.sets(dkeys, n='MouthDist_dkeys')
mc.sets(dkeySet, add=mouthDistSet)

mc.listConnections
if mc.objExists('Mouth'):
    mc.sets(mouthDistSet, add='Mouth')
                
'''
        mouthCornerDistanceNode.getAttributeByName('command').setValue(mouthCornerDistanceNodeCmd)
        cheekClusterNode.addChildren([leftCheekLiftClusterNode, rightCheekLiftClusterNode, mouthCornerDistanceNode])

        # create both face and body builds
        bodyBuildNode = pubs.pNode.PNode("body")
        faceBuildNode = pubs.pNode.PNode("face")

        browsNode = pubs.pNode.PNode("brows")
        browsNode.addChildren([l_brow, r_brow])

        eyesNode = pubs.pNode.PNode("eyes")
        eyesNode.addChildren([l_blink, r_blink, lookAtNode])

        
        # add nodes ass children of body
        bodyBuildNode.addChildren([spine, neck, l_arm, r_arm, l_leg, r_leg, breathing])
        faceBuildNode.addChildren([faceParts, tongueNode, browsNode, eyesNode, mouth, cheekClusterNode])

        bindMeshCurvePairs ="""[
('blinkUpper_l_curve', 'blinkUpper_l'),
('blinkUpper_r_curve', 'blinkUpper_r'),
('blinkLower_l_curve', 'blinkLower_l'),
('blinkLower_r_curve', 'blinkLower_r')
]"""

        # bindmeshes
        bindMeshesNode = self.getNodeByName('bindMeshes')
        lidBindMeshNode = rigrepo.nodes.buildBindMeshNode.BuildBindMeshNode('face',
                          curves = bindMeshCurvePairs)

        bindMeshesNode.addChild(lidBindMeshNode)

        # get the postBuild node
        postBuild = animRigNode.getChild('postBuild')

        # Control visibility switches
        controlVis = rigrepo.nodes.commandNode.CommandNode('controlVisSwitches')
        controlVisCmd = '''
import maya.cmds as mc
import rigrepo.libs.control 

# Control Visibility switches
controls = rigrepo.libs.control.getControls()
node = 'trs_shot'

if mc.objExists(node):
    # Divider attribute
    if not mc.objExists(node+'.CtrlVis'):
        mc.addAttr(node, ln="CtrlVis", nn="Control Vis", at="enum", keyable=False, enumName="--------")
        mc.setAttr(node+'.CtrlVis', l=1, cb=1)

    # All Controls
    attr = 'All'
    if not mc.objExists(node+'.'+attr):
        mc.addAttr(node, ln=attr, at='double', min=0, max=1, dv=1, k=0) 
        mc.setAttr(node+'.'+attr, cb=1) 
    mc.connectAttr(node+'.'+attr, 'rig.v', f=1)

    # Bendbow controls
    attr = 'BendBows'
    targets = list()
    for ctrl in controls:
        if 'bend' in ctrl:
            shapes = mc.listRelatives(ctrl, s=1)
            targets += shapes
            targets.append(ctrl)
    if not mc.objExists(node+'.'+attr):
        mc.addAttr(node, ln=attr, at='double', min=0, max=1, dv=1, k=0) 
        mc.setAttr(node+'.'+attr, cb=1) 
    for target in targets:
        if mc.objExists(target+'.displayHandle'):
            mc.connectAttr(node+'.'+attr, target+'.displayHandle', f=1)
        else:
            mc.connectAttr(node+'.'+attr, target+'.v', f=1)

    # Gimbal controls
    attr = 'Gimbals'
    targets = list()
    for ctrl in controls:
        if 'gimbal' in ctrl:
            shapes = mc.listRelatives(ctrl, s=1)
            targets += shapes
    if not mc.objExists(node+'.'+attr):
        mc.addAttr(node, ln=attr, at='double', min=0, max=1, dv=1, k=0) 
        mc.setAttr(node+'.'+attr, cb=1) 
    for target in targets:
        mc.connectAttr(node+'.'+attr, target+'.v', f=1)
            
    # Hips Movable Pivot
    attr = 'HipsMovablePivot'
    target = 'hipsPivotShape.v'
    if mc.objExists(target):
        if not mc.objExists(node+'.'+attr):
            mc.addAttr(node, ln=attr, at='double', min=0, max=1, dv=1, k=0) 
            mc.setAttr(node+'.'+attr, cb=1) 
        mc.connectAttr(node+'.'+attr, target, f=1)
'''
        controlVis.getAttributeByName('command').setValue(controlVisCmd)

        switchExpression = rigrepo.nodes.utilNodes.SwitchExpressionNode("SwitchExpression")
        postBuild.addChildren([controlVis, switchExpression])
        #switchExpression.disable()

        applyNode = animRigNode.getChild('apply')
        applyNode.addChild(controlsDefaults)

        applyDeformerNode = applyNode.getChild('deformers')
        bindmeshTransferSkinWtsNode = rigrepo.nodes.transferDeformer.TransferDeformerBindmesh('bindmeshAuto',
                                                            source="body_geo",
                                                            target=["lid*_bindmesh", "lip*_bindmesh", "mouth*_bindmesh"],
                                                            deformerTypes = ["skinCluster"],
                                                            surfaceAssociation="closestPoint")
        bindmeshTransferClusterBlinksNode = rigrepo.nodes.transferDeformer.TransferClusterBlinks('transferBlinkClusters',
                                                            source="body_geo")
        bindmeshTransferClusterLidsNode = rigrepo.nodes.transferDeformer.TransferClusterLids('transferLidsClusters', 
                                                            source="body_geo")
        freezeWireNode = rigrepo.nodes.goToRigPoseNode.GoToFreezePoseNode('freezeWire')
        freezeWireExpression = rigrepo.nodes.utilNodes.FreezeWireExpressionNode("FreezeWireExpression")


        lipYankNode = rigrepo.nodes.yankClusterNode.YankClusterNode('WireToClusters',
                                                    clusters='[trs+"_cluster" for trs in mc.ls("lip_*.__control__", o=True)]',
                                                    transforms='mc.ls("lip_*.__control__", o=True)',
                                                    selected=False,
                                                    geometry="body_geo")

        applyWireNode = applyDeformerNode.getChild("wire")
        applyWireNode.addChildren([freezeWireNode, lipYankNode])


        applyDeformerNode.addChildren([bindmeshTransferSkinWtsNode], 1)
        applyDeformerNode.addChildren([bindmeshTransferClusterBlinksNode, bindmeshTransferClusterLidsNode], 4)

        wiresToSkinClusterNode = rigrepo.nodes.wiresToSkinClusterNode.WiresToSkinClusterNode("wireToSkinCluster", 
                                                                        wireList='mc.ls(["*leg*", "*arm*", "*spine*"], type="wire")', 
                                                                        targetGeometry='body_geo',
                                                                        deformerName='body_wire', 
                                                                        keepWires=False,
                                                                        jointDepth=4)
        wiresToSkinClusterNode.disable()
        deliveryNode = self.getNodeByPath("|animRig|delivery")
        deliveryNode.addChild(wiresToSkinClusterNode, index=0)

        # This must be at the end of the build
        applyNode.addChild(freezeWireNode)
        freezeWireNode.addChild(freezeWireExpression)

        # TEMP: Speed up face build
        fastFace = True
        if fastFace:
            lipYankNode.disable()
            bindmeshTransferClusterBlinksNode.disable()
            bindmeshTransferClusterLidsNode.disable()
        
    
        # create a build node to put builds under.
        buildNode = pubs.pNode.PNode("build")
        # add nodes to the build
        buildNode.addChildren([bodyBuildNode, faceBuildNode])

        # add children to the animRigNode
        animRigNode.addChildren([buildNode], 
                                index=postBuild.index())

        l_leg.getAttributeByName('anchor').setValue('hip_swivel')
        r_leg.getAttributeByName('anchor').setValue('hip_swivel')
