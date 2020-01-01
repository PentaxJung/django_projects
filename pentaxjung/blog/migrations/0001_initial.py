# Generated by Django 3.0 on 2019-12-09 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=80)),
                ('Content', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('Comments', models.PositiveSmallIntegerField(default=0, null=True)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Categories')),
                ('Tags', models.ManyToManyField(to='blog.TagModel')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20, null=True)),
                ('Password', models.CharField(max_length=32)),
                ('Content', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('Entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Entries')),
            ],
        ),
    ]
