# Generated by Django 2.2.1 on 2019-05-29 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('LMS', '0019_delete_issue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.PositiveIntegerField()),
                ('is_returned', models.BooleanField(default=False)),
                ('countrenewal', models.PositiveIntegerField(default=0)),
                ('checkedout', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('duedate', models.DateTimeField(auto_now=True)),
                ('mail_send', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS.Book')),
                ('checkoutfrom', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LMS.Faculty')),
                ('member_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
    ]
