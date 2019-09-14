'''
This is a node for importing animation
'''

import rigrepo.nodes.commandNode as commandNode

class ImportAnimationNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None, filePath='temp', remapFile=""):
        super(ImportAnimationNode, self).__init__(name, parent)
        commandAttribute = self.getAttributeByName('command')
        self.addAttribute('remapFile', remapFile, attrType='file', index=0)
        self.addAttribute('filePath', filePath, attrType='file', index=0)
        cmd='''
import maya.cmds as mc
import os
import traceback
import maya.mel as mm
import rigrepo.libs.control

mc.undoInfo(openChunk=1)
try:
    if not mc.pluginInfo('atomImportExport', q=1, l=1):  
        mc.loadPlugin('atomImportExport')

    if os.path.isfile("{filePath}"):

        # Get start and end frame
        startTime = None
        endTime = None
        with open("{filePath}") as f:
            for line in f:
                if line.startswith('startTime'):
                    startTime = line.split()[1][:-1]
                if line.startswith('endTime'):
                    endTime = line.split()[1][:-1]
                    break
        f.close()
                
        # This stupid atom plugin only works on selection
        controls = rigrepo.libs.control.getControls()
        if controls:
            mc.select(controls)
            
        # Clear existing anim 
        mc.cutKey(controls, s=True)
        
        # Set timeline to fit animation
        mc.playbackOptions(min=float(startTime), max=float(endTime))
            
        mm.eval("file -import -type \\"atomImport\\" -ra true -namespace \\"body_calisthenics_1\\" -options \\";;targetTime=1;srcTime=1:"+endTime+";dstTime=1:"+endTime+";option=scaleInsert;match=mapFile;;selected=;search=;replace=;prefix=;suffix=;mapFile={remapFile};\\" \\"{filePath}\\";")
        
except:
    traceback.print_exc()
mc.undoInfo(closeChunk=1)

 '''
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        filePath = self.getAttributeByName("filePath").getValue()
        remapFile = self.getAttributeByName("remapFile").getValue()
        exec(self.getAttributeByName('command').getValue().format(remapFile=remapFile, filePath=filePath))
        
