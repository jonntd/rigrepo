'''
'''
import maya.cmds as mc
import rigrepo.templates.archetype.rig.build.archetypeRig as archetypeRig
import pubs.pNode
from rigrepo.libs.fileIO import joinPath 
import rigrepo.nodes.loadFileNode
import rigrepo.nodes.newSceneNode
import rigrepo.nodes.importDataNode
import rigrepo.nodes.exportDataNode
import rigrepo.parts.arm
import rigrepo.parts.leg
import rigrepo.parts.spine 
import rigrepo.parts.blink
import rigrepo.parts.neck
import rigrepo.parts.neck
import rigrepo.parts.hand
import os

class BipedRig(archetypeRig.ArchetypeRig):
    def __init__(self,name):
        super(BipedRig, self).__init__(name)

        animRigNode = self.getNodeByName("animRig")

        buildPath = joinPath(os.path.dirname(__file__), self.variant)

        # Skeleton 
        skeletonFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("skeleton", filePath=joinPath(buildPath, 'skeleton.ma'))
        jointDataNode = rigrepo.nodes.importDataNode.ImportDataNode('jointPositions',dataFile=joinPath(buildPath, 'joint_positions.data'), dataType='joint', apply=True)
        # Curve
        curveFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("curves", filePath=joinPath(buildPath, 'blink_curves.ma'))

        # Parts
        pSpine = rigrepo.parts.spine.Spine(name='pSpine', jointList="mc.ls('spine_*_bind')")
        pNeck = rigrepo.parts.neck.Neck(name='pNeck', jointList="mc.ls('neck_*_bind')")
        l_arm = rigrepo.parts.arm.Arm("l_arm",['clavicle_l_bind', 'shoulder_l_bind', 'elbow_l_bind', 'wrist_l_bind'], anchor='chest')
        r_arm = rigrepo.parts.arm.Arm("r_arm",['clavicle_r_bind', 'shoulder_r_bind', 'elbow_r_bind', 'wrist_r_bind'], anchor='chest')
        l_hand = rigrepo.parts.hand.Hand("l_hand",['ring_001_l_bind', 'middle_001_l_bind', 'index_001_l_bind', 'pinkyCup_l_bind', 'thumbCup_l_bind'])
        r_hand = rigrepo.parts.hand.Hand("r_hand",['ring_001_r_bind', 'middle_001_r_bind', 'index_001_r_bind', 'pinkyCup_r_bind', 'thumbCup_r_bind'], 'wrist_r_bind_blend')
        l_leg = rigrepo.parts.leg.Leg("l_leg",['pelvis_l_bind', 'thigh_l_bind', 'knee_l_bind', 'ankle_l_bind'], pSpine.getHipSwivelCtrl)
        r_leg = rigrepo.parts.leg.Leg("r_leg",['pelvis_r_bind', 'thigh_r_bind', 'knee_r_bind', 'ankle_r_bind'], pSpine.getHipSwivelCtrl)
        
        l_blink = rigrepo.parts.blink.Blink("l_blink")
        r_blink = rigrepo.parts.blink.Blink("r_blink",side="r")
        r_blink.getAttributeByName("side").setValue("r")

        # get the load node which is derived from archetype.
        load = self.getNodeByName('load')
        load.addChild(skeletonFileNode) 
        load.addChild(jointDataNode) 
        load.addChild(curveFileNode) 
        l_arm.addChild(l_hand)
        r_arm.addChild(r_hand)

        # declare the build order for the anim rig node that you want to go in front of frame camera
        AnimRigBuildOrder = [load,
                            pSpine,
                            pNeck,
                            l_arm,
                            r_arm,
                            l_blink,
                            r_blink]

        animRigNode.addChildren(AnimRigBuildOrder, 
                                index=animRigNode.getChild('frameCamera').index())

        l_leg.getAttributeByName('anchor').setValue('hip_swivel')
        r_leg.getAttributeByName('anchor').setValue('hip_swivel')

        # Workflow
        workflow = pubs.pNode.PNode('workflow')
        workflow.disable()
        exporters = pubs.pNode.PNode('exporters')
        jointExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('jointPositions',dataFile=joinPath(buildPath, 'joint_positions.data'), dataType='joint', apply=True)
        #curveExportDataNode = rigrepo.nodes.exportDataNode.ExportDataNode('curvePositions',dataFile=joinPath(buildPath, 'joint_positions.data'), dataType='joint', apply=True)
        self.addNode(workflow)
        workflow.addChild(exporters)
        exporters.addChild(jointExportDataNode)
        #exporters.addChild(curveExportDataNode)

