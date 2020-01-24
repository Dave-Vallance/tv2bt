'''
Author: www.backtest-rookies.com

MIT License

Copyright (c) 2019 backtest-rookies.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import backtrader as bt
from datetime import datetime
from tv2bt import TVFeed
from ccxtbt import CCXTStore

apikey = 'INSERT YOUR API KEY'
secret = 'INSERT YOUR SECRET'

class TVTest(bt.Strategy):
    '''
    Simple strat to test TV Feed.
    '''

    params = (
        ('perc_size', 0.7),
        ('leverage', 1),
        ('fixed_qty', 12)
        )

    def __init__(self):

        self.data_info = dict()

        for i, d in enumerate(self.datas):

            # Tracking the last bar is useful when we have data coming in
            # at different times.
            self.data_info[d._name] = dict()
            self.data_info[d._name]['last bar'] = 0

            # When we are not using leverage, there is no concept of a
            # position. So we create a dict to store holdings of both
            # the base and quote currencies.
            ticker_components = d._name.split('/')
            self.data_info[d._name]['base'] = ticker_components[0]
            self.data_info[d._name]['counter'] = ticker_components[1]

            for comp in ticker_components:
                self.data_info[d._name][comp] = dict()
                self.data_info[d._name][comp]['cash'] = 0
                self.data_info[d._name][comp]['value'] = 0


    def next(self):

        print('='*80)
        print(' '*36,'NEXT')
        print('='*80)


        for i, d in enumerate(self.datas):

            dn = d._name
            dt = d.datetime.datetime()
            bar = len(d)
            pos = self.getposition(d).size
            base = self.data_info[dn]['base']
            counter = self.data_info[dn]['counter']

            print('Position : {}'.format(pos))

            # Check we have a new bar and are not repeating an old one.
            if bar > self.data_info[dn]['last bar']:
                print('DATE   : {}'.format(dt))
                print('ASSET  : {}'.format(dn))
                print('BAR    : {}'.format(bar))
                print('Open   : {}'.format(d.open[0]))
                print('High   : {}'.format(d.high[0]))
                print('Low    : {}'.format(d.low[0]))
                print('Close  : {}'.format(d.close[0]))
                print('Signal : {}'.format(d.signal[0]))
                print('-'*80)

                # Save the last bar processed
                self.data_info[dn]['last bar'] = bar

            # Get our balances only if we want to go buy/sell.
            # Otherwise, the request slows things down.
            if d.signal in [1,-1, 10]:

                # Get our cash and value to enter a position
                params = {'type': 'trading'}
                cash, value = self.broker.get_wallet_balance('USD', params=params)
                print('CASH   : {}'.format(cash))
                print('VALUE  : {}'.format(value))

            # Enter Long
            if d.signal == 1:

                # Note: Important Differences for the Type parameter!
                # https://docs.bitfinex.com/v1/reference#rest-auth-new-order
                # Also see:
                # https://github.com/ccxt/ccxt/issues/1207
                params = {'type': 'market', 'leverage':self.p.leverage}

                # Specify leverage!
                qty = ((cash * self.p.perc_size) / self.data.close[0]) * self.p.leverage # 2x leverage using 95% cash

                if pos < 0:
                    qty = qty + -pos

                print('Action : Buy | Qty: {}'.format(qty))
                self.buy(d, size=qty, params=params)

            # Enter Short
            if d.signal == -1:

                # Note: Important Differences for the Type parameter!
                # https://docs.bitfinex.com/v1/reference#rest-auth-new-order
                # Also see:
                # https://github.com/ccxt/ccxt/issues/1207
                params = {'type': 'market', 'leverage':self.p.leverage}

                # Specify leverage!
                qty = ((cash * self.p.perc_size) / self.data.close[0]) * self.p.leverage # 2x leverage using 95% cash

                if pos > 0:
                    qty = qty + pos

                print('Action : Sell | Qty: {}'.format(qty))
                self.sell(d, size=qty, params=params)

            if d.signal == 0:

                # Close the position
                # Note: Important Differences for the Type parameter!
                # https://docs.bitfinex.com/v1/reference#rest-auth-new-order
                # Also see:
                # https://github.com/ccxt/ccxt/issues/1207
                params = {'type': 'market'}
                print('Action: | Closing Position')
                self.close(params=params)




    def notify_data(self, data, status, *args, **kwargs):
        print('DATA NOTIF: {}: {}'.format(data._getstatusname(status), ','.join(args)))


    def notify_order(self, order):
        dt = order.data.datetime.datetime()
        dn = order.data._name

        print('='*33, 'NOTIFY ORDER', '='*33)

        if order.status == order.Submitted:
            print('Date   : {}'.format(dt))
            print('Ticker : {}'.format(dn))
            print('Notify : Order Submitted')

        if order.status == order.Accepted:
            print('Date   : {}'.format(dt))
            print('Ticker : {}'.format(dn))
            print('Notify : Order Accepted')

        if order.status == order.Completed:
            print('Date   : {}'.format(dt))
            print('Ticker : {}'.format(dn))
            print('Notify : Order Completed')

        if order.status == order.Canceled:
            print('Date   : {}'.format(dt))
            print('Ticker : {}'.format(dn))
            print('Notify : Order Canceled')

        if order.status == order.Rejected:
            print('Date   : {}'.format(dt))
            print('Ticker : {}'.format(dn))
            print('Notify : Order Rejected')

# Example Alerts
# --------------
# 1. DATA/OHLC
#    The ticker should be the same as you use for your broker to
#    make life easier. Don't blindly copy the Tradingview Ticker.
#    The rest of the string below should be copied in as it. Tradingview
#    will replace the values inside {{}} with the actual values.
'''
{'symbol':'[INSERT TICKER]', 'DT':'{{time}}', 'O':{{open}}, 'H':{{high}}, 'L':{{low}}, 'C':{{close}}, 'V':{{volume}}, 'action':0}
'''
# 2. SIGNALS
#    3 Types of signal are currently supported. 'long', 'short' and 'flat'
#    It is expected that you handle them appropriately and according to your
#    taste in backtrader
'''
{'symbol':'[INSERT TICKER]', 'action':1}
'''

print('='*80)
print('Starting Example Strategy')
print('All data feeds must have one bar of data before before you will see any output \n'
    'on the console. Please be patient...')
print('For instructions how to use, see:')
print('='*80)

debug = False

# Create an instance of cerebro
cerebro = bt.Cerebro()

# Get Data
data = TVFeed(dataname='BTC/USD',  debug=debug)

# Add the data feeds
cerebro.adddata(data)
#cerebro.adddata(data2)

# Set Config
config = {'apiKey': apikey,
          'secret': secret,
          'enableRateLimit': True,
          'rateLimit': 3000
        }

# Add our strategy
cerebro.addstrategy(TVTest)


print('Getting Store')
# Create data feeds
store = CCXTStore(exchange='bitfinex', currency='USD', config=config, retries=5, debug=False)

print('Getting Broker')
broker = store.getbroker()
cerebro.setbroker(broker)

# Run the strategy
cerebro.run()
