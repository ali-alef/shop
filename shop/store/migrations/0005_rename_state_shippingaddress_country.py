# Generated by Django 4.0.3 on 2022-08-12 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_order_date_create_alter_order_transaction_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='state',
            new_name='country',
        ),
    ]
