# Generated by Django 2.0.3 on 2018-04-05 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fav_type',
            field=models.IntegerField(choices=[(1, '租房'), (2, '买房'), (3, '卖房')], default=1, verbose_name='客户类型'),
        ),
    ]