
'''
This is a node for creating a new scene.
'''

import rigrepo.nodes.commandNode as commandNode

class ClusterControlNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None):
        '''
        This node is used to set the defaults. Currently it's set to use biped controls. 
        the user has the ability to make changes to it. 

        '''
        super(ClusterControlNode, self).__init__(name, parent)
        # add the attributes on the node.

        commandAttribute = self.getAttributeByName('command')

        # these are the list attributes that will be used and replaced in the command.
        self.addAttribute('displayHandle', True, attrType=bool, index=0)
        self.addAttribute('parent', 'rig', attrType=str, index=0)
        self.addAttribute('nameList', '["cluster_control"]', attrType=str, index=0)
        self.addAttribute('geometry', 'body_geo', attrType=str, index=0)


        # create the command that the user can change later.
        cmd='''
import maya.cmds as mc
import rigrepo.libs.control
import rigrepo.libs.cluster
for name in {nameList}:
    rigrepo.libs.cluster.create("{geometry}", name=name, parent="{parent}")

    # rename the cluster and control                                    
    mc.rename(name, '%s_cluster' % name)
    mc.rename('%s_ctrl' % name, name)
    mc.xform("%s_nul" % name, ws=True, matrix=mc.xform("{parent}", q=True, ws=True, matrix=True))
    if {displayHandle}:
        mc.setAttr("%s.displayHandle" % name, 1)
    rigrepo.libs.control.tagAsControl(name)
'''

        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        parent = self.getAttributeByName("parent").getValue()
        nameList = eval(self.getAttributeByName("nameList").getValue())
        geometry = self.getAttributeByName('geometry').getValue()
        displayHandle = self.getAttributeByName('displayHandle').getValue()
        exec(self.getAttributeByName('command').getValue().format(nameList=nameList,parent=parent, 
            geometry=geometry, displayHandle=displayHandle))


class FreezeWireExpressionNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None):
        '''
        This node is used to set the defaults. Currently it's set to use biped controls. 
        the user has the ability to make changes to it. 

        '''
        super(FreezeWireExpressionNode, self).__init__(name, parent)
        # add the attributes on the node.

        commandAttribute = self.getAttributeByName('command')

        # create the command that the user can change later.
        cmd="""
import maya.cmds as mc
cmd = '''import maya.cmds as mc
import rigrepo.libs.control
controlList = rigrepo.libs.control.getControls('*') or rigrepo.libs.control.getControls()
wireList = mc.ls(type="wire")
autoKeyframeState = mc.autoKeyframe(q=True, state=True)
mc.autoKeyframe(state=False)
rigrepo.libs.control.setPoseAttr(controlList, poseAttr=10) 
for wire in wireList:
    mc.setAttr("{}.freezeGeometry".format(wire), 0)

rigrepo.libs.control.toPoseAttr(controlList, 9)
for wire in wireList:
    mc.setAttr("{}.freezeGeometry".format(wire), 1)
    mc.refresh()
    
rigrepo.libs.control.toPoseAttr(controlList,10)

for ctrl in controlList:
    mc.deleteAttr("{}.poseAttr_10".format(ctrl))
    
mc.autoKeyframe(state=autoKeyframeState)
'''
mc.evalDeferred(cmd)
"""
        cmd='''
import maya.cmds as mc
mc.scriptNode(st=1, sourceType="python", bs="""{}""", n='poseFreeze')
        '''.format(cmd)
        
        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        exec(self.getAttributeByName('command').getValue())


