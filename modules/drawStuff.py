import pandas as pd
import seaborn as sns
import os
import time
import copy
from matplotlib import pyplot as plt
from classes.portfolio import Asset, Portfolio

sns.set_style('whitegrid')

def plotAssetOrPortfolio(input_obj, tittle: str, Y_axis_colName: str,
                         y_plotName: str, output_name, folder=''):
    """
    Plot the Asset or Portfolio
    :param Y_axis_colName: str, Name of the Pandas Dataframe column to be used
    as Y axis column in the plot.
    :param folder: string, Name of the Folder where to save the plot
    :param output_name: string, Name of the file to be save  as
    :param y_plotName: string, Name of the Y axis to be plot as
    :param tittle: string, Tittle of the Plot
    :param input_obj: Portfolio or Asset object
    """

    if folder != '' and not os.path.exists(os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'Figures', folder))):
        os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 'Figures', folder)))
    sns.set(rc={'figure.figsize': (28, 10)})
    time.sleep(1)
    df = copy.deepcopy(input_obj.assetDf[['Date', Y_axis_colName]]) if \
        isinstance(input_obj, Asset) else \
        copy.deepcopy(input_obj.portfolioDf[['Date', Y_axis_colName]])
    df.rename(columns={Y_axis_colName: y_plotName},
              inplace=True)
    ax = sns.lineplot(x="Date", y=y_plotName, data=df)
    ax.set_title(tittle)
    if folder != '':
        plt.savefig(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 'Figures', folder +
                                                 '\\' + output_name +
                                                 '.png')))
    else:
        plt.savefig(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 'Figures\\' +
                                                 output_name + '.png')))
    plt.close()


def plotMultipleAssets(assets, outputFileName: str, df_Y_nameCol: str,
                       value_name: str, yFinalName: str, tittle: str,
                       folder: str):
    """
    Plot he Variation of the Investment in several assets
    :param folder: string, Name of the Folder where to save the plot
    :param df_Y_nameCol: string, Name of the Dataframe Column which contains
        the Y-Axis values. For example if original column name is :
        'Position Cap ' +
    :param value_name: string, Final Name of melted columns of each
        asset that represent the yName.
    :param outputFileName: string, Name of the file to be save  as
    :param yFinalName: string, Name of the Y axis to be plot as
    :param tittle:  string, Tittle of the Plot
    :param assets: ListOfAssets/Portfolio
    """
    if folder != '' and not os.path.exists(os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'Figures', folder))):
        os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 'Figures', folder)))
    if isinstance(assets, list):
        # List of Assets case
        df_assets = pd.DataFrame()
        for i, asset in enumerate(assets):
            asset_name = asset.assetName
            df_yNameColFinal = df_Y_nameCol + ' ' + asset_name
            df_asset = copy.deepcopy(asset.assetDf[['Date', df_Y_nameCol]])
            df_asset.rename(columns={df_Y_nameCol: df_yNameColFinal},
                            inplace=True)
            if i == 0:
                df_assets = pd.concat([df_assets, df_asset], axis=1)
            else:
                df_assets = pd.concat([df_assets, df_asset[df_yNameColFinal]],
                                      axis=1)
        df_melted = df_assets.melt("Date", var_name="Assets",
                                   value_name=value_name)
        sns.set(rc={'figure.figsize': (28, 10)})
        time.sleep(1)
        ax = sns.lineplot(x="Date", y=yFinalName, data=df_melted, hue="Assets")
        ax.set_title(tittle)
        ax.legend(loc=2, borderaxespad=0.)
        plt.savefig(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 'Figures', folder +
                                                 '\\' + outputFileName)))
        plt.close()

