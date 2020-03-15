
'''
This is a node for creating a new scene.
'''

import rigrepo.nodes.commandNode as commandNode

class TransferDeformer(commandNode.CommandNode):
    '''
    This node will just transfer the deformers from one mesh to another.
    '''
    def __init__(self, name, parent=None, 
        source="body_geo",
        target=["gum_upper_geo"],
        deformerTypes = ["skinCluster"],
        surfaceAssociation="closestPoint"):
        '''
        This node is used to transfer deformers from source mesh to target meshes.
        It will not create unique deformers. It will add them to the membership and project weights.

        :param source: Source mesh you will copy deformers from.
        :type source: str

        :param target: List of geometry you to transfer deformers on
        :type target: list

        :param deformerTypes: List of deformer types you want to transfer
        :type deformerTypes: list

        :param surfaceAccosiation: The surface association you want to use for the projection 
                                    of weights
        :type surfaceAccosiation: str
        '''
        super(TransferDeformer, self).__init__(name, parent)
        # add the attributes on the node.

        commandAttribute = self.getAttributeByName('command')

        # these are the list attributes that will be used and replaced in the command.
        self.addAttribute('source', source, attrType='str', index=0)
        self.addAttribute('target', 'mc.ls({})'.format(target), attrType='str', index=1)
        self.addAttribute('deformerTypes', deformerTypes, attrType='str', index=2)
        self.addAttribute('surfaceAssociation', surfaceAssociation, attrType='str', index=3)

        # create the command that the user can change later.
        cmd='''
import maya.cmds as mc
import rigrepo.libs.deformer
rigrepo.libs.deformer.transferDeformers("{source}", {target}, {deformerTypes}, "{surfaceAssociation}")
'''
        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        source = self.getAttributeByName("source").getValue()
        target = self.getAttributeByName("target").getValue()
        deformerTypes = self.getAttributeByName("deformerTypes").getValue()
        surfaceAssociation = self.getAttributeByName("surfaceAssociation").getValue()
        exec(self.getAttributeByName('command').getValue().format(source=source,
                                                                target=target, 
                                                                deformerTypes=deformerTypes,
                                                                surfaceAssociation=surfaceAssociation))


class TransferDeformerBindmesh(TransferDeformer):
    '''
    '''
    def __init__(self,name='bindmesh', parent=None,
        source="body_geo",
        target=["lip*_bindmesh", "mouth*_bindmesh"],
        deformerTypes = ["skinCluster"],
        surfaceAssociation="closestPoint"):
        '''
        This is the constructor
        '''
        super(TransferDeformerBindmesh, self).__init__(name, parent, source, target, deformerTypes, surfaceAssociation)
        # create the command that the user can change later.
        commandAttribute = self.getAttributeByName('command')
        cmd='''
import numpy
import maya.cmds as mc
import rigrepo.libs.deformer
deltaMush = mc.deltaMush("{source}",smoothingIterations=10,smoothingStep=1.0, pinBorderVertices=True,envelope=1, foc=True)[0]
mc.setAttr(deltaMush+".displacement", 0)
rigrepo.libs.deformer.transferDeformers("{source}", {target}, {deformerTypes}, "{surfaceAssociation}")

for mesh in {target}:
    deformer = mesh+"_skinCluster"
    wtObj = rigrepo.libs.weights.getWeights(deformer)
    weightList = list()
    for inf in wtObj:
        i = 0
        weights = wtObj.getWeights(inf)[0]
        for wt in weights:
            j = i
            if j + 1 >= len(weights):
                break
            wtValue = weights[j]
            while i <= j + 3:
                weights[i] = wtValue
                i +=1
            
        weightList.append(weights)
    wtObj.setWeights(weightList)
    rigrepo.libs.weights.setWeights(deformer, wtObj)

mc.delete(deltaMush)
'''
        # set the command to the attributes value
        commandAttribute.setValue(cmd)


