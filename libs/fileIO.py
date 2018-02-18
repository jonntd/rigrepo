'''
This is the common module for all the common utility functions
'''

#importing python modules
import os
import shutil

#import maya modules
import maya.cmds as mc

def copyFile(src, dst):
    '''
    copys file from src to dst path
    
    :param src: Source file path to copy file from
    :type src: str
    
    :param dst: Destination file path to copy file to
    :type dst: str
    '''
    shutil.copyfile(src = src, dst = dst)
    
def copyDir(src,dst, ignore = None):
    shutil.copytree(src, dst, ignore=ignore)

    
def isFile(filename):
    '''
    Check to see if file actually exists.

    :param filename: filename you want to check
    '''
    if os.path.isfile(filename):
        return True
        
    return False
    
def isDir(dirname):
    if os.path.isdir(dirname):
        return True
        
    return False

def isType(filename, fileExtension = 'py'):
    if isFile(filename):
        if fileExtension == os.path.splitext(filename)[1][1:]:
            return True
        
        return False
    else:
        raise IOError('%s does not exist!' % filename)
    
def loadPlugin(name):
    '''
    Loads plugins. First checks to see if it exists/loaded
    
    :param name: Name of the plugin with extension
    :type name: str  
    '''
    try:
        if not mc.pluginInfo(name, q = True, l = True):
            mc.loadPlugin(name)
    except:
        mc.warning('%s plugin cannot be loaded' % name)

def joinPath(*argv):
    path = os.path.join(*argv).replace('\\','/')
    return(path)

