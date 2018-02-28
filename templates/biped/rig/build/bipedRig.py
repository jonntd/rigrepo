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
import rigrepo.parts.foot
import os

class BipedRig(archetypeRig.ArchetypeRig):
    def __init__(self,name, variant='base'):
        '''
        This is the constructor for the biped template. Here is where you will put nodes onto 
        the graph. 

        :param name: Name of the element you're using this for
        :type name: str

        :param variant: Name of the variant this template is being used for.
        :type variant: str
        '''
        
        super(BipedRig, self).__init__(name, variant)

        animRigNode = self.getNodeByName("animRig")

        buildPath = joinPath(os.path.dirname(__file__), self.variant)

        # Skeleton 
        skeletonFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("skeleton", filePath=self.resolveDataFilePath('skeleton.ma', self.variant))
        jointDataNode = rigrepo.nodes.importDataNode.ImportDataNode('jointPositions',dataFile=self.resolveDataFilePath('joint_positions.data', self.variant), dataType='joint', apply=True)
        # Curve
        curveFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("curves", 
                            filePath=self.resolveDataFilePath('blink_curves.ma', self.variant))

        curveDataNode = rigrepo.nodes.importDataNode.ImportDataNode('curvePosition',
                            dataFile=self.resolveDataFilePath('curve_positions.data', self.variant), 
                            dataType='curve', 
                            apply=True)

        
        # Parts
        #-------------------------------------------------------------------------------------------
        # BODY
        #-------------------------------------------------------------------------------------------
        # center
        pSpine = rigrepo.parts.spine.Spine(name='pSpine', jointList="mc.ls('spine_*_bind')")
        pSpine.setNiceName("spine")

        pNeck = rigrepo.parts.neck.Neck(name='pNeck', jointList="mc.ls('neck_*_bind')")
        pNeck.setNiceName("neck")
        
        # Arm
        l_arm = rigrepo.parts.arm.Arm("l_arm", 
                                    ['clavicle_l_bind', 
                                        'shoulder_l_bind', 
                                        'elbow_l_bind', 
                                        'wrist_l_bind'], 
                                    anchor='chest')

        l_hand = rigrepo.parts.hand.Hand("l_hand",
                                        ['ring_001_l_bind', 
                                        'middle_001_l_bind', 
                                        'index_001_l_bind', 
                                        'pinkyCup_l_bind', 
                                        'thumbCup_l_bind'])
        # add hand to arm node.
        l_arm.addChild(l_hand)

        r_arm = rigrepo.parts.arm.Arm("r_arm",
                                    ['clavicle_r_bind', 
                                        'shoulder_r_bind', 
                                        'elbow_r_bind', 
                                        'wrist_r_bind'], 
                                    anchor='chest')
        
        

        r_hand = rigrepo.parts.hand.Hand("r_hand",
                                        ['ring_001_r_bind', 
                                            'middle_001_r_bind', 
                                            'index_001_r_bind', 
                                            'pinkyCup_r_bind', 
                                            'thumbCup_r_bind'], 
                                        'wrist_r_bind_blend')

        # add hand to arm node.
        r_arm.addChild(r_hand)
        
        # Leg
        l_leg = rigrepo.parts.leg.Leg("l_leg",
                                ['pelvis_l_bind', 'thigh_l_bind', 'knee_l_bind', 'ankle_l_bind'], 
                                pSpine.getHipSwivelCtrl)

        l_foot = rigrepo.parts.foot.Foot("l_foot", ['ankle_l_bind', 'ball_l_bind', 'toe_l_bind'], 
                                        'ankle_l_bind_ik_hdl', 
                                        fkAnchor='ankle_l_bind_fk_ctrl', 
                                        ikAnchor='ankle_l_bind_ik_offset', 
                                        anklePivot='ankle_l_pivot', 
                                        ankleStretchTarget="ankle_l_bind_ik_tgt",
                                        ikfkGroup='l_leg_ikfk_grp')
        # add foot to the leg node
        l_leg.addChild(l_foot)

        r_leg = rigrepo.parts.leg.Leg("r_leg",
                                ['pelvis_r_bind', 'thigh_r_bind', 'knee_r_bind', 'ankle_r_bind'], 
                                pSpine.getHipSwivelCtrl)       

        r_foot = rigrepo.parts.foot.Foot("r_foot", ['ankle_r_bind', 'ball_r_bind', 'toe_r_bind'], 
                                        'ankle_r_bind_ik_hdl', 
                                        fkAnchor='ankle_r_bind_fk_ctrl', 
                                        ikAnchor='ankle_r_bind_ik_offset', 
                                        anklePivot='ankle_r_pivot',
                                        ankleStretchTarget="ankle_r_bind_ik_tgt",
                                        ikfkGroup='r_leg_ikfk_grp')
        # add foot to the leg node
        r_leg.addChild(r_foot)


        #-------------------------------------------------------------------------------------------
        # FACE
        #-------------------------------------------------------------------------------------------
        l_blink = rigrepo.parts.blink.Blink("l_blink")
        r_blink = rigrepo.parts.blink.Blink("r_blink",side="r")
        r_blink.getAttributeByName("side").setValue("r")
        
        # create both face and body builds
        bodyBuildNode = pubs.pNode.PNode("body")
        faceBuildNode = pubs.pNode.PNode("face")
        # add nodes ass children of body
        bodyBuildNode.addChildren([pSpine, pNeck, l_arm, r_arm, l_leg, r_leg])
        faceBuildNode.addChildren([l_blink, r_blink])
        # get the load node which is derived from archetype.
        loadNode = self.getNodeByName('load')
        loadNode.addChild(skeletonFileNode) 
        loadNode.addChild(jointDataNode) 
        loadNode.addChild(curveFileNode) 
        loadNode.addChild(curveDataNode)
        
        # create a build node to put builds under.
        buildNode = pubs.pNode.PNode("build")
        # add nodes to the build
        buildNode.addChildren([bodyBuildNode, faceBuildNode])
        
        print self.getNodes()
        # add children to the animRigNode
        animRigNode.addChildren([buildNode], 
                                index=animRigNode.getChild('frameCamera').index())

        l_leg.getAttributeByName('anchor').setValue('hip_swivel')
        r_leg.getAttributeByName('anchor').setValue('hip_swivel')