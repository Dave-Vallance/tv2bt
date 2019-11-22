import requests

while True:
    ticker = input('Ticker: ')
    action = input('Action: ')

    if action in ['q','quit']:
        break

    data = {
        'symbol':ticker, 'action':int(action)
        }

    resp = requests.post('http://0.0.0.0:8123/tv', json=data)
    print('Status Code: {}'.format(resp.status_code))
    print('Response: {}'.format(resp.text))
