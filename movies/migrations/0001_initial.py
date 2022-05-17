# Generated by Django 4.0.4 on 2022-05-12 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('eng_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('detail_text', models.CharField(max_length=500)),
                ('age_grade', models.CharField(max_length=500)),
                ('is_subtitle', models.BooleanField()),
                ('screening_type', models.PositiveIntegerField()),
                ('preview_url', models.CharField(max_length=500)),
                ('running_time', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'movies',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'regions',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'rooms',
            },
        ),
        migrations.CreateModel(
            name='WatchPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director', models.PositiveIntegerField()),
                ('actor', models.PositiveIntegerField()),
                ('visual_beauty', models.PositiveIntegerField()),
                ('ost', models.PositiveIntegerField()),
                ('story', models.PositiveIntegerField()),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
            options={
                'db_table': 'watch_points',
            },
        ),
        migrations.CreateModel(
            name='WatchCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_time', models.DateField()),
                ('count', models.PositiveIntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
            options={
                'db_table': 'watch_counts',
            },
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=100)),
                ('longtitude', models.CharField(max_length=100)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.region')),
            ],
            options={
                'db_table': 'theaters',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_location', models.CharField(max_length=10)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.room')),
            ],
            options={
                'db_table': 'seats',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.theater'),
        ),
        migrations.CreateModel(
            name='MovieTheater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.room')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.theater')),
            ],
            options={
                'db_table': 'movie_theaters',
            },
        ),
        migrations.CreateModel(
            name='MovieImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_path', models.CharField(max_length=500, null=True)),
                ('stillcut_url', models.CharField(max_length=500)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
            options={
                'db_table': 'movie_images',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='theaters',
            field=models.ManyToManyField(through='movies.MovieTheater', to='movies.theater'),
        ),
    ]