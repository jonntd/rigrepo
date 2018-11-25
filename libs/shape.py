'''
This module is for dealing with shape nodes in Maya
'''
import maya.cmds as mc 
import numpy
def getDeltas(base, target): 
    '''
    Get deltas between two shapes. This will return the magnitude which will be the difference
    between the two points.

    :param base: Base object
    :type base: str
    
    :param target: Target object
    :type target: str

    :returns: List of deltas in the order of point index
    :rtype: list
    '''
    if not mc.objExists(base) or not mc.objExists(target):
        raise RuntimeError("Either {} or {} doesn't exist in the current Maya session".format(base, target))
     
    bs = mc.blendShape(target, base, w=[0, 1])[0] 
    #mc.pointPosition(base+'.vtx[0]') # Enforce refresh
    mc.pointPosition(target+'.vtx[0]') # Enforce refresh 
    delta_list = mc.getAttr(bs+'.it[0].itg[0].iti[6000].ipt')
    index_list = mc.getAttr(bs+'.it[0].itg[0].iti[6000].ict')                                
    mc.delete(bs)
    if not index_list:
        return([])
 
    # =============================================== 
    # Point array 
    # =============================================== 

    count = len(index_list) 
    index_flat_list = list() 
    for n in index_list: 
        index_flat_list.append(target+'.'+n) 
     
    index_flat_list = mc.ls(index_flat_list, fl=1) 
    index_only_list = list() 
     
    for n in index_flat_list: 
        index_only_list.append(int(n.split('[')[1][:-1])) 
     
    # =============================================== 
    # Weight array 
    # ===============================================     
    weight_list = numpy.zeros(len(mc.ls("{}.cp[*]".format(target),fl=True)), dtype=float)                      
    for n in range(len(index_flat_list)): 
        weight_list[index_only_list[n]] = round(delta_list[n][0], 4)

    return weight_list
