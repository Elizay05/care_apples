# Generated by Django 5.0.6 on 2024-07-11 23:49

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, default='categories/default.png', upload_to='categories/')),
            ],
        ),
        migrations.CreateModel(
            name='Establishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=10, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('responsible', models.CharField(max_length=100)),
                ('direction', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, default='establishments/default.png', upload_to='establishments/')),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('image', models.ImageField(blank=True, default='municipalities/default.jpg', upload_to='municipalities/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('role', models.CharField(default='User', max_length=30)),
                ('profile_picture', models.ImageField(blank=True, default='profiles/default.png', upload_to='profiles/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Apple',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=10, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('direction', models.CharField(max_length=250)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apples.municipality')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=10, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, default='services/default.png', upload_to='services/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apples.category')),
                ('establishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apples.establishment')),
            ],
        ),
        migrations.CreateModel(
            name='AppleService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apple', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apples.apple')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apples.service')),
            ],
        ),
        migrations.AddField(
            model_name='apple',
            name='services',
            field=models.ManyToManyField(related_name='apples', through='apples.AppleService', to='apples.service'),
        ),
        migrations.CreateModel(
            name='Women',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=100)),
                ('identification_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=50)),
                ('direction', models.CharField(max_length=100)),
                ('ocupation', models.CharField(max_length=100)),
                ('user_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
