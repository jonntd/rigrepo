'''
/////////////////////////////////////////////////
//                        //
//    skinData            //
//                        //
/////////////////////////////////////////////////

:author: Walt Yoder
:since: 12/5/2013

:summary:
    Scripted command used to query and set weights on a mesh that has a skinCluster 
    connected to it. It can also query influence objects attached to the skinCluster.

:usage:
    Get weights:
    Will get the weights on a skinCluster for a particular mesh or skinCluster.

    Set weights:
    Will set the weights on a skinCluster for a particular mesh or skinCluster.

:scripting:
    If you want to use this command in a script please note the flag options below.

    -vertex or -vtx
    This specifies the vertices you would like to apply you weights too
    :attention: Only works in command mode

    -influence or -inf
    Specifies the influence objects you wish to apply the weights for or query.
    :attention: Only working in command and Query modes

    -weights or -wts
    Specifies the weight values you would like to apply.
    :attention: Only working in command and Query modes
    
    -blendWeight or -bwt
    Specifies the blend weight values you would like to query or apply.
    :attention: Only working in command and Query modes

:example:
    :Mel:
        >>> skinData -wts .5 -wts .2 -inf "joint1" -vrt "pPlane1.vtx[3]" -vtx "pPlane1.vtx[5]" "pPlane1";
        >>> skinData -q -wts "pPlane1"
        >>> skinData -q -inf pPlane1"
    .. python:
        >>> from maya import cmds
        >>> cmds.skinData('pPlane1', wts = (0.2, 0.3), vtx = ("pPlane1.vtx[3]",pPlane1.vtx[5]"), inf = 'joint1')
        >>> cmds.skinData('pPlane1', q = True, wts = True)
        
        
.. todo: Get the command working with multiple influences when assigning weights
'''

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaAnim as OpenMayaAnim
import sys

