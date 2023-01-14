import unittest

from hard_data import generate_sample_df_with_pattern
from patterns import detect_head_shoulder

class TestHeadShoulderDetection(unittest.TestCase):
    def test_detect_head_shoulder(self):
        # Generate data with head and shoulder pattern
        df_head_shoulder = generate_sample_df_with_pattern("Head and Shoulder")
        df_inv_shoulder = generate_sample_df_with_pattern("Inverse Head and Shoulder")
        df_with_detection = detect_head_shoulder(df_head_shoulder)
        df_with_inv_detection = detect_head_shoulder(df_inv_shoulder)
        self.assertTrue(df_with_detection['head_shoulder_pattern'].str.contains("Head and Shoulder").any())
        self.assertTrue(df_with_inv_detection['head_shoulder_pattern'].str.contains("Inverse Head and Shoulder").any())



if __name__ == '__main__':
    unittest.main()
