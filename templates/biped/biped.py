'''
'''
import maya.cmds as mc
import rigrepo.templates.base.base as base
import rigrepo.parts.arm
import rigrepo.parts.limb
import rigrepo.parts.spine 
import rigrepo.parts.blink
import rigrepo.parts.neck
import os

class Biped(base.Base):
    def __init__(self,name):
        super(Biped, self).__init__(name)

        # HERE THE THE LOAD FILE STUFF WE SHOULD TALK ABOUT.
        loadSkeleton = base.LoadFile(name="loadSkeleton")
        skeletonPath = os.path.join(os.path.dirname(__file__),'build','skeleton.ma').replace('\\','/')
        loadSkeleton.getAttributeByName("filepath").setValue(skeletonPath)
        pSpine = rigrepo.parts.spine.Spine(name='pSpine', jointList=mc.ls('spine_*_bind'))
        pNeck = rigrepo.parts.neck.Neck(name='pNeck', jointList=mc.ls('neck_*_bind'))

        l_arm = rigrepo.parts.arm.Arm("l_arm",['clavicle_l_bind', 'shoulder_l_bind', 'elbow_l_bind', 'wrist_l_bind'], anchor='chest')
        r_arm = rigrepo.parts.arm.Arm("r_arm",['clavicle_r_bind', 'shoulder_r_bind', 'elbow_r_bind', 'wrist_r_bind'], anchor='chest')

        l_leg = rigrepo.parts.limb.Limb("l_leg",['thigh_l_bind', 'knee_l_bind', 'ankle_l_bind'], pSpine.getHipSwivelCtrl)
        r_leg = rigrepo.parts.limb.Limb("r_leg",['thigh_r_bind', 'knee_r_bind', 'ankle_r_bind'], pSpine.getHipSwivelCtrl)
        
        # This need to be finished. I am putting it in here to chat. There are still a 
        # few moving pieces. Seems like the Point on curve info node is cycling. I am downloading 
        # update 2 to see if that takes care of it.
        l_blink = rigrepo.parts.blink.Blink("l_blink")
        r_blink = rigrepo.parts.blink.Blink("r_blink",side="r")
        r_blink.getAttributeByName("side").setValue("r")

        self.addNode(loadSkeleton)
        self.addNode(pSpine)
        self.addNode(pNeck)
        self.addNode(l_arm)
        self.addNode(r_arm)
        self.addNode(l_leg)
        self.addNode(r_leg)
        self.addNode(l_blink)
        self.addNode(r_blink)

        l_leg.getAttributeByName('anchor').setValue('hip_swivel')
        r_leg.getAttributeByName('anchor').setValue('hip_swivel')
