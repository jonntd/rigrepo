
'''
This is a node for creating a new scene.
'''

import rigrepo.nodes.commandNode as commandNode

class ControlDefaultsNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None, 
        armControls=["*_shoulder","*_elbow","*_wrist*"],
        armParams=["arm_?"], legParams=["leg_?"]):
        '''
        This node is used to set the defaults. Currently it's set to use biped controls. 
        the user has the ability to make changes to it. 

        .. note: We may want to change the name of this to bipedControlDefaults.

        :param armControls: The arm controls you wish to set default rotation to 0
        :type armControls: list | str

        :param armParams: Arm parameter nodes you need to set ikfk attribute on
        :type armParams: list | str
        '''
        super(ControlDefaultsNode, self).__init__(name, parent)
        # add the attributes on the node.

        commandAttribute = self.getAttributeByName('command')

        # these are the list attributes that will be used and replaced in the command.
        self.addAttribute('armControls', armControls, attrType='list')
        self.addAttribute('armParams', armParams, attrType='list')
        self.addAttribute('legParams', legParams, attrType='list')

        # create the command that the user can change later.
        cmd='''
import maya.cmds as mc
import rigrepo.libs.control
import rigrepo.parts.limb
import rigrepo.parts.limb as limb
import rigrepo.parts.foot as foot
for ctrl in mc.ls({armParams}):
    mc.setAttr(ctrl+".ikfk",1)
    mc.setAttr(ctrl+".softStretch",.2)
for ctrl in mc.ls({legParams}):
    mc.setAttr(ctrl+".softStretch",.2)
    limb.Limb.switch(ctrl, 1)
    try:
        foot.Foot.switch(ctrl, 1)
    except:
        pass

rigrepo.libs.control.setPoseAttr(rigrepo.libs.control.getControls(), 0)
for ctrl in mc.ls({armControls}):
    mc.setAttr(ctrl+".r", 0,0,0)

rigrepo.libs.control.setPoseAttr(rigrepo.libs.control.getControls(), 1)
rigrepo.libs.control.toPoseAttr(rigrepo.libs.control.getControls())
'''

        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        armControls = self.getAttributeByName("armControls").getValue()
        armParams = self.getAttributeByName("armParams").getValue()
        legParams = self.getAttributeByName("legParams").getValue()
        exec(self.getAttributeByName('command').getValue().format(armControls=armControls, 
                                                                    armParams=armParams, 
                                                                    legParams=legParams))