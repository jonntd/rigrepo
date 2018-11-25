
'''
This is a node for mirroring curves
'''

import rigrepo.nodes.commandNode as commandNode
import maya.cmds as mc
class MirrorWiresNode(commandNode.CommandNode):
    '''
    Define cmd to be executed
    '''
    def __init__(self, name, parent=None):
        super(MirrorWiresNode, self).__init__(name, parent)
        self.addAttribute('lipCurves',  'mc.ls("lip*", type="nurbsCurve", ni=True)', attrType='str', index=0)
        self.addAttribute('lipCurveMapping', '{"center":(1, 9), "left":(0, 10, 11, 12, 13, 14 , 15), "right":(2, 8, 7, 6, 5, 4, 3)}', attrType='str', index=1)
        self.addAttribute('blinkCurves', '[mc.listRelatives(curve, p=True)[0] for curve in mc.ls("lid*", type="nurbsCurve", ni=True)]', attrType='str', index=2)
        commandAttribute = self.getAttributeByName('command')
        cmd = '''
import maya.cmds as mc
import rigrepo.libs.curve
import traceback
from rigrepo.libs.common import getSideToken

mc.undoInfo(openChunk=1)
try:
    # Mirror
    for n in {blinkCurves}:
        if getSideToken(n) is 'l':
            rigrepo.libs.curve.mirror(n)

    for curve in {lipCurves}:
        for leftIndex, rightIndex in zip({lipCurveMapping}["left"], {lipCurveMapping}["right"]):
            leftPosition = mc.xform("%s.cv[%s]" % (curve, leftIndex), q=True, ws=True, t=True)
            mc.xform("%s.cv[%s]" % (curve, rightIndex), ws=True, t=(leftPosition[0] *-1, leftPosition[1],leftPosition[2]))
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
        lipCurves = eval(self.getAttributeByName("lipCurves").getValue())
        blinkCurves = eval(self.getAttributeByName("blinkCurves").getValue())
        lipCurveMapping = eval(self.getAttributeByName("lipCurveMapping").getValue())
        exec(self.getAttributeByName('command').getValue().format(blinkCurves=blinkCurves,
                                                                    lipCurves=lipCurves,
                                                                    lipCurveMapping=lipCurveMapping))

