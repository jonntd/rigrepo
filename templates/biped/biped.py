'''
'''
import rigrepo.templates.base.base as base
import rigrepo.parts.arm as arm
import rigrepo.parts.limb as limb

class Biped(base.Base):
    def __init__(self,name):
        super(Biped, self).__init__(name)

        l_arm = arm.Arm("l_arm",['clavicle_l_bind', 'shoulder_l_bind', 'elbow_l_bind', 'wrist_l_bind'])
        r_arm = arm.Arm("r_arm",['clavicle_r_bind', 'shoulder_r_bind', 'elbow_r_bind', 'wrist_r_bind'])

        l_leg = limb.Limb("l_leg",['thigh_l_bind', 'knee_l_bind', 'ankle_l_bind'])
        r_leg = limb.Limb("r_leg",['thigh_r_bind', 'knee_r_bind', 'ankle_r_bind'])

        self.addNode(l_arm)
        self.addNode(r_arm)
        self.addNode(l_leg)
        self.addNode(r_leg)

        
