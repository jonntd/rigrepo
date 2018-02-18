'''
This is the base data node 
'''
import pubs.pNode

class DataNode(pubs.pNode.PNode):
    def __init__(self, file, type):
        super(CommandNode, self).__init__(file, type)
        
        self.addAttribute("file", 'File path to data', attrType = "filePath")
    
    def execute(self, **kwargs):
        pass
