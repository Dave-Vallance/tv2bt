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

from collections import deque
from datetime import datetime
import backtrader as bt
from backtrader.feed import DataBase
import queue

# ------------------------------------------------------------------------------

class TVFeed(DataBase):
    """
    TradingView Data Feed for Backtrader

    Params:
      - debug: __bool__, enable debug printing.
    """

    lines = ('signal',)

    params = (
        ('debug', False),
        ('kickstart', False)
    )

    # States for the Finite State Machine in _load
    _ST_START, _ST_LIVE, _ST_HISTORBACK, _ST_OVER = range(4)

    def __init__(self, config={}, retries=5):

        global data_queue
        from .server import data_queue

        self._data = deque() # data queue for price data

        data_queue[self.p.dataname] = queue.Queue()

        if self.p.kickstart:
            # kickstart the queue with some data
            # Next does not seem to be called until all datas have
            # at least one bar of data. We can't afford to wait for
            # signals
            data = {'symbol':''.format(self.p.dataname), 'action':0}
            data_queue[self.p.dataname].put(data)

    def start(self):
        DataBase.start(self)

        self._state = self._ST_LIVE

    def _load(self):

        if self._state == self._ST_OVER:
            return False

        while True:

            # We won't have data for a while when starting so don't raise
            # an error if we can't find the key.
            try:

                if data_queue[self.p.dataname].empty():
                    return None

                data = data_queue[self.p.dataname].get()

                if self.p.debug:
                    print('{} Data Receieved'.format(self.p.dataname))

            except KeyError as e:
                return None

            # Now we have data, process it.
            try:
                if 'DT' in data.keys():
                    dtime = datetime.strptime(data['DT'], '%Y-%m-%dT%H:%M:%SZ')
                else:
                    dtime = datetime.now()
                self.lines.datetime[0] = bt.date2num(dtime)

                if 'O' in data.keys():
                    self.lines.open[0] = data['O']

                if 'H' in data.keys():
                    self.lines.high[0] = data['H']

                if 'L' in data.keys():
                    self.lines.low[0] = data['L']

                if 'C' in data.keys():
                    self.lines.close[0]  = data['C']

                if 'V' in data.keys():
                    self.lines.volume[0] = data['V']

                if 'action' in data.keys():
                    self.lines.signal[0] = data['action']

            except (KeyError, TypeError) as e:
                print('Bad Syntax in alert. Please check')
                print('{}'.format(e))
                print('Data Supplied: {}'.format(data))
                return False

            if self.p.debug:
                print('{} Loaded OHLC Data'.format(self.p.dataname))

            return True

        return None


    def haslivedata(self):
        return self._state == self._ST_LIVE and self._data

    def islive(self):
        return True
