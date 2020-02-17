'''
This is a node for converting wires into skinClusters
'''
import maya.cmds as mc
import rigrepo.nodes.commandNode as commandNode

class WiresToSkinClusterNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None, wireList='mc.ls(type="wire")', targetGeometry='body_geo',
                    deformerName='body_wire', keepWires=False, rootParentNode="rig", 
                    rootPreMatrixNode="trs_aux", jointDepth=2):
        super(WiresToSkinClusterNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('wireList', wireList, attrType=str, index=0)
        self.addAttribute('targetGeometry',targetGeometry, attrType=str, index=1)
        self.addAttribute('deformerName', deformerName, attrType=str, index=2)
        self.addAttribute('keepWires', keepWires, attrType=bool, index=3)
        self.addAttribute('rootParentNode', rootParentNode, attrType=str, index=4)
        self.addAttribute('rootPreMatrixNode', rootPreMatrixNode, attrType=str, index=5)
        self.addAttribute('jointDepth', jointDepth, attrType=int, index=6)

        cmd = '''
import maya.cmds as mc
import rigrepo.libs.wire
import traceback

mc.undoInfo(openChunk=1)
try:
    print {jointDepth}
    rigrepo.libs.wire.convertWiresToSkinCluster("{deformerName}", "{targetGeometry}",{wireList}, {keepWires}, "{rootParentNode}", "{rootPreMatrixNode}", {jointDepth})   
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
        deformerName = self.getAttributeByName("deformerName").getValue()
        wireList = eval(self.getAttributeByName("wireList").getValue())
        targetGeometry = self.getAttributeByName("targetGeometry").getValue()
        keepWires = self.getAttributeByName("keepWires").getValue()
        rootParentNode = self.getAttributeByName("rootParentNode").getValue()
        rootPreMatrixNode = self.getAttributeByName("rootPreMatrixNode").getValue()
        jointDepth = self.getAttributeByName("jointDepth").getValue()
        exec(self.getAttributeByName('command').getValue().format(deformerName=deformerName,
                                                                  targetGeometry=targetGeometry,
                                                                  wireList=wireList,
                                                                  keepWires=keepWires,
                                                                  rootParentNode=rootParentNode,
                                                                  rootPreMatrixNode=rootPreMatrixNode,
                                                                  jointDepth=jointDepth))