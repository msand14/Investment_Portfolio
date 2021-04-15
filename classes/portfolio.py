import pandas as pd
from modules.handleDf import checkDf
import numpy as np


class Portfolio:
    """ Portfolio class. Entity that contains different assets"""

    def __init__(self, a_name):
        if isinstance(a_name, str):
            self._inversion = 0
            self._name = a_name
            self._myAssets = []
            self._sharpeRatio = 0.0
            self._portfolioDf = pd.DataFrame()
        else:
            raise TypeError(classmethod.__name__ + ': Portfolio name type' +
                            'must be a string.')

    @property
    def portFolioName(self):
        """Gets the name of the Portfolio."""
        return self._name

    @property
    def assetsNumber(self):
        """Gets the number of assets that the Portfolio contains."""
        return len(self.myAssets)

    @property
    def myAssets(self):
        """Gets a list of the assets objects that the Portfolio contains."""
        return self._myAssets

    @property
    def portfolioDf(self):
        """
        (Not implemented yet)
        Gets the Pandas Dataframe contained in the Portfolio.
        :return: Pandas Dataframe that contains all the returns of a Portfolio.
        """
        return self._portfolioDf

    @property
    def inversion(self):
        """
        Gets the total inversion in the Portfolio
        :return: int, Inversion
        """
        return self._inversion

    @property
    def sharpeRatio(self):
        """
        Gets the Sharpe Ratio of the Portfolio
        :return: float, Sharpe Ratio
        """
        return self._sharpeRatio

    @portfolioDf.setter
    def portfolioDf(self, df):
        """
        ( not implemented yet)
        Sets the Dataframe of a Portfolio
        :param nVariables:
        :param df:
        :return:
        """
        if checkDf(df=df):
            self._portfolioDf = df

    @myAssets.setter
    def myAssets(self, assets):
        """
        Sets the assets objects of a Portfolio
        :param assets: List of Assets objects
                       [Asset1, Asset2,...]
        """
        # Check if assets is a list of lists of two elements (strings)
        if type(assets) != list:
            raise TypeError(classmethod.__name__ + ': Assets must be a list')

        # Well, we ve got a list at least! :D
        for i, asset in enumerate(assets):
            if type(asset) != Asset:
                raise TypeError(classmethod.__name__ +
                                ': Element ' + str(i) + ' in list if not' +
                                'an Asset. Type: ' + str(type(asset)))
            self._myAssets.append(asset)

    @portFolioName.setter
    def portFolioName(self, a_name):
        """
        Sets the name of the Portfolio
        :param a_name: string, Name of the Portfolio
        """
        if not isinstance(a_name, str):
            raise TypeError(classmethod.__name__ +
                            ': a_name parameter has not an string type' +
                            '. Current type of the parameter: ' +
                            str(type(a_name)))
        self._name = a_name

    @inversion.setter
    def inversion(self, inversion):
        """
        Sets the total Inversion of the Portfolio
        :param inversion: int Inversion
        """
        if not isinstance(inversion, int):
            raise TypeError(classmethod.__name__ +
                            ': Inversion parameter has not an int type' +
                            '. Current type of the parameter: ' +
                            str(type(inversion)))
        elif inversion <= 0:
            raise ValueError(classmethod.__name__ +
                             ': Initial Inversion must be greater than zero.' +
                             '. Current value of the Initial Inversion: ' +
                             str(inversion))
        else:
            self._inversion = inversion

    @sharpeRatio.setter
    def sharpeRatio(self, returns: pd.Series):
        """
        Sets the Sharpe Ratio for the Asset
        :param returns: Series that contains the returns of the Asset
        """
        if not isinstance(returns, pd.Series):
            raise TypeError(classmethod.__name__ +
                            ': returns must be a Pandas Series.' +
                            '. Current type of the returns: ' +
                            str(type(returns)))
        self._sharpeRatio = (returns.mean() / returns.std()) * (len(returns) ** 0.5)

    def getAssetByName(self, a_name: str):
        """
        Gets an Asset Object identified by the name.
        :param a_name: Name of the asset.
        :return: Asset object contained in the Portfolio.
        """
        ast = [asset for asset in self.myAssets if asset.assetName == a_name]
        return ast[0]

    def getAssetsNames(self):
        """
        Gets the names of all the assets
        :return: List of strings(names)
        """
        if len(self.myAssets) != 0:
            listofnames = []
            for i in self._myAssets:
                listofnames.append(i.assetName)
            return listofnames
        return

    def assignAssetsDfs(self, dictAssetDfs: dict):
        """
        Gets a dictionary of Key:AssetName and Value:Dataframe and set it to
         each Asset
        :param dictAssetDfs: dictionary of Key:AssetName and Value:Dataframe
        :return:
        """
        for asset in self._myAssets:
            if asset.assetName in dictAssetDfs.keys():
                asset.assetDf = dictAssetDfs[asset.assetName]


