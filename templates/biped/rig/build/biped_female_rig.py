import rigrepo.templates.biped.rig.build.biped_base_rig as biped_base_rig

class BipedFemaleRig(biped_base_rig.BipedBaseRig):
    def __init__(self,name, variant='female'):
        '''
        This is the constructor for the biped template. Here is where you will put nodes onto 
        the graph. 

        :param name: Name of the element you're using this for
        :type name: str

        :param variant: Name of the variant this template is being used for.
        :type variant: str
        '''
        
        super(BipedFemaleRig, self).__init__(name, variant)
        nodes = self.getNodes()
        face = self.getNodeByPath('|animRig|build|face')
        face.disable()
        cluster = self.getNodeByPath('|animRig|apply|deformers|cluster')
        cluster.disable()
        cluster = self.getNodeByPath('|animRig|apply|deformers|transferBlinkClusters')
        cluster.disable()
        cluster = self.getNodeByPath('|animRig|apply|deformers|transferLidsClusters')
        cluster.disable()
        worldOrient = self.getNodeByPath('|animRig|postBuild|worldOrient')
        worldOrient.enable()

