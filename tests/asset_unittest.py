import unittest
import pandas as pd
from classes.portfolio import Asset, Portfolio


class testAsset(unittest.TestCase):

    def test_Constructor(self):
        # Wrong type of assetType
        with self.assertRaises(TypeError):
            Asset(a_name='myAsset', assetType='an_etf')
        # Wrong data type for assetType parameter
        with self.assertRaises(TypeError):
            Asset(a_name='myAsset', assetType=['test'])
        # Wrong data type for a_name parameter
        with self.assertRaises(TypeError):
            Asset(a_name=2, assetType='etf')
        # Wrong data type for assetType and a_name parameter
        with self.assertRaises(TypeError):
            Asset(a_name=2, assetType=['test'])
        # No parameters in Constructor
        with self.assertRaises(TypeError):
            Asset()

        test_asset = Asset(a_name='myAsset', assetType='fund')
        self.assertIsInstance(test_asset, Asset)
        self.assertIs(test_asset.assetName, 'myAsset')
        self.assertIs(test_asset.assetType, 'fund')

    def test_getters(self):
        test_asset = Asset(a_name='myAsset', assetType='fund')
        self.assertIs(test_asset.assetName, 'myAsset')
        self.assertIs(test_asset.assetType, 'fund')

        myDf = pd.DataFrame({'Col 1': [1, 2], 'Col 2': [3, 4]})
        test_asset.assetDf = myDf
        self.assertIsInstance(test_asset.assetDf, pd.DataFrame)
        self.assertIs(test_asset.assetDf, myDf)

        test_asset.allocation = 0.30
        self.assertIsInstance(test_asset.allocation, float)
        self.assertEqual(test_asset.allocation, 0.30)

        test_asset.sharpeRatio = pd.Series([1, 2, 3, 4])
        self.assertIsInstance(test_asset.sharpeRatio, float)

        test_asset.initial_inversion = 1000
        self.assertEqual(test_asset.initial_inversion, 1000)

    def test_Setters(self):
        test_asset = Asset(a_name='myAsset', assetType='fund')
        test_asset.assetName = 'myAsset2'
        test_asset.assetType = 'etf'

        mydf = pd.DataFrame({'Data': [1, 2, 3], 'Other': [23, 32, 34]})

        # Test AssetDF
        with self.assertRaises(TypeError):
            test_asset.assetDf = 'mydf'
        with self.assertRaises(ValueError):
            test_asset.assetDf = pd.DataFrame()
        test_asset.assetDf = mydf
        self.assertIsInstance(test_asset.assetDf, pd.DataFrame)

        returns = [1, 2, 3, 4]
        test_asset.assetStdDeviation = returns

        # Test asset Name
        self.assertEqual(test_asset.assetName, 'myAsset2')
        with self.assertRaises(TypeError):
            test_asset.assetName = ['myname']

        # Test asset Type
        self.assertEqual(test_asset.assetType, 'etf')
        with self.assertRaises(TypeError):
            test_asset.assetType = ['myname']
        with self.assertRaises(ValueError):
            test_asset.assetType = 'etf2'

        # Test Allocation
        with self.assertRaises(TypeError):
            test_asset.allocation = 1000
        with self.assertRaises(ValueError):
            test_asset.allocation = 0.0

        # Test Initial Inversion
        with self.assertRaises(TypeError):
            test_asset.initial_inversion = 0.25
        with self.assertRaises(ValueError):
            test_asset.initial_inversion = 0

        # Test Sharpe Ratio
        myReturns = pd.Series([1.5, 2, 4.1, 5])
        test_asset.sharpeRatio = myReturns
        self.assertEqual(round(test_asset.sharpeRatio, 2), 3.77)
        with self.assertRaises(TypeError):
            test_asset.sharpeRatio = 3


