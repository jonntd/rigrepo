'''
This is our json module.
'''
import os
from collections import OrderedDict
import maya.cmds as mc
import json
import getpass
from time import gmtime, strftime

class AbstractData(object):
    '''
    '''
    def __init__(self):
        '''
        '''
        # set class attributes defaults
        self._data = OrderedDict()
        self._filepath = None

    def gatherData(self,node):
        '''
        '''
        if not mc.objExists(node):
            mc.warning("{0} does not exists in the current Maya session.".format(node))
        
        self._data[node] = OrderedDict(dagPath=mc.ls(node,l=True)[0])

    def gatherDataIterate(self, nodes):
        '''
        '''
        for node in nodes:
            self.gatherData(node)

    def getData(self):
        '''
        '''
        return self._data

    def write(self, filepath, createDirectory=True):
        '''
        This will write a dictionary of information out to disc in .json format.

        :param data: This is the dictionary of info you want to write out.
        :type data: dict | orderedDict

        :param filepath: The path to the file you wish to write.
        '''
        if not isinstance(self._data, (dict, OrderedDict)):
            raise TypeError("The data must be passed in as a dictionary.")
        # writeData is user specific just on export
        writeData = OrderedDict(user=getpass.getuser(), 
                                type= self.__class__.__name__,
                                time=strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        writeData['data'] = self._data
        # dump data to json format and write it out to disk.
        data = json.dumps(writeData, indent=4)

        # Create directory if needed
        directory = os.path.dirname(filepath)
        if createDirectory:
            if not os.path.isdir(directory):
                print('making directory', directory)
                os.makedirs(directory, 755)

        # Write
        f = open(filepath, 'w')
        f.write(data)
        f.close()

        # set a new filepath on the class.
        self._filepath = filepath

    def read(self, filepath):
        '''
        This will read a .json file from disk and return the data in the file.

        :param filepath: The path to the file you wish to read from.
        :type filepath: str

        :return: Data that was read from filepath given.
        :rtype: dict
        '''
        if not os.path.isfile(filepath):
            raise RuntimeError("This {0} does not exists.".format(filepath))

        f = open(filepath, 'r')
        data = json.loads(f.read())
        f.close()

        # set a new filepath on the class.
        self._filepath = filepath
        self._data = data['data']
        return self._data

    def applyData(node, attributes=None):
        '''
        '''
        pass
