# Generated by Django 2.0.3 on 2018-04-08 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20180408_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='bb',
            field=models.ForeignKey(default='313799043', on_delete=django.db.models.deletion.CASCADE, related_name='ccc', to='web.UserInfo'),
            preserve_default=False,
        ),
    ]
