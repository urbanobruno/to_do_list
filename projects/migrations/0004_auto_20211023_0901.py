# Generated by Django 3.2.5 on 2021-10-23 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210925_1829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['updated_at', 'created_at'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AddField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=75),
        ),
    ]