class SwitchExpressionNode(commandNode.CommandNode):
    '''
    This node will just create a new scene. I am making it available as a command node, in-case user wants to change it.
    '''
    def __init__(self, name, parent=None):
        '''
        This node is used to set the defaults. Currently it's set to use biped controls. 
        the user has the ability to make changes to it. 

        '''
        super(SwitchExpressionNode, self).__init__(name, parent)
        # add the attributes on the node.

        # these are the list attributes that will be used and replaced in the command.
        self.addAttribute('legParamNodeList', '["leg_R", "leg_L"]', attrType=str, index=0)
        self.addAttribute('armParamNodeList', '["arm_L", "arm_R"]', attrType=str, index=0)
        self.addAttribute('elementName', 'biped', attrType=str, index=0)

        commandAttribute = self.getAttributeByName('command')

        # create the command that the user can change later.
        cmd="""
# this is the switch command that should be made into a script node
import maya.cmds as mc

def getDistanceVector(distance):
        '''
        '''
        distanceValue = max(distance, key=abs)
        index = distance.index(distanceValue)
        attr = ["x","y","z"][index]
        value = round(distance[index], 4)
        if attr == "x":
            if value < 0:
                attr = "-x"
                vector = [-1,0,0]
            else:
                vector = [1,0,0]
        elif attr == "y":
            if value < 0:
                attr = "-y"
                vector = [0,-1,0]
            else:
                vector = [0,1,0]
        elif attr == "z":
            if value < 0:
                attr = "-z"
                vector = [0,0,-1]
            else:
                vector = [0,0,1]

        return (attr, vector)

def switch(paramNode, value):
    
    mc.undoInfo(openChunk=1)
    
    namespace=""
    namespaceSplit = paramNode.split(":")

    if namespaceSplit > 1:
        namespace = ":".join(namespaceSplit[:-1]) 
        namespace = "%s:" % (namespace)

    if value == 1:
        fkControls = eval(mc.getAttr(paramNode + '.fkControls'))
        ikMatchTransforms = eval(mc.getAttr(paramNode + '.ikMatchTransforms'))
        
        aimAttr, vector= getDistanceVector(mc.getAttr("%s%s.t" % (namespace,fkControls[2]))[0])
        scaleValues = [mc.getAttr('%s%s.s%s' % (namespace,ctrl,aimAttr.strip("-"))) for ctrl in (fkControls[1],fkControls[2])]
        shoulderGimbal = "%s%s" % (namespace, fkControls.pop(1))
        wristGimbal = "%s%s" % (namespace,fkControls.pop(-1))
        rotationList = list()
        for ctrl in ikMatchTransforms:
            rotationList.append(mc.xform("%s%s" % (namespace, ctrl), q=True, ws=True, rotation=True))
        mc.setAttr("%s.pvPin" % (paramNode), 0)
        mc.setAttr("%s.twist" % (paramNode), 0)
        mc.setAttr("%s.ikfk" % (paramNode), 1)
        mc.getAttr("%s.ikfk" % (paramNode))
        mc.setAttr("%s.ikfk" % (paramNode), 1)
        mc.setAttr(wristGimbal + '.r',0, 0, 0)
        mc.setAttr(shoulderGimbal + '.r',0, 0, 0)
        
        for rotation, ctrl in zip(rotationList,fkControls):
            mc.xform("%s%s" % (namespace, ctrl), ws=True, rotation=rotation)
    
        attrList = ('stretchTop', 'stretchBottom')
        for scaleValue, attr in zip(scaleValues, attrList):
            mc.setAttr(paramNode + '.' + attr, scaleValue)
    elif value == 0:
        # get the ik controls
        ikControls = eval(mc.getAttr(paramNode + '.ikControls'))
        # get the fk transforms
        fkMatchTransforms = eval(mc.getAttr(paramNode + '.fkMatchTransforms'))
        aimAttr, vector= getDistanceVector(mc.getAttr("%s%s.t" % (namespace,fkMatchTransforms[1]))[0])
        # get the match node for the pole vector node
        matchNode = mc.getAttr(paramNode + '.pvMatch')
        # get the current distance between the joints
        currentDistance = mc.getAttr("%s%s.t%s" % (namespace, fkMatchTransforms[1], aimAttr.strip("-"))) + mc.getAttr("%s%s.t%s" % (namespace, fkMatchTransforms[2], aimAttr.strip("-")))
        #check to see if the distance in negative, which means we have to treat the matching differently
        flip = False
        if currentDistance < 0:
            flip=True
            
        newPvPos = mc.xform("%s%s" % (namespace, matchNode), q=True, ws=True, t=True)
        endJntMatrix = mc.xform("%s%s" % (namespace,fkMatchTransforms[2]), q=True, ws=True, matrix=True)
        mc.setAttr("%s.ikfk" % (paramNode), 0)
        mc.getAttr("%s.ikfk" % (paramNode))
        mc.setAttr("%s.ikfk" % (paramNode), 0)
        
        mc.xform("%s%s" % (namespace, ikControls[1]), ws=True, matrix=endJntMatrix)
        mc.xform("%s%s" % (namespace, ikControls[0]), ws=True, t=newPvPos)
        mc.setAttr("%s%s.r" % (namespace, ikControls[-1]), 0,0,0)
    mc.undoInfo(closeChunk=1)

def armSwitch(paramNode=None):
    '''
    '''
    if not paramNode:
        paramNode = mc.ls(sl=True)[0]
    
    value = mc.getAttr("%s.ikfk_switch" % (paramNode))
    print paramNode, value
    switch(paramNode, value)

def legSwitch(paramNode=None):
    '''
    '''
    paramNode = mc.ls(sl=True)[0]

    namespace=""
    namespaceSplit = paramNode.split(":")

    if len(namespaceSplit) > 1:
        namespace = ":".join(namespaceSplit[:-1]) 
        namespace = "%s:" % (namespace)

    value = mc.getAttr("%s.ikfk_switch" % (paramNode))

    if value == 1:
        fkControl = eval(mc.getAttr("%s.footFkControl" % (paramNode)))
        fkControlPos = mc.xform("%s%s" % (namespace, fkControl), q=True, ws=True, matrix=True)
        switch(paramNode, value)
        mc.xform("%s%s" % (namespace, fkControl), ws=True, matrix=fkControlPos)
    elif value == 0:
        ikControls = eval(mc.getAttr(paramNode + '.ikControls'))

        switch(paramNode, value)
    
topNodeList = mc.ls(["*{elementName}", "*:{elementName}"])  
# kill the jobs first
legParamNodeList = {legParamNodeList}
armParamNodeList = {armParamNodeList}
paramNodeList =  legParamNodeList + armParamNodeList
for job in mc.scriptJob(lj=True):
    jobSplit = job.split()
    for node in topNodeList:
        nameSplit = node.split(":")
        name = nameSplit[0]
        for paramNode in paramNodeList:
            jobNameList = ['%s"' % ("%s:%s.ikfk_switch" % (name, paramNode)),
                           '%s.ikfk_switch' % (paramNode),
                           ]
            for jobName in jobNameList:
                for job in jobSplit:
                    if jobName in job:
                        print "deleting job---->", jobName
                        mc.scriptJob(k=int(jobSplit[0].split(":")[0]))    
                        break

for node in topNodeList:
    nameSplit = node.split(":")
    lenSplit = len(nameSplit)
    for paramNode in paramNodeList:
        if lenSplit > 1:
            name = nameSplit[0]
            print "making job---->", "%s:%s.ikfk_switch" % (name, paramNode)
            if paramNode in legParamNodeList:
                mc.scriptJob(attributeChange=["%s:%s.ikfk_switch" % (name, paramNode), legSwitch])            
            elif paramNode in armParamNodeList:
                mc.scriptJob(attributeChange=["%s:%s.ikfk_switch" % (name, paramNode), armSwitch])                            
        else:
            print "making job---->", "%s.ikfk_switch" % (paramNode)
            if paramNode in legParamNodeList:
                mc.scriptJob(attributeChange=["%s.ikfk_switch" % (paramNode), legSwitch])            
            elif paramNode in armParamNodeList:
                mc.scriptJob(attributeChange=["%s.ikfk_switch" % (paramNode), armSwitch])            
"""
        cmd='''
import maya.cmds as mc
scriptNode = mc.scriptNode(st=1, sourceType="python", bs="""{}""", n='ikfkSwitch')
mc.scriptNode(scriptNode, eb=True)
        '''.format(cmd)
        
        # set the command to the attributes value
        commandAttribute.setValue(cmd)

    def execute(self, *args, **kwargs):
        '''
        Here is where the code will run for this node.
        '''
        # get the attributes that were set by the user so we can pass it to the command.
        elementName = self.getAttributeByName('elementName').getValue()
        legParamNodeList = eval(self.getAttributeByName('legParamNodeList').getValue())
        armParamNodeList = eval(self.getAttributeByName('armParamNodeList').getValue())
        exec(self.getAttributeByName('command').getValue().format(elementName=elementName, legParamNodeList=legParamNodeList, armParamNodeList=armParamNodeList))
