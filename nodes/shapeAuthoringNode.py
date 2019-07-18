
'''
This is a node that with useful commands for sculpting and editing shapes.
'''

import rigrepo.nodes.commandNode as commandNode

class ShapeAuthoringNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, action='duplicate'):
        super(ShapeAuthoringNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('action', action, attrType='str', index=0)
        # -----------------------------------------------------------
        cmd = '''
import maya.cmds as mc
import rigrepo.libs.common as common
import maya.mel as mm


#############
# DUPLICATE #
#############

if action == 'duplicate':
    sel = common.getFirstIndex(mc.ls(sl=1))
    if not sel:
        mc.error('Please select a mesh')

    subdiv = mc.duplicate(sel, n=sel+'_subdiv')[0]
    mc.polySmooth(subdiv)
    subdiv_negative = mc.duplicate(subdiv, n='negative_subdiv')[0]
    mc.select(cl=1)
    mc.blendShape(subdiv, subdiv_negative, sel, w=([0,1], [1,-1]), tc=0)
    mc.hide(sel)
    mc.delete(subdiv_negative)
    mc.delete(subdiv, ch=1)
    
    # Add message attribute
    if not mc.objExists(sel+'.subdiv'):
        mc.addAttr(subdiv, ln='subdiv', at='message')
        mc.addAttr(sel, ln='subdiv', at='message')
    mc.connectAttr(sel+'.subdiv', subdiv+'.subdiv', )
    
    mc.select(subdiv)
    
##########
# TOGGLE #
##########

if action == 'toggle':
    sel = common.getFirstIndex(mc.ls(sl=1))
    if not sel:
        mc.error('Please select a mesh')
    if mc.objExists(sel+'.subdiv'):
        otherMesh = common.getFirstIndex(mc.listConnections(sel+'.subdiv'))
        if otherMesh:
            mc.showHidden(otherMesh)
            mc.hide(sel)
            mc.select(otherMesh)
    
##########
# COMMIT #
##########

if action == 'commit':
    sel = common.getFirstIndex(mc.ls(sl=1))
    if not sel:
        mc.error('Please select a mesh')
    if mc.objExists(sel+'.subdiv'):
        sourceMesh = common.getFirstIndex(mc.listConnections(sel+'.subdiv'))
        if sourceMesh:
            mc.delete(sourceMesh, ch=1)
            mc.delete(sel)
            mc.showHidden(sourceMesh)
            mc.deleteAttr(sourceMesh+'.subdiv')
            
#################
# Extract Faces #
#################

if action == 'extract':
            
    sel = common.getFirstIndex(mc.ls(sl=1, o=1))
    if not sel:
        mc.error('Please select some faces')

    # Grow selection so we don't get get the border edge points
    mc.polySelectConstraint(pp=1, t=0x0008)
    mm.eval('InvertSelection')
    selFaces = mc.ls(sl=1)

    # Ponts that will be removed from the wrap membership
    pointsToRemove = mc.polyListComponentConversion(selFaces, toVertex=1)

    # Grow again so we get the border faces to delete
    mc.polySelectConstraint(pp=1, t=0x0008)
    selFaces = mc.ls(sl=1)

    # Dup
    part = mc.duplicate(sel, n=sel+'_part')[0]

    # Delete faces on dup
    facesToDelete = [part+'.'+x.split('.')[1] for x in selFaces] 
    mc.delete(facesToDelete)

    # Build Wrap
    mc.select(sel, part)
    # From C:/Program Files/Autodesk/Maya2018/scripts/others/performCreateWrap.mel
    exclusiveBind = '1'
    wrap = mm.eval('doWrapArgList "7" {{ "1","0","1", "2", "'+exclusiveBind+'", "1", "0", "0" }}')[0]
    set = mc.listConnections(wrap+'.message')[0]
    mc.sets(pointsToRemove, remove=set)

    mc.select(part)

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


        
