# Generated by Django 2.2.1 on 2019-05-28 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LMS', '0013_auto_20190528_0856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('is_issued', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ISBN',
            fields=[
                ('isbn', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=30)),
                ('publisher', models.CharField(max_length=30)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserBasicSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('maxBook', models.PositiveSmallIntegerField()),
                ('maxDay', models.IntegerField()),
                ('finePerDay', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20)),
                ('count_books', models.PositiveIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, to='LMS.UserBasicSetting')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.PositiveIntegerField()),
                ('is_returned', models.BooleanField(default=False)),
                ('issue_day', models.DateTimeField(auto_now=True)),
                ('return_day', models.DateTimeField(auto_now=True)),
                ('mail_send', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS.Book')),
                ('member_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20)),
                ('isHOD', models.BooleanField(default=False)),
                ('subject', models.CharField(max_length=20)),
                ('count_books', models.PositiveIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, to='LMS.UserBasicSetting')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS.ISBN'),
        ),
    ]
