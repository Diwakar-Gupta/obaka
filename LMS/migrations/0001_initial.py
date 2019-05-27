# Generated by Django 2.2.1 on 2019-05-22 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBasicSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=20)),
                ('maxBook', models.IntegerField()),
                ('maxDay', models.IntegerField()),
                ('fineperDay', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20)),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, to='LMS.UserBasicSetting')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20)),
                ('isHOD', models.BooleanField(default=False)),
                ('subject', models.CharField(max_length=20)),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, to='LMS.UserBasicSetting')),
            ],
        ),
    ]