class SkinDataCmd(OpenMayaMPx.MPxCommand):
    kCmdName = "skinData"
    kInfluenceFlag = '-inf'
    kInfluenceLongFlag = '-influence'
    kWeightsFlag = '-wts'
    kWeightsLongFlag = '-weights'
    kVertIdFlag = '-vtx'
    kVertIdLongFlag = '-vertex'
    kBlendWeightsFlag = '-bwt'
    kBlendWeightsLongFlag = '-blendWeight'
    
    def __init__(self):
        super(SkinDataCmd, self).__init__()
        self.__mesh            = str()
        self.__mObject         = OpenMaya.MObject()
        self.__mDagPath        = OpenMaya.MDagPath()
        self.__mSelList        = OpenMaya.MSelectionList()
        self.__mVertSelList    = OpenMaya.MSelectionList()
        self.__influenceNames  = list()
        self.__weights         = OpenMaya.MDoubleArray()
        self.__blendWeights    = OpenMaya.MDoubleArray()
        self.__oldWeights      = OpenMaya.MDoubleArray()
        self.__oldBlendWeights = OpenMaya.MDoubleArray()
        
        #set/return variables
        self.__returnWeights          = False
        self.__returnBlendWeights     = False
        self.__returnInfluenceWeights = False
        self.__returnInfluence        = False
        self.__undoable               = False
        self.__setVertWeights         = False
        self.__setVertBlendWeights    = False

    
    def doIt(self, args):
        # Create the node
        self.parseArguments(args)
        return self.redoIt()
    
    def parseArguments(self, args):
        ''' 
        The presence of this function is not enforced,
        but helps separate argument parsing code from other
        command code.
        '''
        # Getting the argData from MArgParser
        argData = OpenMaya.MArgDatabase( self.syntax(), args )
        try:
            self.__mesh = argData.commandArgumentString( 0 )
        except:
            self.displayError('Must pass in Mesh as first Argument')         
        if argData.isQuery() and argData.isFlagSet( SkinDataCmd.kWeightsFlag ) and argData.isFlagSet( SkinDataCmd.kInfluenceFlag ):
            try:
                self._influnceNode = argData.commandArgumentString( 1 )
            except:
                pass
            self.__returnWeights = True
            self.__returnInfluenceWeights = True
            self.__undoable = False
        elif argData.isQuery() and argData.isFlagSet( SkinDataCmd.kInfluenceFlag ):
            self.__returnInfluence = True
            self.__undoable = False
        elif argData.isQuery() and argData.isFlagSet( SkinDataCmd.kWeightsFlag ):
            self.__returnWeights = True
            self.__undoable = False
        elif argData.isQuery() and argData.isFlagSet( SkinDataCmd.kBlendWeightsFlag ):
            self.__returnBlendWeights = True
            self.__undoable = False
        elif argData.isFlagSet( SkinDataCmd.kWeightsFlag ) and argData.isFlagSet( SkinDataCmd.kInfluenceFlag):
            #add to doubleArray for weights
            self.__weights.setLength(argData.numberOfFlagUses(SkinDataCmd.kWeightsFlag))
            for i in range(self.__weights.length()):
                argList = OpenMaya.MArgList()
                argData.getFlagArgumentList(SkinDataCmd.kWeightsFlag,i, argList)
                self.__weights.set(argList.asDouble(0),i)
            #add to selectionList for verts
            if argData.isFlagSet( SkinDataCmd.kVertIdFlag ):
                for i in range(argData.numberOfFlagUses(SkinDataCmd.kVertIdFlag)):
                    argList = OpenMaya.MArgList()
                    argData.getFlagArgumentList(SkinDataCmd.kVertIdFlag, i, argList)
                    self.__mVertSelList.add(argList.asString(0), i)
            #append to list of influence names
            for i in range(argData.numberOfFlagUses(SkinDataCmd.kInfluenceFlag)):
                argList = OpenMaya.MArgList()
                argData.getFlagArgumentList(SkinDataCmd.kInfluenceFlag, i, argList)
                self.__influenceNames.append(argList.asString(0))
            self.__setVertWeights = True
            self.__undoable = True
        elif argData.isFlagSet( SkinDataCmd.kBlendWeightsFlag ):
            #add to doubleArray for weights
            self.__blendWeights.setLength(argData.numberOfFlagUses(SkinDataCmd.kBlendWeightsFlag))
            for i in range(self.__blendWeights.length()):
                argList = OpenMaya.MArgList()
                argData.getFlagArgumentList(SkinDataCmd.kBlendWeightsFlag,i, argList)
                self.__blendWeights.set(argList.asDouble(0),i)
            
            self.__setVertBlendWeights = True
            self.__undoable = True
        else:
            self.displayError('No arguments passed')

            
    def redoIt(self):
        '''
        Get weights on mesh from skinCluster deformer passed in and return dictionary
        with all data stored.
        '''
        mSkinClsObject = self.__getSkinClusterObject(self.__mesh)
        
        #get the skincluster object
        self.__mFnScls = OpenMayaAnim.MFnSkinCluster(mSkinClsObject)
        
        #check which operation we want to return to the user
        if self.__returnWeights or self.__returnBlendWeights or self.__setBlendWeights:
            dagPath, components = self.__getComponents()
        
        if self.__returnWeights:
            influence = None
            if self.__returnInfluenceWeights:
                influence = self._influnceNode
            weights = self.__getWeights(dagPath, components, influence)
            self.setResult(weights)
            self.getCurrentResult(OpenMaya.MDoubleArray())
        elif self.__returnBlendWeights:
            weights = self.__getBlendWeights(dagPath, components)
            self.setResult(weights)
            self.getCurrentResult(OpenMaya.MDoubleArray())
        elif self.__returnInfluence:
            influenceNames = self.__getInfluences()
            self.setResult(influenceNames)
            self.getCurrentResult(list())
        elif self.__setVertWeights:
            self.__setWeights(self.__weights, self.__influenceNames, True)
        elif self.__setVertBlendWeights:
            self.__setBlendWeights(dagPath, components, self.__blendWeights)


    def undoIt(self):
        if self.__setVertWeights:
            self.__setWeights(self.__oldWeights, self.__getInfluences(), False)
        elif self.__setVertBlendWeights:
            dagPath, components = self.__getComponents()
            self.__setBlendWeights(dagPath, components, self.__oldBlendWeights)
            
    def isUndoable(self):
        ''' This function indicates whether or not the command is undoable. If the
        command is undoable, each executed instance of that command is added to the
        undo queue. '''
        
        # We must return True to specify that this command is undoable.
        return self.__undoable
    
    
    #--------------------------------------------------------------------
    #GATHER DATA METHODS
    #--------------------------------------------------------------------

    def __getSkinClusterObject(self, mesh):
        '''
        Gets the deformer object on the given mesh. If no mesh is passed in,
        by default we will get active selection from you Maya scene

        :param mesh: Polygonal mesh you wish to get skincluster from
        :type mesh: *str* or *unicode*
        
        :return: Returns an MObject for the skinCluster attached to given mesh.
        :rtype: *MObject* or *None*
        
        '''
        self.__mSelList.add(self.__mesh)
        self.__mSelList.getDependNode(0, self.__mObject)
        
        if self.__mObject.hasFn(OpenMaya.MFn.kSkinClusterFilter):
            return self.__mObject
        
        self.__mSelList.getDagPath(0, self.__mDagPath)
        
        #check the object
        if not self.__mObject.hasFn(OpenMaya.MFn.kMesh) and self.__mObject.hasFn(OpenMaya.MFn.kTransform):
            dagFn = OpenMaya.MFnDagNode(self.__mDagPath)
            childCount = dagFn.childCount()
            for index in range(0,childCount):
                child = dagFn.child(index)
                if child.hasFn(OpenMaya.MFn.kMesh):
                    self.__mObject = OpenMaya.MObject(child)
                    break
                
        graphIter = OpenMaya.MItDependencyGraph(self.__mObject, OpenMaya.MItDependencyGraph.kDownstream, OpenMaya.MItDependencyGraph.kPlugLevel)
        
        while not graphIter.isDone():
            currentItem = graphIter.currentItem()
            if currentItem.hasFn(OpenMaya.MFn.kSkinClusterFilter):
                return currentItem
            graphIter.next()  

        
        return None 
    
    def __getComponents(self):
        '''
        Gets and returns the DagPath to the mesh and the components of the mesh
        '''
        fnSet = OpenMaya.MFnSet(self.__mFnScls.deformerSet())
        members = OpenMaya.MSelectionList()
        fnSet.getMembers(members, False)
        dagPath = OpenMaya.MDagPath()
        components = OpenMaya.MObject()
        members.getDagPath(0, dagPath, components)
        
        return dagPath, components
    
    def __getWeights(self, dagPath, components, influence = None):
        '''
        Gets the weights from on the mesh
        
        :param dagPath: DagPath to the mesh
        :type dagPaht: *OpenMaya.MDagPath*
        
        :param components: Object pointing to the Components (i.e. Vertices)
        :type components: *OpenMaya.MObject*
        
        :param influence: Name of the influence being queried
        :type influence: *str* or *unicode* 
        '''
        weights = OpenMaya.MDoubleArray()
        util = OpenMaya.MScriptUtil()
        util.createFromInt(0)
        pUInt = util.asUintPtr()
        if influence:
            influenceNames = self.__getInfluences()
            index = influenceNames.index(influence)
            self.__mFnScls.getWeights(dagPath,components, index, weights)
        else:
            self.__mFnScls.getWeights(dagPath, components, weights, pUInt)
        
        return weights
        
    def __getBlendWeights(self, dagPath, components):
        weights = OpenMaya.MDoubleArray()
        self.__mFnScls.getBlendWeights(dagPath, components, weights)
        
        return weights
    
    def __getInfluences(self):
        '''
        Gets and returns all the influence objects on the skinCluster
        '''
        # Influences & Influence count
        influences= OpenMaya.MDagPathArray()
        infCount = self.__mFnScls.influenceObjects(influences)
        # Get node names for influences
        influenceNames = [influences[i].partialPathName() for i in range(infCount)]
        
        return influenceNames


    #--------------------------------------------------------------------
    #SET DATA METHODS
    #--------------------------------------------------------------------
    def __setWeights(self, weights, influences, getOldWeights = False):
        #Create MObject and MDagPath
        if self.__mVertSelList.length() != 0:
            mComponentsObject = OpenMaya.MObject()
            mComponentsDagPath = OpenMaya.MDagPath()
            self.__mVertSelList.getDagPath(0, mComponentsDagPath, mComponentsObject) #assigns first index in the list to MDagPath
        else:
            mComponentsDagPath,mComponentsObject = self.__getComponents()
        
        
        if mComponentsObject.apiType() != OpenMaya.MFn.kMeshVertComponent:
            raise TypeError('Selection must Vertices on a mesh')
        
        #Get node names for influences
        influenceObjects = self.__getInfluences()
        influenceIndices = OpenMaya.MIntArray()
        influenceIndices.setLength(len(influences))
        
        for i,inf in enumerate(influences):
            index = influenceObjects.index(inf)
            influenceIndices.set(index, i)

        if getOldWeights:
            #get the old weights so we can reapply them when we undo.
            #self.__oldWeights = self.__getWeights(self.__mDagPath, mComponentsObject)
            self.__mFnScls.setWeights(mComponentsDagPath, mComponentsObject, influenceIndices, weights, True,self.__oldWeights)
        else:
            self.__mFnScls.setWeights(mComponentsDagPath, mComponentsObject, influenceIndices, weights, True)
            
            
    def __setBlendWeights(self, dagPath, components, weights):
        self.__oldBlendWeights = self.__getBlendWeights(dagPath, components)
        self.__mFnScls.setBlendWeights(dagPath, components, weights)



    #--------------------------------------------------------------------
    #CREATOR METHODS
    #--------------------------------------------------------------------
    @classmethod
    def cmdCreator(cls):
        return OpenMayaMPx.asMPxPtr(cls())

    @classmethod
    def cmdSyntaxCreator(cls):
        ''' Defines the argument and flag syntax for this command. '''
        syntax = OpenMaya.MSyntax()
        syntax.addArg( OpenMaya.MSyntax.kString )
        syntax.addArg( OpenMaya.MSyntax.kString )
        syntax.addFlag( cls.kInfluenceFlag, cls.kInfluenceLongFlag, OpenMaya.MSyntax.kString)
        syntax.addFlag( cls.kWeightsFlag, cls.kWeightsLongFlag, OpenMaya.MSyntax.kDouble )
        syntax.addFlag( cls.kVertIdFlag, cls.kVertIdLongFlag, OpenMaya.MSyntax.kString  )
        syntax.addFlag( cls.kBlendWeightsFlag, cls.kBlendWeightsLongFlag, OpenMaya.MSyntax.kDouble)
        syntax.makeFlagMultiUse(cls.kWeightsFlag)
        syntax.makeFlagMultiUse(cls.kVertIdFlag)
        syntax.makeFlagMultiUse(cls.kInfluenceFlag)
        syntax.makeFlagMultiUse(cls.kBlendWeightsFlag)
        syntax.enableQuery(True)
        syntax.enableEdit(True)
            
        return syntax


# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Magic Leap - Walt Yoder", "1.0", "Any")
    try:
        mplugin.registerCommand(SkinDataCmd.kCmdName, SkinDataCmd.cmdCreator, SkinDataCmd.cmdSyntaxCreator)
    except:
        sys.stderr.write("Failed to register command: %s" % SkinDataCmd.kCmdName)
        raise


# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(SkinDataCmd.kCmdName)
    except:
        sys.stderr.write("Failed to deregister command: %s" % SkinDataCmd.kCmdName)
        raise