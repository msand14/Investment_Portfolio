import unittest
import pandas as pd
from classes.portfolio import Portfolio, Asset


class testPortfolio(unittest.TestCase):

    def test_Constructor(self):
        with self.assertRaises(TypeError):
            myPortfolio = Portfolio()
        with self.assertRaises(TypeError):
            myPortfolio = Portfolio(a_name=3)

        test_Portfolio = Portfolio(a_name='pfolio')
        self.assertIsInstance(test_Portfolio, Portfolio)

    def test_Getters(self):
        test_Portfolio = Portfolio(a_name='pfolio')
        test_asset1 = Asset('asset1', 'etf')
        test_asset2 = Asset('asset1', 'fund')
        test_Portfolio.myAssets = [test_asset1, test_asset2]

        # Test Assets Number
        self.assertEqual(test_Portfolio.assetsNumber, 2)

        # Test getAssetByName
        self.assertIsInstance(test_Portfolio.getAssetByName(a_name='asset1'),
                              Asset)
        self.assertEqual(test_Portfolio. \
                         getAssetByName(a_name='asset1').assetName,
                         'asset1')


    def test_Setters(self):
        test_Portfolio = Portfolio(a_name='pfolio')

        # Test

        # Test assets Number


if __name__ == '__main__':
    unittest.main()
