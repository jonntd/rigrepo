'''
This module will have the class that deals with weights.
'''
import numpy
import rigrepo.libs.common 
class WeightObject(object):
    '''
    Class that contains maps and weights per map.
    '''
    def __init__(self, maps=list(), weights=list()):
        '''
        This is the constructor for our weightObject

        :param maps: List of maps that will have a corresponding weights array per component
        :type maps: list

        :param weights: List of numpy array's storing influnce value per component
        :type weights: list
        '''
        super(WeightObject, self).__init__()

        self.__maps = list()
        self.__weights = list()
        self.setMaps(maps)
        self.setWeights(weights)
        self._index = 0
        
    def __iter__(self):
        return self

    def next(self):
        '''
        This will iterate through each index
        '''
        try:
            result = self.__maps[self._index]
        except IndexError:
            self._index = 0
            raise StopIteration
        self._index += 1
        return result

    # Get
    def getMaps(self):
        '''
        This will return the list of maps 

        :return: List of maps stored on this weight object
        :type: list
        '''
        return self.__maps

    def getWeights(self, maps=None):
        '''
        This will return the list of weights 

        :return: List of maps stored on this weight object
        :type: list
        '''
        if not maps:
            return self.__weights
        else:
            mapList = rigrepo.libs.common.toList(maps)
            return [self.__weights[self.__maps.index(map)] for map in mapList if map in self.__maps]

    # Set
    def setMaps(self, value):
        '''
        This will take in a value which should be a list of maps you want to set 

        :param value: Must be a list of maps.
        :type value: list
        '''
        self.__maps = rigrepo.libs.common.toList(value)

    def setWeights(self, value):
        '''
        This will take in a value which should be a list of numpy arrays you want to in the order
        which you have given the maps. These two list should be the same length.

        :param value: Must be a list of numpy arrays.
        :type value: list
        '''
        weightList = rigrepo.libs.common.toList(value)
        self.__weights = list()
        for weights in weightList:
            if isinstance(weights, numpy.ndarray):
                self.__weights.append(weights)
                continue
            self.__weights.append(numpy.array(weights))

