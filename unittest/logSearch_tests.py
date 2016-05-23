__author__ = 'davidsiecinski'
import unittest
import logsearch

class LogSearchTestCase (unittest.TestCase):
    def setUp(self):
        current_picture=[[0,0,0,0],[0,1,0,0],[0,3,0,0],[0,0,0,0]]
        reference_picture=[[0,0,0,0],[0,0,1,0],[0,0,3,0],[0,0,0,0]]
        self.logsearch_= logsearch.LogSearch(current_picture,reference_picture)

        small_current_picture=[[0,1,0,0]]
        small_reference_picture=[[0,0,1,0]]
        self.small_logsearch = logsearch.LogSearch(small_current_picture,small_reference_picture)


    def test_motionVector(self):
        self.small_logsearch.p = 1
        return_value = [0, 1]
        # macrobloc size
        self.small_logsearch.n = 1
        # coordinates of top left corner of macro block
        self.small_logsearch.y= 0
        self.small_logsearch.x = 1

        self.assertEqual(self.small_logsearch.motionVector(), return_value)
    def test_motionEstimation(self):
        self.small_logsearch.p = 1
        self.small_logsearch.n = 1
        result=[[[0,0],[0,1],[0,-1],[0,0]]]
        self.assertEqual(self.small_logsearch.motionEstimation(),result)

    def test_motionEstimation2(self):
        # result should fit one of 2 choices
        result1=[[[0, 1],[0, -2]], [[0, 1],[-2, -2]]]
        self.small_logsearch.p = 1
        # [0,0]
        self.assertEqual(self.logsearch_.motionEstimation(),result1)
