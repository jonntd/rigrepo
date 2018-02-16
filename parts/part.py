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
        This is the constructor for the base part
        :param name: Name of the part you are creating.
        :type name: str
        '''
        super(Part, self).__init__(name)
        # self._name exists in pObject. Be sure to reference that if you're 
        # trying to figure out where self._name is coming from.
        self.name = self._name
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

        groupList = [self.trsMaster, self.trsShot, self.trsAux, 
                    self.modelGroup, self.rigGroup, self.bindGroup]
        # iterate through the groups and create them if they don't exist yet.
        for group in groupList:
            if not mc.objExists(group):
                mc.createNode("transform", n=group)

            # check to see if there's a parent and it exist in the current scene.
            if parent and mc.objExists(parent):
                parentList = mc.listRelatives(group,p=True)
                if not parentList:
                    mc.parent(group, parent)
                elif parentList[0] != parent:
                    mc.parent(group, parent)

            if group == groupList[3]:
                continue
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
        if not mc.objExists("{}.overrideModel".format(self.modelGroup)):
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


    def execute(self, *args, **kwargs):
        '''
        '''
        self.setup()
        self.build()
        self.postBuild()