class TransferClusterBlinks(commandNode.CommandNode):
    '''
    '''
    def __init__(self,name='transferLidClusters', parent=None, source="body_geo"):
        '''
        This is the constructor
        '''
        super(TransferClusterBlinks, self).__init__(name, parent)
        self.addAttribute('source', source, attrType='str', index=0)
        # create the command that the user can change later.
        commandAttribute = self.getAttributeByName('command')
        cmd='''
import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.libs.deformer
import rigrepo.libs.weights
import rigrepo.libs.cluster
import rigrepo.libs.curve
import rigrepo.libs.transform
source = "{source}"
temp = mc.createNode("closestPointOnMesh", name="temp")
sourceDag = rigrepo.libs.transform.getDagPath(source)
sourceDag.extendToShape()
mc.connectAttr("%s.outMesh" % (sourceDag.fullPathName()), "%s.inMesh" % (temp), f=True)
for side in ['l','r']:
    for section in ['Upper', 'Lower']:
        baseWire = "blink%s_%s_curveBaseWire" % (section, side)
        mesh = "blink%s_%s_bindmesh" % (section, side)
        newClusterList=rigrepo.libs.cluster.transferCluster(source, mesh, "blink%s_%s_cluster" % (section, side), handle=True, surfaceAssociation="closestPoint", createNew=True)
        for deformer in newClusterList:
            wtObj = rigrepo.libs.weights.getWeights(deformer, geometry=mesh)
            sourceWtObj = rigrepo.libs.weights.getWeights(deformer.split("__")[-1], geometry=source)
            weightList = list()
            
            i = 0
            weights = wtObj.getWeights()[0]
            sourceWeights = sourceWtObj.getWeights()[0]
            for wt in weights:
                j = i
                if j + 1 >= len(weights):
                    break
                # get the closest point on the curve so we can use that to get the closest
                mPoint = rigrepo.libs.curve.getPointOnCurveFromPosition(baseWire, "%s.cp[%s]" % (mesh, j))
                mc.setAttr("%s.inPosition" % (temp), mPoint.x, mPoint.y, mPoint.z)
                vrtId = mc.getAttr("%s.closestVertexIndex" % (temp))
                wtValue = sourceWeights[vrtId]
                while i <= j + 3:
                    weights[i] = wtValue
                    i +=1
                    
            weightList.append(weights)
            wtObj.setWeights(weightList)
            rigrepo.libs.weights.setWeights(deformer, wtObj, geometry=mesh)
                
        # now we will transfer the wts
        mc.copyDeformerWeights(ss=mesh, ds=baseWire, sd="blink%s_%s_bindmesh__blink%s_%s_cluster" % (section, side, section, side), dd="blink%s_%s_curveBaseWire__blink%s_%s_cluster" % (section, side, section, side), sa="closestPoint", noMirror=True)
mc.delete(temp)
'''
        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        source = self.getAttributeByName("source").getValue()
        exec(self.getAttributeByName('command').getValue().format(source=source))


