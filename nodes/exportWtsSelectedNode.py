
'''
This is a node for exporting skinCluster weights
'''

import rigrepo.nodes.commandNode as commandNode

class ExportWtsSelectedNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp"):
        super(ExportWtsSelectedNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('dirPath', dirPath, attrType='dir', index=0)
        cmd = '''
import rigrepo.libs.weights
import maya.cmds as mc

sc_nodes = list()
sel = mc.ls(sl=1)
if sel:
    meshes = mc.listRelatives(sel, ad=1, type=('mesh', 'nurbsCurve'))
    for mesh in meshes:
        sc = mc.ls(mc.listHistory(mesh, pdo=1, il=1), type='skinCluster')
        if sc:
            sc_nodes.append(sc[0])
    for sc in sc_nodes:
        geo = mc.deformer(sc, g=1, q=1)
        if geo:
            geo = mc.listRelatives(geo, p=1)[0]
            if sc != (geo+'_skinCluster'):
                sc = mc.rename(sc, geo + '_skinCluster')
            print('exporting ' + sc)
            rigrepo.libs.weights.exportWeights(geo, sc, "{dirPath}")

    print('\\nexported '+str(len(sc_nodes))+' skinClusters'),
else:
    print("\\nSelect geometry our a group containing geometry"),
'''
        # command 
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        dirPath = self.getAttributeByName("dirPath").getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath))
        

        
