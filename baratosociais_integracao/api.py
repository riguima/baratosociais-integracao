import re

import toml
from httpx import Client

secrets = toml.load(open('.secrets.toml'))


def add_order_on_provider(order):
    item = order['line_items'][0]
    service = 784 if 'instagram' in item['name'].lower() else 662
    quantity = int(re.findall(r'^\d+ ', item['name'].replace('.', ''))[0])
    with Client() as client:
        response = client.post(
            'https://baratosociais.com/api/v2',
            json={
                'key': secrets['BARATOSOCIAS_API_KEY'],
                'action': 'add',
                'service': service,
                'link': order['meta_data'][0]['value'],
                'quantity': quantity,
            },
        )
        return response.json()['order']
