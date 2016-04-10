__author__ = 'davidsiecinski'
import unittest
import diamondSearch

class DiamondSearchTestCase (unittest.TestCase):
    def setUp(self):
        current_picture=[[0,0,0,0],[0,1,0,0],[0,3,0,0],[0,0,0,0]]
        reference_picture=[[0,0,0,0],[0,0,1,0],[0,0,3,0],[0,0,0,0]]
        self.diamond_search_= diamondSearch.DiamondSearch(current_picture,reference_picture)

        small_current_picture=[[0,1,0,0]]
        small_reference_picture=[[0,0,1,0]]
        self.small_diamond_search = diamondSearch.DiamondSearch(small_current_picture,small_reference_picture)


    def test_motionVector(self):
        self.small_diamond_search.p = 1
        return_value = [0, 1]
        # macrobloc size
        self.small_diamond_search.n = 1
        # coordinates of top left corner of macro block
        self.small_diamond_search.y= 0
        self.small_diamond_search.x = 1

        self.assertEqual(self.small_diamond_search.motionVector(), return_value)
    def test_motionEstimation(self):
        self.small_diamond_search.p = 1
        self.small_diamond_search.n = 1
        result=[[[0,0],[0,1],[0,-1],[0,0]]]
        self.assertEqual(self.small_diamond_search.motionEstimation(),result)

    def test_motionEstimation2(self):
        # result should fit one of 2 choices
        result1=[[[0, 1],[0, -2]], [[0, 1],[-2, -2]]]
        self.small_diamond_search.p = 1
        # [0,0]
        self.assertEqual(self.diamond_search_.motionEstimation(),result1)
