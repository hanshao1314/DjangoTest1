# Generated by Django 2.1.8 on 2019-09-16 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0003_auto_20190911_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_name', models.CharField(max_length=32)),
                ('goods_number', models.IntegerField()),
                ('goods_price', models.FloatField()),
                ('goods_picture', models.CharField(max_length=32)),
                ('goods_total', models.FloatField()),
                ('goods_id', models.IntegerField()),
                ('cart_user', models.IntegerField()),
            ],
        ),
    ]