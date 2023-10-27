import re

import toml
from httpx import Client
from woocommerce import API

secrets = toml.load(open('.secrets.toml'))

wcapi = API(
    url=secrets['STORE_URL'],
    consumer_key=secrets['CONSUMER_KEY'],
    consumer_secret=secrets['CONSUMER_SECRET'],
    wp_api=True,
    version='wc/v3',
)


def get_completed_orders():
    result = []
    for order in wcapi.get('orders').json():
        item = order['line_items'][0]
        quantity = int(re.findall(r'^\d+ ', item['name'].replace('.', ''))[0])
        order_result = {
            'id': order['id'],
            'product_name': item['name'],
            'quantity': quantity,
        }
        if order['status'] == 'completed':
            result.append(order_result)
    return result


def add_order_on_provider(order):
    service = 784 if 'instagram' in order['product_name'].lower() else 662
    with Client() as client:
        response = client.post(
            'https://baratosociais.com/api/v2',
            json={
                'key': secrets['BARATOSOCIAIS_API_KEY'],
                'action': 'add',
                'service': service,
                'link': '',
                'quantity': order['quantity'],
            },
        )
        return response.json()['order']
