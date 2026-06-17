from django.db import migrations, models
import cloudinary_storage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, blank=True)),
                ('image', models.ImageField(upload_to='hero/', storage=cloudinary_storage.storage.MediaCloudinaryStorage())),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
