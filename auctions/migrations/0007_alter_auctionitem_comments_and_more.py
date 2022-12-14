# Generated by Django 4.0.4 on 2022-11-02 18:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auctionitem_watching_alter_auctionitem_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitem',
            name='comments',
            field=models.ManyToManyField(blank=True, to='auctions.comment'),
        ),
        migrations.AlterField(
            model_name='auctionitem',
            name='watching',
            field=models.ManyToManyField(blank=True, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
