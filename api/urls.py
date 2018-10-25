from django.conf.urls import url

from .views import PublisherShopsView, ShopBookSoldView

urlpatterns = [
    # List of shops (with their info) for a publisher.
    url(r'^publisher/(?P<pk>\d+)/shops/$', PublisherShopsView.as_view()),
    # Selling one or more copies of a book in a shop.
    url(r'^shop/(?P<pk>\d+)/book-sold/$', ShopBookSoldView.as_view())
]
