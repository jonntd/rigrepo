'''
This is a node for adding spaces to controls.
'''

import rigrepo.nodes.commandNode as commandNode

class AddSpaceNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None, attrNode='', constraintNode='', parentNode='rig', targetList=list(), 
        nameList=list(), constraintType='parent'):
        '''
        This node is used to set the defaults. Currently it's set to use biped controls. 
        the user has the ability to make changes to it. 
        '''
        super(AddSpaceNode, self).__init__(name, parent)
        # add the attributes on the node.

        commandAttribute = self.getAttributeByName('command')

        # these are the list attributes that will be used and replaced in the command.
        self.addAttribute('attrNode', attrNode, attrType=str, index=0)
        self.addAttribute('constraintNode', constraintNode, attrType=str, index=1)
        self.addAttribute('parent', parentNode, attrType=str, index=2)
        self.addAttribute('targetList', '{}'.format(targetList), attrType=str, index=3)
        self.addAttribute('nameList', '{}'.format(nameList), attrType=str, index=4)
        self.addAttribute('constraintType', constraintType, attrType=str, index=5)
        # create the command that the user can change later.
        cmd='''
import maya.cmds as mc
import rigrepo.libs.spaces

if mc.objExists("{constraintNode}") and mc.objExists("{attrNode}"):
    group=rigrepo.libs.spaces.create("{constraintNode}", "{attrNode}", parent="{parent}")
    if {targetList} and {nameList}:
        rigrepo.libs.spaces.addSpace("{constraintNode}",{targetList},{nameList},group,"{attrNode}","{constraintType}")
'''
        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass i to the command.
        constraintNode = self.getAttributeByName('constraintNode').getValue()
        attrNode = self.getAttributeByName('attrNode').getValue()
        parent = self.getAttributeByName("parent").getValue()
        targetList = eval(self.getAttributeByName("targetList").getValue())
        nameList = eval(self.getAttributeByName("nameList").getValue())
        constraintType = self.getAttributeByName('constraintType').getValue()
        exec(self.getAttributeByName('command').getValue().format(constraintNode=constraintNode, 
            attrNode=attrNode, parent=parent, targetList=targetList,nameList=nameList,
            constraintType=constraintType)) 