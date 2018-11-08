import inspect
'''
This is a node for mirroring skinClusters
'''

import rigrepo.nodes.commandNode as commandNode

class YankSkinClusterNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(YankSkinClusterNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import traceback
import rigrepo.libs.shape
reload(rigrepo.libs.shape)

mc.undoInfo(openChunk=1)
try:
    sel = mc.ls(sl=1, dag=1, s=1, ni=1)
    if not sel:
        sel = mc.ls(hl=1, dag=1, s=1, ni=1)
    if sel:
        sc = mc.ls(mc.listHistory(sel, pdo=1, il=1), type='skinCluster')
        if sc:
            deltaMush = mc.ls(mc.listHistory(sel, pdo=1, il=1), type='deltaMush')
            if deltaMush:
                for d in deltaMush:
                    mc.setAttr(d+'.envelope', 1)
            base = mc.listRelatives(sel, p=1)[0]
            target = mc.duplicate(base)[0]
            weights = dict()
            sc = sc[0]
            infs = mc.skinCluster(sc, q=1, inf=1)
            for inf in infs:
                #tempInf = mc.duplicate(inf, po=1) 
                matrixCon = mc.listConnections(inf+'.worldMatrix[0]', p=1, d=1, s=0)
                infIndex = None
                for con in matrixCon:
                    node = con.split('.')[0]
                    if node == sc:
                        infIndex = con.split('[')[1].split(']')[0]
                if infIndex:
                    tempInf = mc.duplicate(inf, po=1)[0]
                    mc.connectAttr(tempInf+'.worldMatrix[0]', sc+'.matrix[{}]'.format(infIndex), f=1)
                    mc.move( -1, 0, 0, tempInf, r=1, worldSpaceDistance=1) 
                    weights[inf] = rigrepo.libs.shape.getDeltas(base, target)
                    mc.connectAttr(inf+'.worldMatrix[0]', sc+'.matrix[{}]'.format(infIndex), f=1)                         
                    mc.delete(tempInf)
            # Set Weights
            for inf in infs:
                rigrepo.libs.weights.setWeights(sc, weights[inf], map=inf) 
            if deltaMush:
                for d in deltaMush:
                    mc.setAttr(d+'.envelope', 0)
            mc.delete(target)     
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
        exec(self.getAttributeByName('command').getValue())
