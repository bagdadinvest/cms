# Generated by Django 5.1.2 on 2024-10-18 11:55

import coderedcms.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderedcms', '0041_remove_layoutsettings_frontend_theme'),
        ('wagtailimages', '0026_delete_uploadedimage'),
        ('wagtailmedia', '0004_duration_optional_floatfield'),
        ('website', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomHomePage',
            fields=[
                ('coderedpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='coderedcms.coderedpage')),
                ('body', coderedcms.fields.CoderedStreamField(blank=True, block_lookup={}, null=True)),
                ('subtitle', models.CharField(blank=True, help_text='Subtitle for the homepage.', max_length=255, null=True)),
                ('additional_text', models.TextField(blank=True, help_text='Additional text content for the homepage.', null=True)),
                ('scroll_link', models.URLField(blank=True, help_text='Link for the scroll icon.', null=True)),
                ('scroll_icon_url', models.URLField(blank=True, help_text='URL for the scroll icon image.', null=True)),
                ('portfolio_items', coderedcms.fields.CoderedStreamField(blank=True, block_lookup={}, help_text='Items to be displayed in the portfolio section.', null=True)),
                ('about_us_heading', models.CharField(blank=True, help_text='Heading for the About Us section.', max_length=255, null=True)),
                ('services', coderedcms.fields.CoderedStreamField(blank=True, block_lookup={}, help_text='Services provided by the organization.', null=True)),
                ('patient_name', models.CharField(blank=True, help_text='Name of the patient for the patient story.', max_length=255, null=True)),
                ('patient_journey_title', models.CharField(blank=True, help_text='Title for the patient journey.', max_length=255, null=True)),
                ('patient_journey_subtitle', models.CharField(blank=True, help_text='Subtitle for the patient journey.', max_length=255, null=True)),
                ('patient_story', models.TextField(blank=True, help_text='Patient story content.', null=True)),
                ('patient_stories_link', models.URLField(blank=True, help_text='Link to more patient stories.', null=True)),
                ('read_more_text', models.CharField(blank=True, help_text="Text for the 'Read More' button.", max_length=255, null=True)),
                ('pricing_items', coderedcms.fields.CoderedStreamField(blank=True, block_lookup={}, help_text='Pricing items to be displayed in the pricing tables section.', null=True)),
                ('details_text', models.CharField(blank=True, help_text="Text for the 'Details' button.", max_length=255, null=True)),
                ('background_video', models.ForeignKey(blank=True, help_text='Background video to be displayed in the video container.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailmedia.media')),
                ('more_about_us_background_image', models.ForeignKey(blank=True, help_text='Background image for the More About Us section.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Custom Home Page',
                'abstract': False,
            },
            bases=('coderedcms.coderedpage',),
        ),
    ]
