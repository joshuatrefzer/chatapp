# Generated by Django 5.0.3 on 2024-04-04 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_message_reactions_alter_thread_reactions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='reactions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
