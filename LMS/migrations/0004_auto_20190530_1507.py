# Generated by Django 2.2.1 on 2019-05-30 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0003_auto_20190530_1437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='checkedout',
            new_name='checkedoutfrom',
        ),
    ]