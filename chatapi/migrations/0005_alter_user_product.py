# Generated by Django 4.1.1 on 2022-10-07 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapi', '0004_alter_user_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='product',
            field=models.CharField(choices=[('WorkflowAi', 'WorkflowAi'), ('DigitalQ', 'DigitalQ'), ('DowellChat', 'DowellChat')], max_length=20),
        ),
    ]
