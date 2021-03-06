# Generated by Django 4.0.4 on 2022-05-05 14:19

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
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
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profession', models.IntegerField(choices=[(-1, 'Niezdefiniowano'), (0, 'Inspektor'), (1, 'Specjalista'), (2, 'Zast??pca dyrektora'), (3, 'Dyrektor')], default=-1)),
                ('date_employed', models.DateField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=210)),
                ('region', models.IntegerField(choices=[(-1, 'Niezdefiniowano'), (2, 'Dolno??l??skie'), (4, 'Kujawsko-Pomorskie'), (6, 'Lubelskie'), (8, 'Lubuskie'), (10, '????dzkie'), (12, 'Ma??opolskie'), (14, 'Mazowieckie'), (16, 'Opolskie'), (18, 'Podkarpackie'), (20, 'Podlaskie'), (22, 'Pomorskie'), (24, '??l??skie'), (26, '??wi??tokrzyskie'), (28, 'Warmi??sko-Mazurskie'), (30, 'Wielkopolskie'), (32, 'Zachodniopomorskie')], default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scope', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Subcontractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mail', models.CharField(max_length=150)),
                ('tax_connection', models.CharField(max_length=15)),
                ('min_contract_value', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('max_contract_value', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('scope', models.ManyToManyField(default=-1, to='offers_manager.scope')),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('net_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date_begin', models.DateField()),
                ('date_finish', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('related_workers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('net_value', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('accepted_value', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('vat_rate', models.IntegerField(choices=[(1, 'Zwolniony'), (2, 0.0), (3, 0.05), (4, 0.08), (5, 0.23)], default=5)),
                ('description', models.TextField(default=None, null=True)),
                ('accepted_by', models.ManyToManyField(related_name='accepted_by', to='offers_manager.subcontractor')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='offers_manager.plant')),
                ('related_workers', models.ManyToManyField(related_name='related_workers', to=settings.AUTH_USER_MODEL)),
                ('scope', models.ManyToManyField(to='offers_manager.scope')),
                ('subcontractors', models.ManyToManyField(related_name='subcontractors', to='offers_manager.subcontractor')),
                ('winner', models.ManyToManyField(related_name='winner', to='offers_manager.subcontractor')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.IntegerField(choices=[(-1, 'Niezdefiniowano'), (0, 'Polska'), (1, 'Niemcy'), (2, 'Norwegia'), (3, 'Szwecja'), (4, 'Dania'), (5, 'Norwegia')], default=-1)),
                ('post_code', models.CharField(max_length=10)),
                ('street', models.CharField(max_length=150)),
                ('house_number', models.CharField(max_length=7)),
                ('flat_number', models.CharField(max_length=7, null=True)),
                ('acceptable_radius', models.IntegerField(null=True)),
                ('city', models.ManyToManyField(default=-1, to='offers_manager.city')),
                ('plant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='offers_manager.plant')),
                ('subcontractor', models.ManyToManyField(to='offers_manager.subcontractor')),
            ],
        ),
    ]
