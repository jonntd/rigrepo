
'''
This is a node for exporting skinCluster weights
'''

import rigrepo.nodes.commandNode as commandNode
import maya.cmds as mc
class ExportSkinWtsDirNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp"):
        super(ExportSkinWtsDirNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('dirPath', dirPath, attrType='dir', index=0)
        cmd = '''
import rigrepo.libs.weights
import maya.cmds as mc
import rigrepo.libs.skinCluster
import rigrepo.libs.cluster

rigrepo.libs.skinCluster.removeLocalize(mc.ls(type="skinCluster"))

model_grp = 'model'
sc_nodes = list()
if mc.objExists(model_grp):
    meshes = mc.listRelatives(model_grp, ad=1, type=('mesh', 'nurbsCurve'))
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
'''
        # command 
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        dirPath = self.getAttributeByName("dirPath").getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath))
        


class ExportWtsDirNode(ExportSkinWtsDirNode):   
    def __init__(self, name, parent=None, dirPath="/disk1/temp", deformerType="cluster", excludeNodes='[]'):
        super(ExportWtsDirNode, self).__init__(name, parent, dirPath)
        self.addAttribute('deformerType', deformerType, attrType=str, index=1)
        self.addAttribute('excludeNodes', excludeNodes, attrType=str, index=2)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import rigrepo.libs.weights
import maya.cmds as mc

model_grp = 'model'
deformer_nodes = list()
if mc.objExists(model_grp):
    meshes = mc.listRelatives(model_grp, ad=True, type=('mesh', 'nurbsCurve'))
    for mesh in meshes:
        deformer_nodes.extend(mc.ls(mc.listHistory(mesh, pdo=True, il=True), type="{deformerType}"))
    if {excludeNodes}:
        deformer_nodes = list(set(deformer_nodes).difference(set({excludeNodes})))
    for deformer in deformer_nodes:
        geo = mc.ls(list(set(mc.deformer(deformer, g=True, q=True)).intersection(set(meshes))))
        if geo:
            geo = mc.listRelatives(geo, p=True)[0]
            print('exporting ' + deformer)
            rigrepo.libs.weights.exportWeights(geo, deformer, "{dirPath}")

    print('\\nexported '+str(len(deformer_nodes))+"{deformerType}"+' deformers')
'''
        # command 
        commandAttribute.setValue(cmd)
    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        dirPath = self.getAttributeByName("dirPath").getValue()
        deformerType = self.getAttributeByName("deformerType").getValue()
        excludeNodes = eval(self.getAttributeByName("excludeNodes").getValue())
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath,
                                                                deformerType=deformerType,
                                                                excludeNodes=excludeNodes))