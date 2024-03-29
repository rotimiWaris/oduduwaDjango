# Generated by Django 3.0.8 on 2020-09-06 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20200905_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='class_name',
            field=models.CharField(blank=True, choices=[('JSS1', 'JSS1'), ('JSS2', 'JSS2'), ('JSS3', 'JSS3'), ('SSS1', 'SSS1'), ('SSS2', 'SSS2'), ('SSS3', 'SSS3'), ('Other Class', 'Other Class')], max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(blank=True, choices=[('Student', 'Student'), ('Old Student', 'Old Student'), ('Teacher', 'Teacher'), ('Principal', 'Principal'), ('Vice-Principal', 'Vice-Principal'), ('Non-Member', 'Non-Member')], max_length=225, null=True),
        ),
    ]
