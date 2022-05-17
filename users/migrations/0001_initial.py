# Generated by Django 4.0.4 on 2022-05-17 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kakao_id', models.PositiveBigIntegerField(unique=True)),
                ('nickname', models.CharField(max_length=50)),
                ('profile_image_url', models.CharField(max_length=200)),
                ('profile_image_storage_path', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=150, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
