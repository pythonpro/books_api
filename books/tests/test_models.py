from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:
    def test_shop_book_info_sell(self):
        shop_book_info = mixer.blend('books.ShopBookInfo', in_stock=1)
        shop_book_info.sell(1)
        assert shop_book_info.in_stock == 0 and shop_book_info.sold == 1

    def test_shop_book_info_sell_fail(self):
        shop_book_info = mixer.blend('books.ShopBookInfo', in_stock=1)
        with pytest.raises(ValueError):
            shop_book_info.sell(2)
