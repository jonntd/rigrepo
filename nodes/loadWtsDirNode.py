
'''
This is a node for creating a new scene.
'''

import rigrepo.nodes.commandNode as commandNode

class LoadWtsDirNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, 
    in-case user wants to change it.
    '''
    def __init__(self, name, parent=None, dirPath="/disk1/temp", includeFilter='',
                 excludeFilter=''):
        super(LoadWtsDirNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('dirPath', dirPath, attrType='dir', index=0)
        self.addAttribute('includeFilter', includeFilter, attrType='str')
        self.addAttribute('excludeFilter', excludeFilter, attrType='str')
        # command
        cmd = '''
import rigrepo.libs.weights
rigrepo.libs.weights.applyWtsDir("{dirPath}", includeFilter="{includeFilter}", excludeFilter="{excludeFilter}")
'''
        
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        dirPath = self.getAttributeByName("dirPath").getValue()
        includeFilter = self.getAttributeByName("includeFilter").getValue()
        excludeFilter = self.getAttributeByName("excludeFilter").getValue()
        exec(self.getAttributeByName('command').getValue().format(dirPath=dirPath,
                                                                  includeFilter=includeFilter,
                                                                  excludeFilter=excludeFilter))
        

        