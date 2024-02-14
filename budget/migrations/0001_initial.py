# Generated by Django 5.0.1 on 2024-02-06 09:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('amount', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('expense', 'expense'), ('income', 'income')], default='expense', max_length=200)),
                ('category', models.CharField(choices=[('fuel', 'fuel'), ('food', 'food'), ('entertainment', 'entertainment'), ('emi', 'emi'), ('bills', 'bills'), ('miscellaneous', 'miscellaneous')], default='miscellaneous', max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
