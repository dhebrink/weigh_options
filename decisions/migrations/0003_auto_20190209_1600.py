# Generated by Django 2.0 on 2019-02-09 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decisions', '0002_auto_20190209_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date_added',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='prompt',
            name='date_deleted',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='date_deleted',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='templatecopy',
            name='date_deleted',
            field=models.DateTimeField(null=True),
        ),
    ]
