from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
import pytest


class TestPublisherShopsView(APITestCase):
    @pytest.mark.django_db
    def test_can_get_publisher_shops_success_status(self):
        publisher = mixer.blend('books.Publisher')
        url = reverse('publisher_shops_view', kwargs={'pk': publisher.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_can_get_publisher_shops_proper_data(self):
        publisher1 = mixer.blend('books.Publisher')
        publisher2 = mixer.blend('books.Publisher')
        book1 = mixer.blend('books.Book', publisher=publisher1, title='Book1')
        book2 = mixer.blend('books.Book', publisher=publisher1, title='Book2')
        book3 = mixer.blend('books.Book', publisher=publisher1, title='Book3')
        book4 = mixer.blend('books.Book', publisher=publisher2, title='Book4')
        book5 = mixer.blend('books.Book', publisher=publisher2, title='Book5')
        shop1 = mixer.blend('books.Shop', name='Shop1')
        shop2 = mixer.blend('books.Shop', name='Shop2')
        shop3 = mixer.blend('books.Shop', name='Shop3')
        mixer.blend('books.ShopBookInfo', shop=shop1, book=book1, in_stock=2, sold=5)
        mixer.blend('books.ShopBookInfo', shop=shop1, book=book2, in_stock=0, sold=1)
        mixer.blend('books.ShopBookInfo', shop=shop1, book=book3, in_stock=0, sold=1)
        mixer.blend('books.ShopBookInfo', shop=shop2, book=book3, in_stock=0, sold=10)
        mixer.blend('books.ShopBookInfo', shop=shop2, book=book4, in_stock=7, sold=0)
        mixer.blend('books.ShopBookInfo', shop=shop3, book=book5, in_stock=7, sold=1)
        mixer.blend('books.ShopBookInfo', shop=shop3, book=book2, in_stock=1, sold=0)
        mixer.blend('books.ShopBookInfo', shop=shop3, book=book3, in_stock=2, sold=0)
        url = reverse('publisher_shops_view', kwargs={'pk': publisher1.pk})
        response = self.client.get(url)
        assert response.json() == {'shops': [{'id': 3, 'name': 'Shop3', 'books_sold_count': 1,
                                              'books_in_stock': [{'id': 2, 'title': 'Book2', 'copies_in_stock': 1},
                                                                 {'id': 3, 'title': 'Book3', 'copies_in_stock': 2}]},
                                             {'id': 1, 'name': 'Shop1', 'books_sold_count': 7,
                                              'books_in_stock': [{'id': 1, 'title': 'Book1', 'copies_in_stock': 2}]}]}


class TestShopBookSoldView(APITestCase):
    @pytest.mark.django_db
    def test_can_get_shop_book_sold_success_status_and_response_data(self):
        shop = mixer.blend('books.Shop')
        book = mixer.blend('books.Book')
        mixer.blend('books.ShopBookInfo', shop=shop, book=book, in_stock=1)
        url = reverse('shop_book_sold_view', kwargs={'pk': shop.pk})
        response = self.client.post(url, {'book_id': book.id, 'sold': 1}, format='json')
        assert response.status_code == status.HTTP_200_OK and response.json() == 'OK'

    @pytest.mark.django_db
    def test_can_get_shop_book_sold_fail_status_and_response_data(self):
        shop = mixer.blend('books.Shop')
        book = mixer.blend('books.Book')
        mixer.blend('books.ShopBookInfo', shop=shop, book=book, in_stock=1)
        url = reverse('shop_book_sold_view', kwargs={'pk': shop.pk})
        response = self.client.post(url, {'book_id': book.id, 'sold': 2}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST and response.json() == {
            'non_field_errors': ['Wrong sold copies number/insufficient books in stock.']}
