"""
PSD unit and integration tests

Build a basic fixture Maya scene

"""
import maya.cmds as mc
import rigrepo.libs.psd as rlpsd
import rigrepo.libs.blendShape as rlbs
import math
reload(rlbs)
reload(rlpsd)
import unittest

class TestBasic(unittest.TestCase):
    def setUp(self):

        # Test data vars
        self.interp = 'test_interp'
        self.driver = 'locator_driver'
        self.pose_control = 'locator_poseControl'
        self.pose_ry_30 = 'test_rotateY_30'

        # Remove existing nodes
        nodes = mc.ls(self.interp, self.driver, self.pose_control)
        if nodes:
            mc.delete(nodes)

        # Create test scene
        self.driver = mc.spaceLocator(n=self.driver)[0]
        self.pose_control = mc.spaceLocator(n='locator_poseControl')[0]
        mc.orientConstraint(self.pose_control, self.driver)

        # Add interp
        self.interp = rlpsd.addInterp(self.interp,
                                 createNeutralPose=0,
                                 driver=self.driver,
                                 regularization=1,
                                 outputSmoothing=0,
                                 interpolation=1,
                                 allowNegativeWeights=1,
                                 enableRotation=1,
                                 enableTranslation=0,
                                 twistAxis=0)
        # Add pose control
        self.pose_control = self.pose_control + '.rotate'
        rlpsd.addPoseControl(self.interp, self.pose_control)

        # Add neutral pose
        rlpsd.addPose(self.interp, 'neutral', type='swing')

        # Add rotateY 30 pose
        rlpsd.addPose(self.interp, self.pose_ry_30, type='swing')

        # set pose control value

    def test_getPoseName(self):
        pose_name = rlpsd.getPoseName(self.interp, index=1)
        self.assertEqual(pose_name, self.pose_ry_30)

    def test_setPoseControlRotate(self):
        value = [0, 45.332323, 0]
        value_in_radians = [math.radians(x) for x in value]
        value_in_degrees = [math.degrees(x) for x in value_in_radians]
        rlpsd.setPoseControlRotate(self.interp, self.pose_ry_30, self.pose_control, value)
        test_rotate = rlpsd.getPoseControlRotate(self.interp, self.pose_ry_30, self.pose_control)
        self.assertEqual(test_rotate, value_in_degrees)

if __name__ == '__main__':
    unittest.main()