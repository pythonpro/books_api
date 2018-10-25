from rest_framework import serializers


class ShopBookInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for `books_in_stock` nested list of shops list in PublisherShopsInfoSerializer.
    """

    def to_representation(self, obj):
        return {
            'id': obj.book_id,
            'title': obj.book.title,
            'copies_in_stock': obj.in_stock
        }


class PublisherShopsInfoSerializer(serializers.Serializer):
    """
    Shop info serializer.
    Supposed to be used with `many=True`.
    Requires publisher instance passed via context.
    """
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    books_sold_count = serializers.IntegerField()
    books_in_stock = serializers.SerializerMethodField()

    def get_books_in_stock(self, obj):
        """Prepare data for `books_in_stock` field."""
        qs = obj.stock.filter(book__publisher=self.context['publisher'], in_stock__gt=0).select_related('book')
        serializer = ShopBookInfoSerializer(qs, many=True)
        return serializer.data


class BooksSoldSerializer(serializers.Serializer):
    """
    Serializer for selling book(s) API endpoint view.
    """
    book_id = serializers.IntegerField()
    sold = serializers.IntegerField(min_value=1)
