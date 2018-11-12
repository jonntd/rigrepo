import maya.cmds as mc
import rigrepo.libs.common
import os
import maya.api.OpenMaya as om
import xml.etree.ElementTree as et

def setWeights(node, weights, map=None): 
    '''
    Sets weights for specified deformers.

    :param node: Deformer name
    :type node: str

    :param weights: List of tuples. [(pntIndex, value),...]
    :type weights: List

    :param map: Name of influence or deformer map to assing weights to.
    :type map: str

    :return: None
    '''

    if mc.nodeType(node) == 'skinCluster': 
        # find the inf index 
        inf = map
        infIndex = None 
        con = mc.listConnections(inf+'.worldMatrix[0]', p=1, d=1, s=0) 
        for c in con: 
            if node+'.matrix' in c: 
                infIndex = c.split('[')[1][:-1] 
        if infIndex:
            for weight in weights: 
                pntIndex,value = weight
                mc.setAttr(node+'.wl['+pntIndex+'].w['+infIndex+']', value) 

    if mc.nodeType(node) == 'cluster': 
        for w in weights: 
            pntIndex,value = weight
            mc.setAttr(node+'.wl[0].w['+pntIndex+']', value) 

def getWeights(node, map=None):
    '''
    Gets weights for specified deformers.

    :param node: Deformer name
    :type node: str
    :param weights: List of tuples. [(pntIndex, value),...]
    :type weights: List
    :param map: Name of influence or deformer map to assing weights to.
    :type map: str
    :returns: None
    '''

    if mc.nodeType(node) == 'skinCluster': 
        # find the inf index 
        inf = map
        infIndex = None 
        con = mc.listConnections(inf+'.worldMatrix[0]', p=1, d=1, s=0) 
        for c in con: 
            if node+'.matrix' in c: 
                infIndex = c.split('[')[1][:-1] 
        if infIndex:
            for weight in weights: 
                pntIndex,value = weight
                mc.getAttr(node+'.wl['+pntIndex+'].w['+infIndex+']', value) 

    if mc.nodeType(node) == 'cluster': 
        for w in weights: 
            pntIndex,value = weight
            mc.setAttr(node+'.wl[0].w['+pntIndex+']', value) 

