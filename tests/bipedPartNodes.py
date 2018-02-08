import pubs.ui.mainWindow
import rigrepo.templates.biped.biped as biped
import rigrepo.libs.data.joint_data
import os

buildPath = os.path.join(os.path.dirname(biped.__file__),"build")
import maya.cmds as mc
mc.file(os.path.join(buildPath,"skeleton.ma"), o=True,f=True)
data = rigrepo.libs.data.joint_data.JointData()
data.read(os.path.join(buildPath,"joint_positions.data"))
data.applyData(mc.ls(type="joint"))

# the right arm is all messed up and we have to fix it. Also, you can't run nodes more than once
# in the same scene at th moment. We will have to fix this.
matt_graph = biped.Biped('matt')
pubs.ui.mainWindow.launch(graph=matt_graph)