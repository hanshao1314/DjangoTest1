# Generated by Django 2.1.8 on 2019-09-09 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Goods',
        ),
        migrations.DeleteModel(
            name='GoodsType',
        ),
        migrations.DeleteModel(
            name='LoginUser',
        ),
    ]
