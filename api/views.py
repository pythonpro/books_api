from django.db import IntegrityError
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PublisherShopsInfoSerializer, BooksSoldSerializer
from books.models import Publisher, Shop


class PublisherShopsView(GenericAPIView):
    """
    API endpoint that returns a list of shops for a specific publisher
     selling at least one book of that publisher.
    """
    queryset = Publisher.objects.all()

    def get(self, request, *args, **kwargs):
        publisher = self.get_object()

        # List of shop ids used in further annotating and sorting.
        shop_ids = Shop.objects.only('id').filter(stock__book__publisher=publisher, stock__in_stock__gt=0).values_list(
            'id', flat=True)
        # Queryset with shops properly annotated and ordered.
        shops = Shop.objects.filter(id__in=shop_ids).annotate(books_sold_count=Sum('stock__sold')).order_by(
            'books_sold_count')

        serializer = PublisherShopsInfoSerializer(shops, many=True, context={'publisher': publisher})
        return Response({'shops': serializer.data})


class ShopBookSoldView(APIView):
    """
    API endpoint for a specific shop.
     It marks one or multiple copies of a book as sold.
    """

    def post(self, request, *args, **kwargs):
        try:
            shop = Shop.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, shop)

        serializer = BooksSoldSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            sold = serializer.validated_data['sold']
            try:
                book_info_obj = shop.stock.get(book_id=book_id, in_stock__gt=0)
            except ObjectDoesNotExist:
                result = {'non_field_errors': ['Wrong book id/no such book in stock.']}
                http_status = status.HTTP_400_BAD_REQUEST
            else:
                try:
                    book_info_obj.sell(sold)
                except (ValueError, IntegrityError):
                    result = {'non_field_errors': ['Wrong sold copies number/insufficient books in stock.']}
                    http_status = status.HTTP_400_BAD_REQUEST
                else:
                    result = None
                    http_status = status.HTTP_200_OK
        else:
            result = serializer.errors
            http_status = status.HTTP_400_BAD_REQUEST
        return Response(result, status=http_status)
