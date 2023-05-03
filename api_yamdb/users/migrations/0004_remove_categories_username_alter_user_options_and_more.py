# Generated by Django 4.0 on 2023-05-01 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_first_name_alter_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='username',
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('admin', 'admin'), ('moderator', 'moderator')], default='user', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, max_length=254),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('username__iexact', 'me'), _negated=True), name='unique_name_owner'),
        ),
        migrations.DeleteModel(
            name='Categories',
        ),
    ]
