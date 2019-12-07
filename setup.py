from setuptools import setup

setup(
   name='tv2bt',
   version='1.0',
   description='A bridge between Tradingview alerts and Backtrader',
   url='https://github.com/Dave-Vallance/tv2bt',
   author='Dave Vallance',
   author_email='dave@backtest-rookies.com',
   license='MIT',
   packages=['tv2bt'],
   install_requires=['backtrader','flask'],
)
