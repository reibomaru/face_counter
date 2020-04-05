# Generated by Django 2.1.1 on 2020-04-05 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_count', '0005_auto_20200324_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsageList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_title', models.CharField(default='タイトル', max_length=15)),
                ('list_id', models.IntegerField(default=1)),
                ('list_img', models.ImageField(upload_to='')),
                ('list_content', models.CharField(default='', max_length=100)),
                ('list_link', models.CharField(max_length=100)),
            ],
        ),
    ]