class Asset:
    """ Class Asset. Is a part of a Portfolio."""
    _possibleTypes = ['etf', 'fund']

    def __init__(self, a_name: str, assetType: str):
        if type(a_name) == str and type(assetType) == str:
            self._assetName = a_name
            if assetType not in self._possibleTypes:
                raise TypeError(classmethod.__name__ +
                                ': Wrong assetType introduced. Only accept' +
                                " 'etf' or 'fund'.")
            self._assetType = assetType
            self._contents = [a_name, assetType]
            self._assetDf = pd.DataFrame()
            self._sharpeRatio = 0.0
            self._allocation = 0.25
            self._initial_inversion = 1000
        else:
            raise TypeError(classmethod.__name__ +
                            ': Wrong parameters types introduced into' +
                            ' the constructor. We ask for (str,str)')

    @property
    def assetName(self):
        """
        Gets the name of the Asset.
        :return: string. Name of the Asset.
        """
        return self._assetName

    @property
    def assetType(self):
        """
        Gets the type of the Asset.
        :return: string. Type of the Asset ('etf' or 'fund')
        """
        return self._assetType

    @property
    def assetDf(self):
        """
        Gets the Pandas Dataframe related to the Asset.
        :return: Pandas Dataframe.
        """
        return self._assetDf

    @property
    def sharpeRatio(self):
        """
        Gets the Sharpe Ratio of the Asset
        :return: float, Sharpe Ratio
        """
        return self._sharpeRatio

    @property
    def allocation(self):
        """
        Gets the Allocation
        :return: float, Allocation of the Asset
        """
        return self._allocation

    @property
    def initial_inversion(self):
        """
        Gets the Initial Inversion
        :return: int, Initial Inversion
        """
        return self._initial_inversion

    @assetDf.setter
    def assetDf(self, df):  # crear un df para return y otro para prices
        """
        Sets the Pandas Dataframe related to the Asset.
        :param df: Pandas Dataframe to set
        """
        if checkDf(df=df):
            self._assetDf = df

    @assetName.setter
    def assetName(self, a_name):
        """
        Sets the Name of the Asset.
        :param a_name: string. Name of the Asset to set.
        """
        if type(a_name) == str:
            self._assetName = a_name
        else:
            raise TypeError(classmethod.__name__ +
                            ': Name of asset introduced is not a string')

    @assetType.setter
    def assetType(self, typ: str):
        """
        Sets the Type of the Asset.
        :param typ: string. Type of the Asset to set ('etf' or 'fund').
        """
        if not isinstance(typ, str):
            raise TypeError(classmethod.__name__ +
                            ': Type of asset introduced is not a string.')
        elif typ.lower() in self._possibleTypes:
            self._assetType = typ
        else:
            raise ValueError(classmethod.__name__ + ': ' + str(typ) +
                             ' is not a valid type of asset. Try with: ' +
                             str(self._possibleTypes))

    @sharpeRatio.setter
    def sharpeRatio(self, returns: pd.Series):
        """
        Sets the Sharpe Ratio for the Asset
        :param returns: Series that contains the returns of the Asset
        """
        if not isinstance(returns, pd.Series):
            raise TypeError(classmethod.__name__ +
                            ': returns must be a Pandas Series.' +
                            '. Current type of the returns: ' +
                            str(type(returns)))
        self._sharpeRatio = (returns.mean() / returns.std()) * (len(returns) ** 0.5)

    @allocation.setter
    def allocation(self, alloc: float):
        if not isinstance(alloc, float):
            raise TypeError(classmethod.__name__ +
                            ': Allocation must be a float.' +
                            '. Current type of the Allocation: ' +
                            str(type(alloc)))
        elif alloc <= 0:
            raise ValueError(classmethod.__name__ +
                             ': Allocation must be greater than zero.' +
                             '. Current value of the Allocation: ' +
                             str(alloc))
        else:
            self._allocation = alloc

    @initial_inversion.setter
    def initial_inversion(self, inversion: int):
        if not isinstance(inversion, int):
            raise TypeError(classmethod.__name__ +
                            ': Initial Inversion must be an Integer.' +
                            '. Current type of the Initial Inversion: ' +
                            str(type(inversion)))
        elif inversion <= 0:
            raise ValueError(classmethod.__name__ +
                             ': Initial Inversion must be greater than zero.' +
                             '. Current value of the Initial Inversion: ' +
                             str(inversion))
        else:
            self._initial_inversion = inversion