def exportWeights(geometry, deformer, directory):
    '''
    This will export weights for the given deformer into the given directory.
    If the directory doesn't exists. It will create the full path. 

    .. example::
        exportWeights("body_geo",
            "body_geo_skinCluster",
            "shows/template/collections/rigrepo/templates/biped/rig/build/base/skin_wts")

        exportWeights(["body_geo",eye_l_geo],
            "cluster1",
            "shows/template/collections/rigrepo/templates/biped/rig/build/base/cluster_wts")

    .. note:: 
        This is setup to export to only one directory. So typically you will only
        want to export deformers of the same type to the same directory
    
    :param geometry: The geometry(s) you wish to export the weights for.
    :type geometry: str | list
    
    :param deformer: This is the deforemr(s) you wish to export
    :type deformer: str | list

    :param directory: The directory you wish to store the deformers passed. 
    :type directory: str
    '''
    # importing pubs.ui so we can get the maya main window widget.
    import pubs.ui
    from PySide2 import QtWidgets
    # make sure that we have a list for the rest of the function to work properly
    geoList = rigrepo.libs.common.toList(geometry)
    deformerList = rigrepo.libs.common.toList(deformer)
    
    # check to make sure the directory exists. If it doesn't we will create the directory.
    if not os.path.isdir(directory):
        msg = 'The following directory does not exist: {}\n\
        Do you wish to create it so you can export the deformers?'.format(directory)
        reply = QtWidgets.QMessageBox.question(pubs.ui.getMayaWindow(),
                                                'Create directory dialog',
                                                msg,
                                                QtWidgets.QMessageBox.Yes, 
                                                QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            os.makedirs(directory, 755)
        else:
            print "since there is not a directory, we cannot export the deformers."
            return
        
    
    # here we will loop through all of the the deformers and geometry and export the files
    # to the given directory.
    for deformer in deformerList:
        for geo in geoList:
            # adding the geometry to a selection list so I can extend to the shape
            # reliably with out any issues.
            selList = om.MSelectionList()
            selList.add(geo)
            dagPath = selList.getDagPath(0)
            dagPath.extendToShape()
            # once we have the correct shape. Now we will check it against the other shapes 
            # that the given deformer is influencing.
            shapes = mc.deformer(deformer, q=True,g=True)
            geoShape = dagPath.partialPathName()
            
            # get the difference between the deformer and the deformers influenced by
            if geoShape in shapes:
                skipGeo = ";".join(list(set(shapes).difference(set([geoShape]))))

            # this is where we will export the weights.
            mc.deformerWeights("{}__{}.xml".format(geo, deformer), 
                                skip=skipGeo, 
                                export=True, 
                                deformer=deformer,
                                path=directory)

def importWeights(geometry, deformer, filepath):
    '''
    This will import weights for the given deformer into the given directory.

    .. example::
        importWeights("body_geo",
            "cluster1",
            "shows/template/collections/rigrepo/templates/biped/rig/build/base/cluster_wts/body_geo__cluster1.xml)

    .. note::
        This is setup to import only one file at a time. We should write something that imports
        multiple files in a directory
    
    :param geometry: The geometry(s) you wish to import the weights for.
    :type geometry: str
    
    :param deformer: This is the deforemr(s) you wish to import weights onto
    :type deformer: str

    :param filepath: The filepath you want to use for the weights.
    :type filepath: str
    '''
    if not os.path.isfile(filepath):
        raise RuntimeError("{} is not an existing filepath.".format(filepath))

    # split up the path so we can pass the file name and directory in seperately
    filename = os.path.basename(filepath)
    directory = os.path.dirname(filepath)

    # adding the geometry to a selection list so I can extend to the shape
    # reliably with out any issues.
    selList = om.MSelectionList()
    selList.add(geometry)
    dagPath = selList.getDagPath(0)
    dagPath.extendToShape()
    # once we have the correct shape. Now we will check it against the other shapes 
    # that the given deformer is influencing.
    shapes = mc.deformer(deformer, q=True,g=True)
    geoShape = dagPath.partialPathName()
    
    # get the difference between the deformer and the deformers influenced by
    if geoShape in shapes:
        skipGeo = ";".join(list(set(shapes).difference(set([geoShape]))))

    #import the weights for the given deformer and filepath
    mc.deformerWeights(filename, im=True, deformer=deformer, skip=skipGeo, path=directory)


def applyWtsDir(directory):
    '''
    This function will take a directory with properly named weight files,
    i.e.(geometryName__deformerName.xml), and apply them if both the deformer and geometry
    are in the current scene.

    .. TODO::
        We need to make sure we create the other deformers if they don't exist. Currently We're only
        creating skinClusters.

    If the deformers isn't in the scene but the geometry is, we will create the deformer for you.

    :param directory: Directory path with weight files inside of it.
    :type directory: str
    '''
    # Check to see if the directory past into this function exists.
    if os.path.isdir(directory):
        # loop through all of the files in the directory and make sure they're weights files.
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            fileSplit = filename.split("__")
            # get the geometry, deformer, and deformerType from the file name.
            geometry = fileSplit[0]
            deformer = fileSplit[1].split(".")[0]
            deformerType = deformer.split("_")[-1]
            # Continue if the geo doesn't exist
            if not mc.objExists(geometry):
                print('Loading {}: Geometry [ {} ] does not exist'.format(deformer, geometry))
                continue
            # if the deformer doesn't exist, then we will create it.
            if not mc.objExists(deformer):
                tree = et.parse(filepath)
                root = tree.getroot()
                # create skinCluster deformer if it doesn't exist in the current session.
                if deformerType == "skinCluster":
                    jointList = [wts.get('source') for wts in root.findall('weights')]
                    jointListExists = mc.ls(jointList)
                    jointListMissing = list(set(jointList) - set(jointListExists))
                    if jointListMissing:
                        print('Loading {}: Missing joints [ {} ]'.format(deformer, jointListMissing))
                    if not jointListExists:
                        print('No joints could be fournd for [ {} ]'.format(deformer))
                        continue
                    sc = mc.skinCluster(jointListExists, geometry, name=deformer, tsb=1)[0]
                    # Set to dual quaternion mode
                    mc.setAttr(sc+'.skinningMethod', 1)

            # apply the weights
            if not mc.objExists(deformer):
                print('skinCluster does not exist [ {} ]'.format(deformer))
                continue
            rigrepo.libs.weights.importWeights(geometry, deformer, filepath)
            # this ensures that our skinCluster is normalized. 
            if deformerType == "skinCluster":
                mc.skinCluster(deformer, e=True, fnw=True)
