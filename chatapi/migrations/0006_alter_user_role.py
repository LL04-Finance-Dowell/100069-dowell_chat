# Generated by Django 4.1.1 on 2022-10-07 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapi', '0005_alter_user_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('User', 'User'), ('Proj_lead', 'Proj_lead')], max_length=10),
        ),
    ]
