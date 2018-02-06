#import python modules
import os
import sys
import platform

__VERSION__ = "0.1.0"
PACKAGE     = os.path.dirname(__file__)
RELEASEDIR  = str() #os.path.join(os.environ['HOME'], 'release/rig/')
USERDIR     = str() #os.path.join(os.environ['HOME'], 'user/wyoder/rig/')
PLUGINDIR   = os.path.join(os.path.dirname(__file__), 'plugins/')

def importModule(modulePath, force = False):
    '''
    Imports specified module using python's native __import__

    ..python
        importModule('libs.common')

    :param modulePath: path to the module
    :type modulePath: *str*
    @param force:
    '''

    # Resolve module name
    modname = modulePath.split (".")[-1]
    paths = modulePath.split (".")[:-1]

    #create empty string for path
    path = str()

    for p in paths:
        path = '%s/%s' % (path, p)#build path

    #build filepath for module
    filepath = os.path.join('%s%s/%s.py' % (PACKAGE, path, modname))

    #get directory to for path
    directory = os.path.dirname( filepath )
    #add directory to sys.path if it does not exist
    if directory not in sys.path:
        sys.path.append( directory )

    # This version of python import lets you use variables as the name
    # The default version does not
    module = __import__( modname )

    if force:
        reload(module)

    # This returns module as an object
    return module

#File I/O
#-------------------------------
def getSystem():
    '''
    Returns operating system

    '''
    if platform.system() == "Linux" or platform.system() == "Linux2":
        # Linux
        return 'Linux'
    elif platform.system() == "Darwin":
        # OS X
        return 'MacOSX'
    elif platform.system() == "Win32":
        # Windows...
        return 'Windows'

def getSystemVersion():
    '''
    returns version of operating system
    '''
    return platform.version()

def getHomeDir():
    '''
    return home directory
    '''
    return os.path.expanduser("~")
