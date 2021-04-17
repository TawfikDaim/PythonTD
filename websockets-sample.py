# tested in Python 3.6+
# required packages: websockets, requests

import websockets, asyncio, requests, secrets, string, json
from pprint import pprint

# copy your (24-hour) token here
TOKEN = 'eyJhbGciOiJFUzI1NiIsIng1dCI6IjhGQzE5Qjc0MzFCNjNFNTVCNjc0M0QwQTc5MjMzNjZCREZGOEI4NTAifQ.eyJvYWEiOiI3Nzc3NSIsImlzcyI6Im9hIiwiYWlkIjoiMTA5IiwidWlkIjoiNEFhfDNIUEk3S3JVeXxuZkxPYUl2dz09IiwiY2lkIjoiNEFhfDNIUEk3S3JVeXxuZkxPYUl2dz09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiNmZjNGYwMmFkNjA4NDQyMDgwMjBlN2E1NDBkMTcyOTMiLCJkZ2kiOiI4NCIsImV4cCI6IjE2MTg2NjczMTAifQ.IUsYuER8taagbQnBUP5_RR4H8Lhu1Hsod_HG5Y9nPeIZDi5SEmBwSul_SHZ43VGuD9lo1tmXPZv7HFz6XZbYaA'

# create a random string for context ID and reference ID
CONTEXT_ID = secrets.token_urlsafe(10)
REF_ID = secrets.token_urlsafe(5)


def create_subscription(context_id, ref_id, token):
  
    response = requests.get(
        'https://gateway.saxobank.com/sim/openapi/port/v1/balances/me',
        headers={'Authorization': 'Bearer ' + token},
    )
    print (response.text)
    # pprint(decode_message(response))

    response = requests.get(
         'https://gateway.saxobank.com/sim/openapi/port/v1/orders/me',
          headers={'Authorization': 'Bearer ' + token},
    )
    print ('/n'),
    pprint (response.text)
  
    response = requests.post(
        'https://gateway.saxobank.com/sim/openapi/trade/v2/orders',
        headers={'Authorization': 'Bearer ' + token},
        json={
            "Orders": [
                {
                "AccountKey": "4Aa|3HPI7KrUy|nfLOaIvw==",
                "ManualOrder": True,
                "Amount": 100000.0,
                "AssetType": "FxSpot",
                "BuySell": "Buy",
                "OrderDuration": {
                    "DurationType": "GoodTillCancel"
            },
            "OrderPrice": 130.7,
            "OrderType": "Limit",
            "Uic": 18
            },
            {
            "AccountKey": "4Aa|3HPI7KrUy|nfLOaIvw==",
            "Amount": 100000.0,
            "ManualOrder": True,
            "AssetType": "FxSpot",
            "BuySell": "Buy",
            "OrderDuration": {
                "DurationType": "GoodTillCancel"
            },
            "OrderPrice": 132.2,
            "OrderType": "Stop",
            "Uic": 18
            }
        ],
        "WithAdvice": False
        }
    )
    print(response.status_code)
    print(response.text)

    response = requests.post(
        'https://gateway.saxobank.com/sim/openapi/trade/v1/infoprices/subscriptions',
        headers={'Authorization': 'Bearer ' + token},
        json={
            'Arguments': {
		        'Uics': 21,
		        'AssetType': 'FxSpot'
	        },
	        'ContextId': context_id,
	        'ReferenceId': ref_id
        }
    )

    if response.status_code == 201:
        print('Successfully created subscription')
        print('Snapshot data:')
        pprint(response.json()['Snapshot'])
        print('Now receiving delta updates:')
    elif response.status_code == 401:
        print('Error setting up subscription - check TOKEN value')
        exit()


def decode_message(message):
    msg_id = int.from_bytes(message[0:8], byteorder='little')
    ref_id_length = message[10]
    ref_id = message[11:11+ref_id_length].decode()
    payload_format = message[11+ref_id_length]
    payload_size = int.from_bytes(message[12+ref_id_length:16+ref_id_length], byteorder='little')
    payload = message[16+ref_id_length:16+ref_id_length+payload_size].decode()
    return json.loads(payload)


async def streamer(context_id, ref_id, token):
    url = f'wss://streaming.saxobank.com/sim/openapi/streamingws/connect?contextId={context_id}'
    headers = {'Authorization': f'Bearer {token}'}

    async with websockets.connect(url, extra_headers=headers) as websocket:
        async for message in websocket:
            pprint(decode_message(message))


if __name__ == "__main__":

    try:
        create_subscription(CONTEXT_ID, REF_ID, TOKEN)
        asyncio.get_event_loop().run_until_complete(streamer(CONTEXT_ID, REF_ID, TOKEN))
    except KeyboardInterrupt:
        print('User interrupted the interpreter - closing connection.')
        exit()