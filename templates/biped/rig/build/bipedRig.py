'''
'''
import maya.cmds as mc
import rigrepo.templates.archetype.rig.build.archetypeRig as archetypeRig
import rigrepo.nodes.loadFileNode
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

        # HERE THE THE LOAD FILE STUFF WE SHOULD TALK ABOUT.
        #loadSkeleton = base.LoadFile(name="loadSkeleton")
        #loadFileNode = rigrepo.nodes.loadFileNode.LoadFileNode("LoadSkeleton")
        #skeletonPath = os.path.join(os.path.dirname(__file__),'base','skeleton.ma').replace('\\','/')
        #loadFileNode.getAttributeByName("filepath").setValue(skeletonPath)
        pSpine = rigrepo.parts.spine.Spine(name='pSpine', jointList=mc.ls('spine_*_bind'))
        pNeck = rigrepo.parts.neck.Neck(name='pNeck', jointList=mc.ls('neck_*_bind'))

        l_arm = rigrepo.parts.arm.Arm("l_arm",['clavicle_l_bind', 'shoulder_l_bind', 'elbow_l_bind', 'wrist_l_bind'], anchor='chest')
        r_arm = rigrepo.parts.arm.Arm("r_arm",['clavicle_r_bind', 'shoulder_r_bind', 'elbow_r_bind', 'wrist_r_bind'], anchor='chest')
        l_hand = rigrepo.parts.hand.Hand("l_hand",['ring_001_l_bind', 'middle_001_l_bind', 'index_001_l_bind', 'pinkyCup_l_bind', 'thumbCup_l_bind'])
        r_hand = rigrepo.parts.hand.Hand("r_hand",['ring_001_r_bind', 'middle_001_r_bind', 'index_001_r_bind', 'pinkyCup_r_bind', 'thumbCup_r_bind'], 'wrist_r_bind_blend')
        l_leg = rigrepo.parts.leg.Leg("l_leg",['pelvis_l_bind', 'thigh_l_bind', 'knee_l_bind', 'ankle_l_bind'], pSpine.getHipSwivelCtrl)
        r_leg = rigrepo.parts.leg.Leg("r_leg",['pelvis_r_bind', 'thigh_r_bind', 'knee_r_bind', 'ankle_r_bind'], pSpine.getHipSwivelCtrl)
        
        # This need to be finished. I am putting it in here to chat. There are still a 
        # few moving pieces. Seems like the Point on curve info node is cycling. I am downloading 
        # update 2 to see if that takes care of it.
        l_blink = rigrepo.parts.blink.Blink("l_blink")
        r_blink = rigrepo.parts.blink.Blink("r_blink",side="r")
        r_blink.getAttributeByName("side").setValue("r")

        #self.addNode(loadFileNode)
        self.addNode(pSpine)
        self.addNode(pNeck)
        l_arm.addChild(l_hand)
        self.addNode(l_arm)
        r_arm.addChild(r_hand)
        self.addNode(r_arm)
        self.addNode(l_leg)
        self.addNode(r_leg)
        self.addNode(l_blink)
        self.addNode(r_blink)

        l_leg.getAttributeByName('anchor').setValue('hip_swivel')
        r_leg.getAttributeByName('anchor').setValue('hip_swivel')
