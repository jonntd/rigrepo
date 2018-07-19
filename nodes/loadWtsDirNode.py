
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
rigrepo.libs.weights.applyWtsDir("{dirPath}")'
        
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        dirPath = self.getAttributeByName("dirPath").getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath))
        

        