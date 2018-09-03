'''
This is the base module for all of your parts.
'''
import maya.cmds as mc
import rigrepo.libs.attribute as attribute
import rigrepo.libs.bindmesh as bindmesh
import rigrepo.parts.part as part

class Mouth(part.Part):
    '''
    '''
    def __init__(self, name, curve, dataObj=None):
        '''
        This is the constructor for the base part
        :param name: Name of the part you are creating.
        :type name: str

        :param jointList: Name of the part you are creating.
        :type jointList: str

        :param name: Name of the part you are creating.
        :type name: str
        '''
        super(Mouth, self).__init__(name, dataObj=dataObj)

        self.addAttribute("curve", curve, attrType=str)       

    def build(self):
        '''
        '''
        super(Mouth, self).build()
        curve = self.getAttributeByName('curve').getValue()

        if not mc.objExists(curve):
            raise RuntimeError("{} doesn't exist in the currnet Maya session!".format(curve))

        # create the bindmesh
        bindmeshGeometry, follicleList = bindmesh.create(curve)

    def postBuild(self):
        '''
        '''
        super(Mouth, self).postBuild()
