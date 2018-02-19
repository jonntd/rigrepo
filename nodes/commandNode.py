'''
This is the base component for all the rig components
'''
#import package modules
import pubs.pNode

class CommandNode(pubs.pNode.PNode):
    def __init__(self, name, parent = None):
        super(CommandNode, self).__init__(name, parent)
        
        self.addAttribute("command", '#write your python code here', attrType = "code")
    
    def execute(self, **kwargs):
         exec(self.getAttributeByName('command').getValue())