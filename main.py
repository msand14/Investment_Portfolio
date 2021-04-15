from modules.operateReturns import runAssets
from classes.portfolio import Portfolio, Asset

def main():
    euroStockIndex = Asset('eurozone-stock-index-inv-eur', 'fund')
    euroStockIndex.initial_inversion = 1000
    euroStockIndex.allocation = 0.25
    ie00b246kl88 = Asset('ie00b246kl88', 'fund')
    xetraGold = Asset('xetra-gold', 'etf')
    lyxorAAAGov1_3yr = Asset('lyxor-euromts-aaa-gov-1-3-y', 'etf')
    us500StockIndex = Asset('us-500-stock-index-inv-usd', 'fund')
    dtla = Asset('dtla', 'etf')
    swissGoldUSD = Asset('etfs-physical-swiss-gold-uk', 'etf')
    isharesTreasuryUSD = Asset('ishares-treasury-bond-0-1yr-ucits', 'etf')
    gobalStockIndexUSD = Asset('global-stock-index-ins-usd', 'fund')
    gobalStockIndexUSD.allocation = 0.33
    vanguardReit = Asset('vanguard-reit', 'etf')
    vanguardReit.allocation = 0.33
    vanguardTotalBondMarket = Asset('vanguard-total-bond-market', 'etf')
    vanguardTotalBondMarket.allocation = 0.33

    european_PP = Portfolio('European Permanent Portfolio')
    european_PP.inversion = 4000
    european_PP.myAssets = [euroStockIndex, ie00b246kl88, xetraGold,
                            lyxorAAAGov1_3yr]

    american_PP = Portfolio('American Permanent Portfolio')
    american_PP.inversion = 4000
    american_PP.myAssets = [us500StockIndex, dtla, swissGoldUSD,
                            isharesTreasuryUSD]

    talmud_pfolio = Portfolio('Talmud Portfolio')
    talmud_pfolio.inversion = 3000
    talmud_pfolio.myAssets = [gobalStockIndexUSD, vanguardReit,
                              vanguardTotalBondMarket]
    for folderName, portfolio in zip(['EUR_PP', 'USA_PP', 'talmud_folio'],
                                  [european_PP, american_PP, talmud_pfolio]):
        runAssets(portfolio=portfolio, folder=folderName,
                  fromDate='01/01/2020', returnsUnit='Percentage')


if __name__ == '__main__':
    main()
