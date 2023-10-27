from time import sleep
from baratosociais_integracao.api import get_completed_orders, add_order_on_provider
from baratosociais_integracao.database import Session
from baratosociais_integracao.models import Order


if __name__ == '__main__':
    with Session() as session:
        while True:
            orders = get_completed_orders()
            for order in orders:
                order_model = session.get(Order, order['id'])
                if order_model is None:
                    add_order_on_provider(order)
                    order_model = Order(order_id=order['id'])
                    session.add(order_model)
                    session.commit()
            sleep(30)
