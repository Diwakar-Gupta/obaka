# Generated by Django 2.2.3 on 2019-07-19 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0009_student_attentionmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='attentionMessage',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]