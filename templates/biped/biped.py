'''
'''
import rigrepo.templates.base.base_template as base
import rigrepo.parts.part as part

class Biped(base.Base):
    def __init__(self,name):
        super(Biped, self).__init__(name)

        l_arm = part.Part("l_arm")
        #l_arm.addAttribute('test', 1.0, attrType = float)
        l_hand = part.Part("l_hand")
        l_arm.addChild(l_hand)
        self.addNode(l_arm)

        