class TransferClusterLids(commandNode.CommandNode):
    '''
    '''
    def __init__(self,name='transferLidClusters', parent=None, source="body_geo"):
        '''
        This is the constructor
        '''
        super(TransferClusterLids, self).__init__(name, parent)
        self.addAttribute('source', source, attrType='str', index=0)
        # create the command that the user can change later.
        commandAttribute = self.getAttributeByName('command')
        cmd='''
import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.libs.deformer
import rigrepo.libs.weights
import rigrepo.libs.cluster
import rigrepo.libs.curve
import rigrepo.libs.transform
source = "{source}"
temp = mc.createNode("closestPointOnMesh", name="temp")
sourceDag = rigrepo.libs.transform.getDagPath(source)
sourceDag.extendToShape()
mc.connectAttr("%s.outMesh" % (sourceDag.fullPathName()), "%s.inMesh" % (temp), f=True)
deltaMush = mc.deltaMush(source,smoothingIterations=10,smoothingStep=1.0, pinBorderVertices=True,envelope=1, foc=True)[0]
mc.setAttr(deltaMush+".displacement", 0)
for side in ['l','r']:
    mesh = "lid_%s_bindmesh" % (side)
    curve = "lid_%s_curve" % (side)
    newClusterList = list()
    newClusterList.extend(mc.ls("%s*socketStretch_%s_cluster" % (mesh,side)))
    for section in ['Upper', 'Lower']: 
        newClusterList.extend(rigrepo.libs.cluster.transferCluster(source, mesh, "blink%s_%s_cluster" % (section, side), handle=True, surfaceAssociation="closestPoint", createNew=True))
        
    for deformer in newClusterList:
        wtObj = rigrepo.libs.weights.getWeights(deformer, geometry=mesh)
        sourceWtObj = rigrepo.libs.weights.getWeights(deformer.split("__")[-1], geometry=source)
        weightList = list()
        i = 0
        weights = wtObj.getWeights()[0]
        sourceWeights = sourceWtObj.getWeights()[0]
        for wt in weights:
            j = i
            if j + 1 >= len(weights):
                break
            # get the closest point on the curve so we can use that to get the closest
            mPoint = rigrepo.libs.curve.getPointOnCurveFromPosition(curve, "%s.cp[%s]" % (mesh, j))
            mc.setAttr("%s.inPosition" % (temp), mPoint.x, mPoint.y, mPoint.z)
            vrtId = mc.getAttr("%s.closestVertexIndex" % (temp))
            wtValue = sourceWeights[vrtId]
            while i <= j + 3:
                weights[i] = wtValue
                i +=1
                
        weightList.append(weights)
        wtObj.setWeights(weightList)
        rigrepo.libs.weights.setWeights(deformer, wtObj, geometry=mesh)

mc.delete(deltaMush)
mc.delete(temp)
'''
        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        source = self.getAttributeByName("source").getValue()
        exec(self.getAttributeByName('command').getValue().format(source=source))




class TransferClusterLips(commandNode.CommandNode):
    '''
    '''
    def __init__(self,name='transferLidClusters', parent=None, source="body_geo", 
                    target='lip_bindmesh', deformerList=["lip_upper_cluster", "lip_lower_cluster"]):
        '''
        This is the constructor
        '''
        super(TransferClusterLips, self).__init__(name, parent)
        self.addAttribute('source', source, attrType='str', index=0)
        self.addAttribute('target', target, attrType='str', index=1)
        self.addAttribute('deformerList', deformerList, attrType='str', index=2)
        # create the command that the user can change later.
        commandAttribute = self.getAttributeByName('command')
        cmd='''
import maya.cmds as mc
import maya.api.OpenMaya as om
import rigrepo.libs.weights
import rigrepo.libs.cluster
import rigrepo.libs.curve
import rigrepo.libs.transform
source = "{source}"
target = "{target}"
deltaMush = mc.deltaMush(source, smoothingIterations=10,smoothingStep=1.0, pinBorderVertices=True,envelope=1, foc=True)[0]
mc.setAttr(deltaMush+".displacement", 0)
for cluster in mc.ls({deformerList}):
    newClusterList=rigrepo.libs.cluster.transferCluster(source, target, cluster, handle=True, surfaceAssociation="closestPoint", createNew=True)
    for deformer in newClusterList:
        wtObj = rigrepo.libs.weights.getWeights(deformer, geometry=target)
        sourceWtObj = rigrepo.libs.weights.getWeights(deformer.split("__")[-1], geometry=source)
        weightList = list()
        
mc.delete(deltaMush)
'''
        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        source = self.getAttributeByName("source").getValue()
        target = self.getAttributeByName("target").getValue()
        deformerList = self.getAttributeByName("deformerList").getValue()
        exec(self.getAttributeByName('command').getValue().format(source=source, 
                                                                    target=target, 
                                                                    deformerList=deformerList))



