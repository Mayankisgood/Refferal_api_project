# Generated by Django 5.0.4 on 2024-04-08 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_user_detail_referral_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_detail",
            name="referral_code",
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
