# Generated by Django 5.0.1 on 2024-02-03 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_rename_course_id_studentmark_course_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentmark',
            old_name='course',
            new_name='course_id',
        ),
        migrations.RenameField(
            model_name='studentmark',
            old_name='stu',
            new_name='stu_id',
        ),
    ]