class testPortfolio(unittest.TestCase):

    def test_Constructor(self):
        # Wrong data type for a_name
        with self.assertRaises(TypeError):
            Portfolio(a_name=2)
        # No parameters in Constructor
        with self.assertRaises(TypeError):
            Portfolio()

        test_portfolio = Portfolio(a_name='myPortfolio')
        self.assertIsInstance(test_portfolio, Portfolio)
        self.assertIs(test_portfolio.portFolioName, 'myPortfolio')
        self.assertEqual(test_portfolio.inversion, 0)
        self.assertEqual(test_portfolio.myAssets, [])
        self.assertEqual(test_portfolio.sharpeRatio, 0.0)
        self.assertIsInstance(test_portfolio.portfolioDf, pd.DataFrame)

    def test_getters(self):
        # Test Name
        test_portfolio = Portfolio(a_name='myPortfolio')
        self.assertIs(test_portfolio.portFolioName, 'myPortfolio')

        # Test myAssets
        asset1 = Asset(a_name='myAsset1', assetType='etf')
        asset2 = Asset(a_name='myAsset2', assetType='fund')
        test_portfolio.myAssets = [asset1, asset2]
        self.assertIsInstance(test_portfolio.myAssets, list)
        self.assertIsInstance(test_portfolio.myAssets[0], Asset)
        self.assertIsInstance(test_portfolio.myAssets[1], Asset)

        # Test Number of Assets
        self.assertEqual(test_portfolio.assetsNumber, 2)

        # Test Df
        dummyDf = pd.DataFrame({'hey': [1, 2], 'ou': [3, 4]})
        test_portfolio.portfolioDf = dummyDf
        self.assertIsInstance(test_portfolio.portfolioDf, pd.DataFrame)

        # Test inversion
        test_portfolio.inversion = 1000
        self.assertIsInstance(test_portfolio.inversion, int)
        self.assertIs(test_portfolio.inversion, 1000)

        # Test sharpeRatio
        test_portfolio.sharpeRatio = pd.Series([1, 2, 3, 4])
        self.assertIsInstance(test_portfolio.sharpeRatio, float)
        self.assertEqual(round(test_portfolio.sharpeRatio, 2), 3.87)

    def test_setters(self):
        test_portfolio = Portfolio(a_name='myPortfolio')

        mydf = pd.DataFrame({'Data': [1, 2, 3], 'Other': [23, 32, 34]})

        # Test AssetDF
        with self.assertRaises(TypeError):
            test_portfolio.portfolioDf = 'mydf'
        with self.assertRaises(ValueError):
            test_portfolio.portfolioDf = pd.DataFrame()
        test_portfolio.portfolioDf = mydf
        self.assertIsInstance(test_portfolio.portfolioDf, pd.DataFrame)

        # Test Portfolio Name
        self.assertEqual(test_portfolio.portFolioName, 'myPortfolio')
        with self.assertRaises(TypeError):
            test_portfolio.portFolioName = ['myname']

        # Test my Assets
        asset1 = Asset(a_name='myAsset1', assetType='etf')
        asset2 = Asset(a_name='myAsset2', assetType='fund')
        with self.assertRaises(TypeError):
            test_portfolio.myAssets = asset1
        with self.assertRaises(TypeError):
            test_portfolio.myAssets = [asset1, 'asset2']
        test_portfolio.myAssets = [asset1, asset2]
        self.assertIsInstance(test_portfolio.myAssets, list)
        self.assertIsInstance(test_portfolio.myAssets[0], Asset)
        self.assertIsInstance(test_portfolio.myAssets[1], Asset)

        # Test Initial Inversion
        with self.assertRaises(TypeError):
            test_portfolio.inversion = 0.25
        with self.assertRaises(ValueError):
            test_portfolio.inversion = 0

        # Test Sharpe Ratio
        myReturns = pd.Series([1.5, 2, 4.1, 5])
        test_portfolio.sharpeRatio = myReturns
        self.assertEqual(round(test_portfolio.sharpeRatio, 2), 3.77)
        with self.assertRaises(TypeError):
            test_portfolio.sharpeRatio = 3


if __name__ == '__main__':
    unittest.main()
