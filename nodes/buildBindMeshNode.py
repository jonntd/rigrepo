
'''
This is a node for building bind meshes
'''

import rigrepo.nodes.commandNode as commandNode

class BuildBindMeshNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, curves="['curveName']"):
        super(BuildBindMeshNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('curves', curves, attrType='str', index=0)
        cmd = '''
import maya.cmds as mc
import maya.mel as mm
import rigrepo.libs.bindmesh as bindmesh
import rigrepo.libs.common as common

if {curves}:
    grp = mc.group(empty=1, n='bindmeshes_grp')
    if mc.objExists('rig'):
        mc.parent(grp, 'rig')
    for curve, name in {curves}:
        if mc.objExists(curve):
            bindmeshGeometry, follicleList = bindmesh.createFromCurve(name, curve)
            mc.parent(bindmeshGeometry, follicleList, grp)
        else:
            print(curve+' does not exist to build bindmeshes for.')
'''
        # command
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        curves = self.getAttributeByName("curves").getValue()
        exec(self.getAttributeByName('command').getValue().format(curves=curves))
        
