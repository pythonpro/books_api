from django.urls import reverse, resolve


class TestUrls:
    def test_publisher_shops_view_url(self):
        path = reverse('publisher_shops_view', kwargs={'pk': 1})
        assert path == '/api/publisher/1/shops/'

    def test_shop_book_sold_view_url(self):
        path = reverse('shop_book_sold_view', kwargs={'pk': 1})
        assert path == '/api/shop/1/book-sold/'
