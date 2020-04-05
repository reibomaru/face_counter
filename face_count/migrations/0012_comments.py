# Generated by Django 2.1.1 on 2020-04-05 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_count', '0011_usagelist_list_link_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('mail', models.CharField(max_length=30)),
                ('comment', models.TextField()),
                ('created_data', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
