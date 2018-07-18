
'''
This is a node for creating a new scene.
'''

import rigrepo.nodes.commandNode as commandNode

class LoadWtsDirNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, 
    in-case user wants to change it.
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp"):
        super(LoadWtsDirNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('dirPath', dirPath, attrType='dir', index=0)
        # command 
        cmd='import rigrepo.libs.weights\n\
import os\n\
if os.path.isdir("{dirPath}"):\n\t\
    for filename in os.listdir("{dirPath}"):\n\t\t\
        filepath = os.path.join(dirPath, filename)\n\t\t\
        fileSplit = filename.split("__")\n\t\t\
        geo = fileSplit[0]\n\t\t\
        deformer = fileSplit[1].split(".")[0]\n\t\t\
        print geo, deformer\n\t\t\
        rigrepo.libs.weights.importWeights(geo, deformer, filepath)'
        
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        dirPath = self.getAttributeByName("dirPath").getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath))
        

        