import rigrepo.libs.shape as rigShape
reload(rigShape)
import rigrepo.libs.weights as rigWeights
reload(rigWeights)
import maya.cmds as mc

def testEye_yankWireToSkinCluster():
    deltaList = list()
    skinCls = "skinCluster2"
    jointList = mc.ls("lidUpper_l_*_bind")
    cvList = mc.ls("lidUpper_l_blink1.cv[*]", fl=True)
    for cv,jnt in zip(cvList,jointList):
        #pos = mc.xform(cv, q=True, ws=True, t=True)
        mc.move( 1, 0, 0, cv, r=1)
        #mc.refresh()
        #mc.pause(sec=1)
        deltas = rigShape.getDeltas("base_geo","head_geo")
        #print(deltas)
        mc.move( -1, 0, 0, cv, r=1)
        rigWeights.setWeights(skinCls,deltas, jnt)
        mc.setAttr("{0}.liw".format(jnt),1)


    mc.skinPercent(skinCls, mc.deformer(skinCls, q=1, geometry=1)[0], normalize=1) # in case of floating point precision
