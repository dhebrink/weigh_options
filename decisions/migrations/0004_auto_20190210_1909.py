# Generated by Django 2.0 on 2019-02-11 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decisions', '0003_auto_20190209_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='comments',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='prompt',
            name='answer_options',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
    ]