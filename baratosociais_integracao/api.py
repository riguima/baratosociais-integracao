import toml
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
        order_result = {
            'id': order['id'],
            'product_name': item['name'],
            'quantity': item['quantity'],
        }
        if order['status'] == 'completed':
            result.append(order_result)
    return result


def add_order_on_provider(order):
    pass
