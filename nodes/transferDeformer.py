
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

