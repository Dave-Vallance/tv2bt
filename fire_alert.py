import requests
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Test Program to trigger alerts')

    parser.add_argument('--port',
                        default=8123,
                        help='Port of the server')

    parser.add_argument('--endpoint',
                        default='tv',
                        help='endpoint to target')

    return parser.parse_args()

args = parse_args()

while True:
    ticker = input('Ticker: ')
    ohlcv = input('Send OHLCV? (y/n): ')
    action = input('Action: ')

    if action in ['q', 'quit']:
        break

    if ohlcv.lower() == 'y':
        o = int(input('Open: '))
        h = int(input('High: '))
        l = int(input('Low: '))
        c = int(input('Close: '))
        v = int(input('Volume: '))

        data = {
            'symbol': ticker, 'O': o, 'H': h, 'L': l, 'C': c, 'V': v, 'action': int(action)
        }

    elif ohlcv.lower() == 'n':

        data = {
            'symbol': ticker, 'action': int(action)
        }

    else:
        print('OHLCV input not recognized. Try again')

    # Send the request!
    resp = requests.post('http://0.0.0.0:{}/{}'.format(args.port, args.endpoint), json=data)
    print('Status Code: {}'.format(resp.status_code))
    print('Response: {}'.format(resp.text))
