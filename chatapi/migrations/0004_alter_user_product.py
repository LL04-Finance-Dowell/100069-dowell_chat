# Generated by Django 4.1.1 on 2022-10-06 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapi', '0003_user_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='product',
            field=models.CharField(choices=[('Workflow AI', 'Workflow AI'), ('Digital Q', 'Digital Q'), ('Wifi QR code', 'Wifi QR code'), ('Dowell Chat', 'Dowell Chat')], max_length=20),
        ),
    ]
