from time import sleep

from sqlalchemy import select

from baratosociais_integracao.api import (
    add_order_on_provider,
    get_completed_orders,
)
from baratosociais_integracao.database import Session
from baratosociais_integracao.models import Order

if __name__ == '__main__':
    with Session() as session:
        while True:
            orders = get_completed_orders()
            breakpoint()
            for order in orders:
                query = select(Order).where(Order.order_id == order['id'])
                order_model = session.scalars(query).first()
                if order_model is None:
                    add_order_on_provider(order)
                    order_model = Order(order_id=order['id'])
                    session.add(order_model)
                    session.commit()
            sleep(30)
