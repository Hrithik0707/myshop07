# Generated by Django 2.2.6 on 2020-05-28 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('img', models.ImageField(default='default.png', upload_to='pics')),
                ('des', models.TextField()),
                ('price', models.IntegerField()),
            ],
        ),
    ]