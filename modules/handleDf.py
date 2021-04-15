import pandas
import pandas as pd


def saveDf(df, location: str):
    if not isinstance(location, str):
        raise TypeError(saveDf.__name__ +
                        ': Location parameter has not a string type.' +
                        'Actual type: ' + type(location))
    try:
        pd.to_pickle(df, location)
    except:
        raise IsADirectoryError(saveDf.__name__ +
                                ': Location introduced doesnt exist:' +
                                location)


def loadDf(location):
    if not isinstance(location, str):
        raise TypeError(loadDf.__name__ +
                        ': Location parameter has not a string type.' +
                        'Actual type: ' + type(location))
    try:
        df = pd.read_pickle(location)
    except:
        raise FileNotFoundError(loadDf.__name__ +
                                ': File not found in location: ' +
                                location)
    return df


def checkDf(df):
    """

    :param number: number of variables that are represented in the df
                   A df with 1 variable is a df with 2 columns (Date
                   and Price/Return/Other)
    :param df: Dataframe to analyse
    :return:
    """
    if type(df) != pandas.core.frame.DataFrame:
        raise TypeError(checkDf.__name__ +
                        ': Parameter introduced is not a Dataframe!')
    elif df.empty:
        raise ValueError(checkDf.__name__ +
                         ': Parameter introduced is an empty Dataframe' +
                         'it mustnt be empty!')
    else:
        return True
    return False


def makeUpDf(df):
    """
    Treatment for the columns typo
    :param df: Dataframe containing Dates and Price
    :return df: Dataframe with the proper column types
    """
    df = df.apply(lambda x: x.str.replace(',', '.'))
    df['Price'] = df['Price'].astype(float)
    df['Date'] = df['Date'].astype(str)
    df['Date'] = df['Date'].apply(lambda x: x.replace('.', '-'))
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    return df