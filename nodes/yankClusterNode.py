'''
This is a node for yanking clusters
'''
import inspect
import maya.cmds as mc
import rigrepo.nodes.commandNode as commandNode

class YankClusterNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, transforms='mc.ls(type="transform")', clusters='mc.ls(type="cluster")'):
        super(YankClusterNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('transforms', transforms, attrType='str', index=0)
        self.addAttribute('clusters', clusters, attrType='str', index=0)
        cmd = '''
import maya.cmds as mc
import traceback
import rigrepo.libs.shape
import rigrepo.libs.weightObject

mc.undoInfo(openChunk=1)
try:
    selectionList = mc.ls(sl=1, dag=1, s=1, ni=1)
    if not selectionList:
        selectionList = mc.ls(hl=1, dag=1, s=1, ni=1)
    if selectionList:
        for sel in selectionList:
            deltaMush = mc.ls(mc.listHistory(sel, pdo=1, il=1), type='deltaMush')
            if deltaMush:
                for d in deltaMush:
                    mc.setAttr(d+'.envelope', 1)
            target = mc.listRelatives(sel, p=1)[0]
            base = mc.duplicate(target)[0]
            for cls, trs in zip({clusters}, {transforms}):
                mc.move( 1, 0, 0, trs, r=1, worldSpaceDistance=1) 
                weightList = rigrepo.libs.shape.getDeltas(base, target)
                # Set Weights
                rigrepo.libs.weights.setWeights(cls, weights=weightList, geometry=sel) 
                mc.move( -1, 0, 0, trs, r=1, worldSpaceDistance=1) 
            if deltaMush:
                for d in deltaMush:
                    mc.setAttr(d+'.envelope', 0)
            mc.delete(base)     
except:
    traceback.print_exc()
mc.undoInfo(closeChunk=1)
'''
        # command 
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Execute node code
        '''
        clusters = eval(self.getAttributeByName("clusters").getValue())
        transforms = eval(self.getAttributeByName("transforms").getValue())
        exec(self.getAttributeByName('command').getValue().format(clusters=clusters,
                                                                    transforms=transforms))