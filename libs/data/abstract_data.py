'''
This is our json module.
'''
import os
from collections import OrderedDict
import maya.cmds as mc
import json
import getpass
from time import gmtime, strftime

import rigrepo.libs.common

class AbstractData(object):
    '''
    The template for all data classes. This doesn't define any specific data. Rather it is a
    place where we describe how the data classes should be constructed.
    '''
    def __init__(self):
        '''
        The constructor for the abstract class. This abstract class is used as a template for
        all data classes. 
        '''
        # set class attributes defaults
        self._data = OrderedDict()
        self._filepath = None

    def gatherData(self,node):
        '''
        This method will gather data for the node that is passed in as an argument. It will
        store this data on the self._data member/attribute on the class.

        :param node: Node you wish to gather the data for.
        :type node: str
        '''
        if not mc.objExists(node):
            mc.warning("{0} does not exists in the current Maya session.".format(node))
        
        self._data[node] = OrderedDict(dagPath=mc.ls(node,l=True)[0])

    def gatherDataIterate(self, nodes):
        '''
        This method will iterate through the list of nodes passed in and use ther gatherData
        method to store the data onto the self._data member/attribute.

        :param nodes: Array of nodes you wish to gather the data from.
        :type nodes: list | tuple
        '''
        for node in nodes:
            self.gatherData(node)

    def getData(self):
        '''
        This will return the self._data member/attribute.
        '''
        return self._data

    # Set
    def setData(self, value):
        '''
        This should only be setting the data on this class if the data is a dictionary.

        .. warning::
            We're not checking to make sure the data is correct. Only if it's a dictionary.

        :param value: The data for what it is you're trying to set.
        :type value: dict
        '''
        if not isinstance(value, dict):
            raise TypeError("The value argument must be a dictionary.")

        self._data = value

    def applyData(node, attributes=None):
        '''
        Holder method for inherited classes to define how it will be used.
        '''
        pass

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
        self._data = rigrepo.libs.common.convertDictKeys(data['data'])
        return self._data

