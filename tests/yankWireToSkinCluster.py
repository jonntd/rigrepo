import rigrepo.libs.shape
import rigrepo.libs.weights
import maya.cmds as mc
reload(rigrepo.libs.weights)
reload(rigrepo.libs.shape)

base = 'pCylinder1_noDeformation'
target = 'pCylinder1_wireDeformed'
sc = 'skinCluster2'

for joint in mc.ls('joint?'):
    mc.move( 1, 0, 0, joint, r=1) 
    deltas = rigrepo.libs.shape.getDeltas(base, target)
    #print(deltas)
    mc.move( -1, 0, 0, joint, r=1) 
    rigrepo.libs.weights.setWeights(sc, deltas, map=joint) 
    
mc.skinPercent(sc, mc.deformer(sc, q=1, geometry=1)[0], normalize=1) # in case of floating point precision 
