from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    def __str__(self):
        return '{0.title}[{0.publisher.name}]'.format(self)


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    books = models.ManyToManyField(Book, through='ShopBookInfo')

    def __str__(self):
        return self.name


class ShopBookInfo(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Shop book info record'
        verbose_name_plural = 'Shop book info records'
        unique_together = ('shop', 'book')

    def __str__(self):
        return '{0.book.title}[{0.shop.name}]'.format(self)
