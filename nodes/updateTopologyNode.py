
'''
This node is for updating the topology of a rigged mesh by transferring
the deformers between different topologies.
It assumes every mesh under the model node will be transferred.
'''

import rigrepo.nodes.commandNode as commandNode

class UpdateTopologyNode(commandNode.CommandNode):
    '''
    UpdateTopologyNode class. Uses an action attribute to switch
    what chunks of code will be run in the cmd.
    '''
    def __init__(self, name, parent=None, action='rename'):
        super(UpdateTopologyNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('action', action, attrType='str', index=0)
        # -----------------------------------------------------------
        cmd = '''
import maya.cmds as mc
import rigrepo.libs.common as common
import maya.mel as mm
import rigrepo.libs.deformer
import rigrepo.libs.skinCluster as skinCluster

prefix = 'OLD_TOPO__'
model = 'model'

################
# Rename Model #
################

if action == 'rename':
    topNodes = list(set(mc.ls(assemblies=1))-set(['persp', 'top', 'front', 'side']))

    for node in topNodes:
        allDescendents = mc.listRelatives(node, ad=1, type='transform', path=1)
        if allDescendents:
            for child in allDescendents+[node]:
                mc.rename(child, prefix + child.split('|')[-1])
                
##############################
# Transfer SkinCluster Model #
##############################

if action == 'skinCluster':
    # Get geometry under the model
    geos = mc.listRelatives(prefix+model, ad=1, type='mesh', path=1, ni=1)
    geos = list(set(mc.listRelatives(geos, p=1, path=1, type='transform')))
    
    for geo in geos:
        sc = skinCluster.getSkinCluster(geo)
        if sc:
            target = geo.replace(prefix, '')
            if mc.objExists(target):
                sc = mc.rename(sc, prefix+sc)
                rigrepo.libs.deformer.transferDeformers(geo, 
                                                        [target], 
                                                        ['skinCluster'], 
                                                        'closestPoint')
                
#####################
# Replace The Model #
#####################

if action == 'replace':
    # Find the old top level transform and the new one with the new topology
    topNodes = list(set(mc.ls(assemblies=1))-set(['persp', 'top', 'front', 'side']))
    oldTop = None
    newTop = None
    for node in topNodes:
        if prefix in node:
            oldTop = node
            newTop = node.replace(prefix, '')
            break
    
    # Find the old model's parent
    par = mc.listRelatives(prefix+model, p=1)[0]
    # Move the new model there
    mc.parent(model, par)
    # Remove the old model and the new top node
    mc.delete(prefix+model, newTop)
    
    # Remove the prefix
    oldNames = mc.ls(prefix+'*')
    for name in oldNames:
        if mc.objExists(name):
            if name != name.replace(prefix, ''):
                mc.rename(name, name.replace(prefix, ''))
    
#'''
        # -----------------------------------------------------------
        # command
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        action = self.getAttributeByName("action").getValue()
        exec(self.getAttributeByName('command').getValue().format(action=action))


        
