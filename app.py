from flask import Flask, request
from sqlalchemy import select

from baratosociais_integracao.api import add_order_on_provider
from baratosociais_integracao.database import Session
from baratosociais_integracao.models import Order


def create_app():
    app = Flask(__name__)

    @app.post('/baratosociais/api')
    def add_order():
        with Session() as session:
            order = request.json
            if order['status'] == 'completed':
                query = select(Order).where(Order.order_id == order['id'])
                order_model = session.scalars(query).first()
                if order_model is None:
                    add_order_on_provider(order)
                order_model = Order(order_id=order['id'])
                session.add(order_model)
                session.commit()

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
