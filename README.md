# tv2bt
A python package that bridges Tradingview alerts to backtrader.

A data feed for Backtrader which will allow you to receive both trade signals
and/orOHLCV data from Tradingview. You can send trading signals from the
plethora of open source strategies and indicators on the platform. Or perhaps
you are struggling to find some good, reliable intra-day data. Tradingview
has plenty we can now access in Backtrader.

## Introduction
for a full overview and gentle introduction please see: https://backtest-rookies.com/2019/11/22/tv2bt-tradingview-to-backtrader-module/

## Installation
Note: Developed for Python 3.x only.

Download and run `python setup.py install develop` or `python3 setup.py install develop`

A simple Flask server is used to receive the webhooks from Tradingview. This means, that you will need to configure some port forwarding on your router to the machine running the datafeed. Redirect port 80(HTTP) to port 8123. If you don't do this, no alerts will be received.

## Testing  
If you are having trouble receiving alerts, a special test script has been provided to push alerts to the system in the same manner that Tradingview would. First, fire up the `example_strategy.py` and then run `alert_tests.py`. You should see some test data pushed to the system that looks like this:

If you are able to see these alerts but you are not seeing Tradingview alerts, check your alert settings at Tradingview side or your port forward settings. If you don't see the alerts when running this script, ensure you have not made any changes to `example_strategy.py`

## Donations Welcome, but not required!

Download The Brave Browswer. A privacy focused browser that supports content
creators: https://brave.com/dav470

Tips are are lovely too.

BTC: 3HxNVyh5729ieTfPnTybrtK7J7QxJD9gjD

ETH: 0x9a2f88198224d59e5749bacfc23d79507da3d431

XMR: 42nzsthr1C79nr6TYP2eaW7XMAdS5Rz1Ad9KVSCnCrn9RA9dthWYrHLTyfnULnCmXkA5mL3iF1EX9H7hK4XxUszyAoQjjBa
