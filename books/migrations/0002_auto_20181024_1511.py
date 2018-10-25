from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopbookinfo',
            options={'verbose_name': 'Book in stock', 'verbose_name_plural': 'Books in stock'},
        ),
        migrations.RenameField(
            model_name='shopbookinfo',
            old_name='stock',
            new_name='in_stock',
        ),
        migrations.AddField(
            model_name='shopbookinfo',
            name='sold',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='books.Publisher'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='books',
            field=models.ManyToManyField(related_name='shops', through='books.ShopBookInfo', to='books.Book'),
        ),
        migrations.AlterField(
            model_name='shopbookinfo',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='books.Shop'),
        ),
    ]
