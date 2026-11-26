import pytest
from unittest.mock import MagicMock, patch

from warehouse.services.order_service import OrderService
from warehouse.models import Order, OrderLine
from warehouse.errors import InvalidRequestError


class TestOrderService:
    @pytest.fixture
    def mock_store(self):
        store = MagicMock()
        store.products = {
            "SKU1": MagicMock(quantity_on_hand=100, unit_price=10.0)
        }
        store.next_order_id = MagicMock(side_effect=[1, 2, 3])
        store.orders = {}
        return store

    def test_place_order_sends_email(self, mock_store):
        service = OrderService(mock_store)
        with patch.object(service, '_send_confirmation_email') as mock_send:
            lines = [("SKU1", 1)]
            service.place_order(lines)
            assert mock_send.called
            # Verify that an Order object was passed to the email function
            order_arg = mock_send.call_args[0][0]
            assert isinstance(order_arg, Order)
            assert order_arg.status == "placed"