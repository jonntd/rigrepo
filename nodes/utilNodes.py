
'''
This is a node for creating a new scene.
'''

import rigrepo.nodes.commandNode as commandNode

class ClusterControlNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None):
        '''
        This node is used to set the defaults. Currently it's set to use biped controls. 
        the user has the ability to make changes to it. 

        '''
        super(ClusterControlNode, self).__init__(name, parent)
        # add the attributes on the node.

        commandAttribute = self.getAttributeByName('command')

        # these are the list attributes that will be used and replaced in the command.
        self.addAttribute('parent', 'rig', attrType=str, index=0)
        self.addAttribute('nameList', '["cluster_control"]', attrType=str, index=0)
        self.addAttribute('geometry', 'body_geo', attrType=str, index=0)

        # create the command that the user can change later.
        cmd='''
import maya.cmds as mc
import rigrepo.libs.control
import rigrepo.libs.cluster
for name in {nameList}:
            rigrepo.libs.cluster.create("{geometry}", name=name, parent="{parent}")

            # rename the cluster and control                                    
            mc.rename(name, '%s_cluster' % name)
            mc.rename('%s_ctrl' % name, name)
            mc.xform("%s_nul" % name, ws=True, matrix=mc.xform("{parent}", q=True, ws=True, matrix=True))
            mc.setAttr("%s.displayHandle" % name, 1)
            rigrepo.libs.control.tagAsControl(name)
'''

        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        parent = self.getAttributeByName("parent").getValue()
        nameList = eval(self.getAttributeByName("nameList").getValue())
        geometry = self.getAttributeByName('geometry').getValue()
        exec(self.getAttributeByName('command').getValue().format(nameList=nameList,parent=parent, geometry=geometry))