import pandas as pd
from modules.scrappingActions import getHistorical
from classes.portfolio import Portfolio
from modules.drawStuff import plotAssetOrPortfolio, plotMultipleAssets
from modules.handleDf import makeUpDf

def addFeatures(df, allocation: float, inversion: int, name: str):
    """
    Gets a Pandas Dataframe with two columns ( Date and Price) and
    add some columns like Allocation, Normalization Return and Positions.
    :param df: Pandas Dataframe containing ( Date and Price)
    :param allocation: float, allocation part of the Portfolio
    :param inversion: Inversion of the Asset
    :param name: str, name of the Asset.
    :return: Pandas Dataframe with all this added information.
    """
    # df.index = df['Date']
    # df.drop('Date', axis=1, inplace=True)
    df.sort_values(by='Date', inplace=True)
    df['Norm return'] = df['Price'] / df['Price'].iloc[0]
    df['Allocation'] = df['Norm return'] * allocation
    df['Position Cap'] = df['Allocation'] * inversion
    df['Return'] = df['Position Cap'].pct_change(1).fillna(0)
    df['Return %'] = df['Return'] * 100
    return df

def getCombinedReturns(portfolio: Portfolio, group_name: str):
    """
    Get a Portfolio Dictionary with all returns from assets and return the
     combined returns
    :param assets: List of assets
    :param group_name: WTF?¿
    :return dfFinal: Pandas Dataframe with two columns ( Date and
     combined return)
    """
    for i, asset in enumerate(assets):
        if i == 0:
            dfFinal = asset.assetDf.copy()
            returnNameCol = dfFinal.columns[1]
        else:
            # lets summ all the returns columns in order to get a
            # combined return for the portfolio
            dfFinal[returnNameCol] += asset.assetDf.iloc[:, 1]
    returnColName = dfFinal.columns[1]
    dfFinal.rename(columns={returnColName: group_name}, inplace=True)
    return dfFinal


def getMultiplePortfolioAnnualReturns(portfolios: list):
    """
    Gets a list of Portfolios and returns a df with all the summ Return of
     the Assets of every Portfolio in a specified
    period of time
    :param portfolios: List of Portfolio objects
    :return: Pandas Dataframe containing Dates column and several returns
    columns depending onf the amount of Portfolios introduced in the input
    list.
            List of Pandas Dataframes containing for each Portfolio:
            'Date' Column and 'return' column ( summ of its assets returns).
    """
    dateCol = 'Date'
    portfolios_meanReturnsDf = []
    dfFinal = pd.DataFrame()
    for i, pfolio in enumerate(portfolios):
        if i == 0:
            # Copy the first dataframe (with Assets Returns Combined)
            # of all the List of Dicts (Portfolios)
            dfFinal = getCombinedReturns(assets=pfolio.myAssets,
                                         group_name=pfolio._name).copy()
            portfolios_meanReturnsDf.append(dfFinal)
            # Lets save the Date column as a unique one for all the
            # portfolios
            dateCol = dfFinal.columns[0]
        else:
            # Combine Dataframes of AvgReturns (Date, Return) of every
            # Portfolio with the dfFinal but dropping the Date
            combRets = getCombinedReturns(assets=pfolio.myAssets,
                                          group_name=pfolio._name)
            portfolios_meanReturnsDf.append(combRets)
            combRets = combRets.drop(dateCol, axis=1)
            dfFinal = pd.concat([dfFinal, combRets], axis=1)
    return dfFinal, portfolios_meanReturnsDf

def runAssets(portfolio, folder: '',
              fromDate: str, returnsUnit=''):
    """

    :param portfolio: Portfolio object to be analyzed.
    :param portFolio: Portfolio object containing different Assets objects.
    :param namePortfolio: Name of the Portfolio, not a compulsory parameter.
    :param folder: Name of the folder where to save the Portfolio Data ( it
                    will be located inside Figures directory).
    :param fromDate: Date from where get the historical data of the Portfolio.
    :param returnsUnit: String, if 'Percentage' the Returns will be given in
                        that style, if not, Normalised style will be used.
    :return:
    """


    for asset in portfolio.myAssets:
        # First lets get the Historical Price Data and put it into a Dataframe
        # and get also the Real Name of the Active from the webpage
        df, name_active = getHistorical(asset.assetName, fromDate=fromDate,
                                        Mode=asset.assetType)
        df = makeUpDf(df)
        df_asset = addFeatures(df, allocation=asset.allocation,
                               inversion=portfolio.inversion,
                               name=asset.assetName)
        asset.assetDf = df_asset
        asset.sharpeRatio = df_asset['Return']

    allAsset = [portfolio.myAssets[0].assetDf['Date']] + \
               [asset.assetDf['Position Cap'] for asset in
                portfolio.myAssets]

    df_allAsset = pd.concat(allAsset, axis=1)
    df_allAsset['Position'] = df_allAsset.sum(axis=1)
    df_allAsset['Return'] = df_allAsset['Position'].pct_change(1).fillna(0)
    df_allAsset['Return %'] = df_allAsset['Return']*100
    portfolio.portfolioDf = df_allAsset
    portfolio.sharpeRatio = df_allAsset['Return']

    plotMultipleAssets(assets=portfolio.myAssets,
                       outputFileName='Assets_Inversion.png',
                       df_Y_nameCol='Position Cap',
                       yFinalName="Variation of Inversion",
                       value_name="Variation of Inversion",
                       tittle="How is my money going? (Assets Version)",
                       folder=folder)
    plotMultipleAssets(assets=portfolio.myAssets,
                       outputFileName='Assets_returns.png',
                       df_Y_nameCol='Return %',
                       yFinalName="Return %",
                       value_name="Return %",
                       tittle="Returns of my Assets",
                       folder=folder)
    plotAssetOrPortfolio(input_obj=portfolio,
                         tittle=("How is my money going? " +
                                 "(Portfolio Cash Version)"),
                         y_plotName='Variation of Inversion',
                         Y_axis_colName="Position",
                         output_name="Portfolio_Inversion_cash.png",
                         folder=folder)
    plotAssetOrPortfolio(input_obj=portfolio,
                         tittle=("How is my money going? " +
                                 "(Portfolio returns Version)"),
                         y_plotName='Variation of Inversion',
                         Y_axis_colName="Return %",
                         output_name="Portfolio returns.png",
                         folder=folder)
    print('Portfolio: ' + portfolio.portFolioName)
    for asset in portfolio.myAssets:
        print('  Asset: ' + asset.assetName + ' sharpeRatio: ' + str(asset.sharpeRatio))
