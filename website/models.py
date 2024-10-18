"""
Create or customize your page models here.
"""

from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from modelcluster.fields import ParentalKey


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"

    def get_articles(self):
        # Returns all published ArticlePages beneath this index page.
        return self.get_children().specific().live().order_by('-first_published_at')

class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"


from django.db import models
from wagtailmedia.models import Media
from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from coderedcms.fields import CoderedStreamField
from coderedcms.blocks import CONTENT_STREAMBLOCKS
from coderedcms.blocks import LAYOUT_STREAMBLOCKS
from coderedcms.blocks import STREAMFORM_BLOCKS
from coderedcms.blocks import ContentWallBlock
from coderedcms.fields import CoderedStreamField
from coderedcms.fields import ColorField
from coderedcms.forms import CoderedFormBuilder
from coderedcms.forms import CoderedSubmissionsListView
from coderedcms.models.snippet_models import ClassifierTerm
from coderedcms.models.wagtailsettings_models import LayoutSettings
from coderedcms.settings import crx_settings
from coderedcms.wagtail_flexible_forms.blocks import FormFieldBlock
from coderedcms.wagtail_flexible_forms.blocks import FormStepBlock
from coderedcms.wagtail_flexible_forms.models import SessionFormSubmission
from coderedcms.wagtail_flexible_forms.models import Step
from coderedcms.wagtail_flexible_forms.models import Steps
from coderedcms.wagtail_flexible_forms.models import StreamFormJSONEncoder
from coderedcms.wagtail_flexible_forms.models import StreamFormMixin
from coderedcms.wagtail_flexible_forms.models import SubmissionRevision
from coderedcms.widgets import ClassifierSelectWidget
from wagtail.search import index
from wagtail.search.index import SearchField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.admin.panels import ObjectList
from wagtail.admin.panels import TabbedInterface
from wagtail.utils.decorators import cached_classmethod
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from coderedcms.models import CoderedWebPage

from django.db import models
from wagtailmedia.models import Media
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from coderedcms.models import CoderedWebPage
from wagtail.snippets.models import register_snippet

# Defining the snippets
@register_snippet
class AboutUsSnippet(models.Model):
    heading = models.CharField(max_length=255, help_text="Heading for the About Us section.")

    panels = [
        FieldPanel('heading'),
    ]

    class Meta:
        verbose_name = "About Us Section"
        verbose_name_plural = "About Us Sections"


@register_snippet
class ServiceSnippet(models.Model):
    title = models.CharField(max_length=255, help_text="Service title.")
    description = models.TextField(help_text="Service description.")
    icon_url = models.URLField(help_text="URL for the service icon image.")

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon_url'),
    ]

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

@register_snippet
class PatientJourneySnippet(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the patient.")
    journey_title = models.CharField(max_length=255, help_text="Title of the patient journey.")
    journey_subtitle = models.CharField(max_length=255, help_text="Subtitle of the patient journey.")
    story = models.TextField(help_text="Content of the patient story.")
    stories_link = models.URLField(help_text="URL for more patient stories.")
    read_more_text = models.CharField(max_length=255, help_text="Text for the 'Read More' button.")
    background_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background image for the patient journey section."
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('journey_title'),
        FieldPanel('journey_subtitle'),
        FieldPanel('story'),
        FieldPanel('stories_link'),
        FieldPanel('read_more_text'),
        FieldPanel('background_image'),
    ]

    class Meta:
        verbose_name = "Patient Journey"
        verbose_name_plural = "Patient Journeys"

@register_snippet
class PricingSnippet(models.Model):
    price = models.CharField(max_length=255, help_text="Price for the pricing item.")
    title = models.CharField(max_length=255, help_text="Title of the pricing item.")
    features = models.TextField(help_text="Features for the pricing item, separated by commas.")
    is_premium = models.BooleanField(default=False, help_text="Mark this pricing item as premium.")
    details_link = models.URLField(help_text="Link to more details.")

    panels = [
        FieldPanel('price'),
        FieldPanel('title'),
        FieldPanel('features'),
        FieldPanel('is_premium'),
        FieldPanel('details_link'),
    ]

    class Meta:
        verbose_name = "Pricing Item"
        verbose_name_plural = "Pricing Items"

    def get_features_list(self):
        """Returns the features as a list of strings."""
        return self.features.split(',') if self.features else []

# Modifying the CustomHomePage model to use snippets for the relevant sections
class CustomHomePage(CoderedWebPage):
    """
    Custom model for the homepage that includes a background video
    selected from uploaded media using the Wagtail media extension.
    """

    class Meta:
        verbose_name = "Custom Home Page"
        abstract = False

    template = "coderedcms/pages/home_page.html"

    # Video-related fields
    background_video = models.ForeignKey(
        Media,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background video to be displayed in the video container."
    )
    scroll_link = models.URLField(null=True, blank=True, help_text="Link for the scroll icon.")
    scroll_icon_url = models.URLField(null=True, blank=True, help_text="URL for the scroll icon image.")

    # Panels for video-related fields
    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("background_video"),
        FieldPanel("scroll_link"),
        FieldPanel("scroll_icon_url"),
    ]


@register_snippet
class PortfolioSnippet(models.Model):
    title = models.CharField(max_length=255, help_text="Title for the portfolio item.")
    description = models.TextField(help_text="Description for the portfolio item.")
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Portfolio image."
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('image'),
    ]

    class Meta:
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"
