'''
This is the base module for all of your parts.
'''
import maya.cmds as mc
import rigrepo.libs.attribute as attribute
import pubs.pNode

class Part(pubs.pNode.PNode):
    '''
    '''
    def __init__(self, name):
        '''
        '''
        self.name = name
        self.trsMaster = "trs_master"
        self.trsShot = "trs_shot"
        self.trsAux = "trs_aux"
        self.rigGroup = "rig"
        self.bindGroup = "bind"
        self.modelGroup = "model"        

    def setup(self):
        '''
        '''
        parent = str()

        # iterate through the groups and create them if they don't exist yet.
        for group in [self.trsMaster, self.trsShot, self.trsAux, self.rigGroup, self.bindGroup]:
            if not mc.objExists(group):
                mc.createNode("transform", n=group)

            # check to see if there's a parent and it exist in the current scene.
            if parent and mc.objExists(parent):
                parentList = mc.listRelatives(group,p=True)
                if not parentList:
                    mc.parent(group, parent)
                elif parentList[0] != parent:
                    mc.parent(group, parent)

            parent = group

        # check to see if object exists in the scene
        if not mc.objExists(self.name):
            mc.createNode("transform", n=self.name)
        
        mc.parent(self.name, self.rigGroup)

    def build(self):
        '''
        '''
        pass

    def postBuild(self):
        '''
        '''
        # lock attributes on groups
        groupTuple = (self.name,
                    self.trsMaster,
                    self.trsShot,
                    self.trsAux,
                    self.rigGroup,
                    self.bindGroup,
                    self.modelGroup)

        attribueTuple = ('t','r','s')

        attribute.lock(groupTuple, attribueTuple)

        # set the model group to have an override on the display
        mc.addAttr(self.modelGroup, ln="overrideModel", at="bool", keyable=True, dv=1)
        mc.setAttr("{0}.overrideEnabled".format(self.modelGroup), 1)
        modelOverrideChoice = mc.createNode("choice", n="model_override_choice")
        mc.addAttr(modelOverrideChoice, ln = "on", at="byte",dv=2)
        mc.addAttr(modelOverrideChoice, ln = "off", at="byte",dv=0)
        mc.connectAttr("{0}.on".format(modelOverrideChoice),
                    "{0}.input[1]".format(modelOverrideChoice), f=True)

        mc.connectAttr("{0}.off".format(modelOverrideChoice),
                    "{0}.input[0]".format(modelOverrideChoice), f=True)

        mc.connectAttr("{0}.overrideModel".format(self.modelGroup),
            "{0}.selector".format(modelOverrideChoice), f=True)

        mc.connectAttr("{0}.output".format(modelOverrideChoice),
            "{0}.overrideDisplayType".format(self.modelGroup), f=True)

