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

from flask import Flask, request, render_template
from threading import Thread
import queue
import ast
from .config import *
import logging


# Stop Logging Loads of informational data
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# ------------------------------------------------------------------------------
# Create Server
# ------------------------------------------------------------------------------
data_queue = dict()
server = Flask(__name__)

@server.route("/tv", methods=['POST'])
def alert():

    data = request.get_data(as_text=True)

    data = ast.literal_eval(data)
    if not isinstance(data, dict):
        print('Warning Invalid Signal Received')

        return 'Bad Request', 400

    else:
        # Check if the key has a queue, if not, make the key.
        if data['symbol'] not in data_queue.keys():
            print("WARNING: Symbol not found for alert receieved: {}".format(data['symbol']))
            return 'Bad Request', 400

        try:

            data_queue[data['symbol']].put(data)

        except KeyError as e:
            print("WARNING: Data Received not in the correct format. Missing Key: {}".format(e))
            return 'Bad Request', 400


        return 'OK', 200

server_thread = Thread(target=server.run, kwargs={'host':'0.0.0.0', 'port':PORT, 'debug': False})
server_thread.start()
