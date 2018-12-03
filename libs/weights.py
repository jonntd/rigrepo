'''
This will deal with getting, setting, importing, exporting weights.
'''
import maya.cmds as mc
import maya.api.OpenMaya as om
# using this one for the MItGeometry 
import maya.OpenMaya as OpenMaya

import os
import xml.etree.ElementTree as et
import numpy

import rigrepo.libs.common
import rigrepo.libs.weightObject
import rigrepo.libs.transform

def setWeights(deformer, weights, mapList=None, geometry=None): 
    '''
    Sets weights for specified deformers.

    :param deformer: Deformer name
    :type deformer: str

    :param weights: WeightObject or list of numpy arrays or tuples or lists
    :type weights: WeightObject | list | tuple

    :param map: Name of influence or deformer map to assing weights to.
    :type map: str | list

    :return: None
    '''
    # make sure we have the mapList
    if isinstance(mapList, basestring):
        mapList = rigrepo.libs.common.toList(mapList)
    elif mapList == None:
        mapList = getMaps(deformer)

    if geometry:
        if not mc.objExists(geometry):
            raise RuntimeError("{} doesn't exists in the current Maya session!".format(geometry))
        # make sure we have the shape of the geometry for all deformers except the skinCluster
        geoDagPath = rigrepo.libs.transform.getDagPath(geometry)
        geoDagPath.extendToShape()

    # make sure we have the correct weights for what we're going to set.
    if isinstance(weights, (list, tuple)):
        weightList = [numpy.array(weights)]
    elif isinstance(weights, numpy.ndarray):
        weightList = [weights]
    elif isinstance(weights, rigrepo.libs.weightObject.WeightObject):
        weightList = weights.getWeights()

    if mc.nodeType(deformer) == 'skinCluster': 
        # iterate through the mesh and set the values on each point
        for mapIndex, inf in enumerate(mapList):
            # find the inf index 
            infIndex = None 
            con = mc.listConnections(inf+'.worldMatrix[0]', p=True, d=True, s=False) 
            for c in con: 
                if deformer+'.matrix' in c: 
                    infIndex = c.split('[')[1][:-1] 
            if infIndex:
                for pntIndex, value in enumerate(weightList[mapIndex]):
                    mc.setAttr('{}.wl[{}].w[{}]'.format(deformer, pntIndex, infIndex), value) 

    if mc.nodeType(deformer) == 'cluster': 
        geometryindex = 0
        if geometry:
            geometryindex = mc.cluster(deformer,q=True, geometry=True).index(geoDagPath.partialPathName())
        for pntIndex, value in enumerate(weightList[0]):
            mc.setAttr('{}.wl[{}].w[{}]'.format(deformer, geometryindex, pntIndex), value) 

def getWeights(deformer, mapList=None):
    '''
    Gets weights for specified deformers.

    :param deformer: Deformer name
    :type deformer: str
    :param map: Name of influence or deformer map to assing weights to.
    :type map: str | list
    :returns: Returns a weight object that you are able to use or manipulate.
    :rtype: WeightObject
    '''
    weightList = list()
    # make sure there is a mapList
    if not mapList:
        mapList = getMaps(deformer)
    elif not isinstance(mapList, (list, tuple)):
        rigrepo.libs.common.toList(mapList)
    # get the geometry and the iterator to use for looping through the mesh points for wts.
    geometry = mc.deformer(deformer, q=True, g=True)[0]
    selList = OpenMaya.MSelectionList()
    selList.add(geometry)
    dagPath = OpenMaya.MDagPath()
    selList.getDagPath(0, dagPath)
    geoIterator = OpenMaya.MItGeometry(dagPath)
    weightList = [numpy.array([]) for map_ in mapList]

    if mc.nodeType(deformer) == 'skinCluster': 
        # iterate over the geometry
        while not geoIterator.isDone():
            # find the inf index 
            for inf in mapList:
                # get the connections so we can get to the weight list
                infIndex = None 
                con = mc.listConnections('{}.worldMatrix[0]'.format(inf), p=True, d=True, s=False) 
                for c in con: 
                    if deformer+'.matrix' in c: 
                        infIndex = c.split('[')[1][:-1] 
                if infIndex:
                    weightList[mapList.index(inf)] = numpy.append(weightList[mapList.index(inf)], numpy.array(round(mc.getAttr('{}.wl[{}].w[{}]'.format(deformer, geoIterator.index(), infIndex)), 4)))
            geoIterator.next()

    if mc.nodeType(deformer) == 'cluster': 
        # iterate over the geometry
        while not geoIterator.isDone():
            weightList[0] = numpy.append(weightList[0], numpy.array(round(round(mc.getAttr('{}.wl[0].w[{}]'.format(deformer, geoIterator.index())), 4))))

    return rigrepo.libs.weightObject.WeightObject(maps=mapList, weights=weightList)

def getMaps(deformer):
    '''
    This will return the list of maps that live on the deformer passed into this funciton.

    :param deformer: The deformer name
    :type deformer: str

    :return: List of deformers
    :rtype: list
    '''

    # first we will make sure the deformer exist in the current Maya session
    if not mc.objExists(deformer):
        raise RuntimeError("{} doesn't exist in the current Maya session!".format(deformer))

    if mc.nodeType(deformer) == "skinCluster":
        return mc.skinCluster(deformer, q=True, inf=True)
    elif mc.nodeType(deformer) == "cluster":
        return None

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
                    skin = mc.skinCluster(jointListExists, geometry, name=deformer, tsb=True)[0]
                    # Set to dual quaternion mode
                    mc.setAttr('{}.skinningMethod'.format(skin), 1)

            # apply the weights
            if not mc.objExists(deformer):
                print('deformer does not exist [ {} ]'.format(deformer))
                continue
            rigrepo.libs.weights.importWeights(geometry, deformer, filepath)
            # this ensures that our skinCluster is normalized. 
            if deformerType == "skinCluster":
                mc.skinCluster(deformer, e=True, fnw=True)
