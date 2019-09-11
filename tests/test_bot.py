import unittest
import os
import discord
from bot import _get_chart

class TestBot(unittest.TestCase):
    
    def test_environvars(self):
        self.assertEqual(type(os.environ.get('BOT_TOKEN')), str)
        self.assertEqual(type(os.environ.get('BOT_AIS_KEY')), str)
        self.assertEqual(type(os.environ.get('BOT_AIS_TOKEN')), str)
        self.assertEqual(type(os.environ.get('BOT_TEST_GUILD_ID')), str)
        self.assertEqual(type(os.environ.get('BOT_TEST_USER_ID')), str)

    def test_getcharts(self):
        """
        Test if it can get charts from aisweb
        """
        a, b = _get_chart('SBBR', 'ADC')
        self.assertEqual(a, True)
        self.assertEqual(type(b), list)

    def test_getmetartaf(self):
        """
        Test if it can get metar/taf from aisweb
        """
        pass

    def test_getnotam(self):
        """
        Test if it can get notam from aisweb
        """
        pass

    def test_rotaer(self):
        """
        Test if it can get metar from aisweb
        """
        pass

    def test_infotemp(self):
        """
        Test if it can get infotemp from aisweb
        """
        pass

    def test_sol(self):
        """
        Test if it can get sol from aisweb
        """
        pass

    def test_waypoints(self):
        """
        Test if it can get waypoints info from aisweb
        """
        pass

if __name__ == '__main__':
    unittest.main()
