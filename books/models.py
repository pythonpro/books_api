from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return '{0.title}[{0.publisher.name}]'.format(self)


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    books = models.ManyToManyField(Book, related_name='shops', through='ShopBookInfo')

    def __str__(self):
        return self.name


class ShopBookInfo(models.Model):
    """
    Intermediary model (with extra info) for shop-book M2M relation.
    """
    shop = models.ForeignKey(Shop, related_name='stock', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    in_stock = models.PositiveIntegerField()
    sold = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Book in stock'
        verbose_name_plural = 'Books in stock'
        unique_together = ('shop', 'book')

    def __str__(self):
        return self.book.__str__()

    def sell(self, copies):  # Sell `copies` (integer) of a book, check availability.
        if copies > self.in_stock:
            raise ValueError
        self.in_stock -= copies
        self.sold += copies
        self.save(update_fields=['in_stock', 'sold'])
