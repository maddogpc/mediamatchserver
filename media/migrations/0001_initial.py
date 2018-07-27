# Generated by Django 2.0.7 on 2018-07-26 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=20)),
                ('author', models.CharField(default='unauthored', max_length=20)),
                ('profiles', models.ManyToManyField(to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='MediaShort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator_or_title', models.CharField(default='blank', max_length=20)),
                ('content_type', models.CharField(default='blank', max_length=20)),
                ('profiles', models.ManyToManyField(to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('widget_type', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=20)),
                ('image_size', models.CharField(default='none provided', max_length=50)),
                ('link', models.CharField(default='none provided', max_length=50)),
                ('content', models.TextField(default='')),
                ('medias', models.ManyToManyField(to='media.Media')),
                ('profiles', models.ManyToManyField(to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='WidgetFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
                ('widgets', models.ManyToManyField(to='media.Widget')),
            ],
        ),
    ]
