# Generated by Django 5.1.4 on 2025-01-25 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EPI_App', '0004_alter_productscheme_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productscheme',
            name='end_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productscheme',
            name='product_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='productscheme',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
