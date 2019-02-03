
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
        self.addAttribute('displayHandle', True, attrType=bool, index=0)
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
    if {displayHandle}:
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
        displayHandle = self.getAttributeByName('displayHandle').getValue()
        exec(self.getAttributeByName('command').getValue().format(nameList=nameList,parent=parent, 
            geometry=geometry, displayHandle=displayHandle))


class FreezeWireExpressionNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None):
        '''
        This node is used to set the defaults. Currently it's set to use biped controls. 
        the user has the ability to make changes to it. 

        '''
        super(FreezeWireExpressionNode, self).__init__(name, parent)
        # add the attributes on the node.

        commandAttribute = self.getAttributeByName('command')

        # create the command that the user can change later.
        cmd="""
import maya.cmds as mc
cmd = '''import maya.cmds as mc
import rigrepo.libs.control
controlList = rigrepo.libs.control.getControls('*') or rigrepo.libs.control.getControls()
wireList = mc.ls(type="wire")
autoKeyframeState = mc.autoKeyframe(q=True, state=True)
mc.autoKeyframe(state=False)
rigrepo.libs.control.setPoseAttr(controlList, poseAttr=10) 
for wire in wireList:
    mc.setAttr("{}.freezeGeometry".format(wire), 0)

rigrepo.libs.control.toPoseAttr(controlList, 9)
for wire in wireList:
    mc.setAttr("{}.freezeGeometry".format(wire), 1)
    mc.refresh()
    
rigrepo.libs.control.toPoseAttr(controlList,10)

for ctrl in controlList:
    mc.deleteAttr("{}.poseAttr_10".format(ctrl))
    
mc.autoKeyframe(state=autoKeyframeState)
'''
mc.evalDeferred(cmd)
"""
        cmd='''
import maya.cmds as mc
mc.scriptNode(st=1, sourceType="python", bs="""{}""", n='poseFreeze')
        '''.format(cmd)
        
        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        exec(self.getAttributeByName('command').getValue())