# Generated by Django 4.1.1 on 2022-10-21 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapi', '0007_room_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='product',
            field=models.CharField(choices=[('WorkflowAi', 'WorkflowAi'), ('DigitalQ', 'DigitalQ'), ('DowellChat', 'DowellChat'), ('WifiQrCode', 'WifiQrCode'), ('UxLive', 'UxLive')], max_length=20),
        ),
    ]
