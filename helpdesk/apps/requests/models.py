from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

class Category(models.Model):
    """Request Categories"""
    category_id = models.CharField(
        primary_key=True,
        max_length=30,
    )

    #category_parent = models.ForeignKey(
    #    Category,
    #    verbose_name="parent category",
    #    null=True,
    #    blank=True,
    #)

    category_description = models.CharField(
        _("category description"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("request category")
        verbose_name_plural = _("request categories")
        db_table = "helpdesk_request_categories"
        ordering = ("category_id",)

    def __unicode__(self):
        return u"%s" % self.category_description


class EnvironmentDetails(models.Model):
    operating_system = models.CharField(
        _("operating system"),
        max_length=255,
    )

    screen_resolution = models.CharField(
        _("screen resolution"),
        max_length=30,
    )

    browser = models.CharField(
        _("browser"),
        max_length=255,
    )

    browser_size = models.CharField(
        _("browser size"),
        max_length=30,
    )

    ip_address = models.CharField(
        _("ip address"),
        max_length=15,
    )

    color_depth = models.IntegerField(
        null=True,
        blank=True,
    )

    javascript = models.BooleanField(
        default=False,
    )

    flash_version = models.FloatField(
        null=True,
        blank=True,
    )

    cookies = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = _("environment details")
        verbose_name_plural = _("environment details")
        db_table = "helpdesk_environment_details"

    def __unicode__(self):
        return _("Environment details for a ticket")


class Ticket(models.Model):
    """The main ticketing system for the site"""

    OPEN_STATUS = 1
    REOPENED_STATUS = 2
    RESOLVED_STATUS = 3
    CLOSED_STATUS = 4
    DUPLICATE_STATUS = 5

    STATUS_CHOICES = (
        (OPEN_STATUS, _('Open')),
        (REOPENED_STATUS, _('Reopened')),
        (RESOLVED_STATUS, _('Resolved')),
        (CLOSED_STATUS, _('Closed')),
        (DUPLICATE_STATUS, _('Duplicate')),
    )

    PRIORITY_CHOICES = (
        (5, "General Question"),
        (4, "Low Priority"),
        (3, "Moderate Priority"),
        (2, "High Priority"),
        (1, "Need Help Now"),
    )

    user = models.ForeignKey(
        User,
        unique=False,
        related_name="ticket_user",
    )

    assigned_user = models.ForeignKey(
        User,
        verbose_name=_("assigned_user"),
        related_name="ticket_support_user",
        blank=True,
        null=True,
        help_text=_("The support staff user that is currently addressing the issue."),
    )

    category = models.ForeignKey(
        Category,
        verbose_name=_("category"),
        related_name="ticket_category",
        help_text=_("The support category of the ticket."),
    )

    #subcategory = models.ForeignKey(Category, verbose_name=_("subcategory"), related_name="ticket_subcategory", blank=True)

    created = models.DateTimeField(
        _("created"),
        auto_now_add=True,
        help_text=_("The date and time that the ticket was created"),
    )

    modified = models.DateTimeField(
        _("modified"),
        auto_now=True,
        help_text=_("The date and time that the ticket was last modified"),
    )

    closed = models.DateTimeField(
        _("closed"),
        null=True,
        blank=True,
        help_text=_("The date and time that the ticket was officially resolved"),
    )

    priority = models.IntegerField(
        _("priority"),
        choices=PRIORITY_CHOICES,
        default=3,
        blank=3,
        help_text=_("1 = Highest Priority, 5 = Lowest Priority"),
    )

    state = models.IntegerField(
        _("state"),
        choices=STATUS_CHOICES,
        help_text=_("The current status of a ticket."),
    )

    short_description = models.CharField(
        _("short description"),
        max_length=255,
        help_text=_("A short summary of the issue"),
        )

    description = models.TextField(
        _("description"),
        help_text=_("The complete descriptive text of the issue being experienced by the end user."),
    )

    resolution = models.TextField(
        _("resolution"),
        blank=True,
        null=True,
        help_text=_("The solution provided by support"),
    )

    environment_details = models.OneToOneField(
        EnvironmentDetails,
        verbose_name=_("environment details"),
        blank=True,
        null=True,
        help_text=_("Foreign key to an object that includes the details of the environment."),
    )

    class Meta:
        verbose_name = _("ticket")
        verbose_name_plural = _("tickets")
        db_table = "helpdesk_tickets"
        ordering = ("created",)

    def __unicode__(self):
        return u"%s" % self.short_description

    def _get_assigned_user(self):
        """ Returns the assigned support user. Retuned Unassigned if
        the ticket has not been assigned """

        if not self.assigned_user:
            return _("Unassigned")
        else:
            if self.assigned_user.name():
                return self.assigned_user.name()
            else:
                return self.assigned_user.username
    get_assigned_user = property(_get_assigned_user)


class LogEntry(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        unique=False,
        verbose_name=_("ticket"),
    )

    action_time = models.DateTimeField(
        _("action time"),
        auto_now=True,
    )

    user = models.ForeignKey(
        User,
        related_name="log_entry_user",
    )

    type = models.CharField(
        _("type"),
        max_length=30,
    )

    description = models.CharField(
        _("description"),
        max_length=255,
    )

    action_flag = models.PositiveSmallIntegerField(
        _("action flag"),
    )

    class Meta:
        verbose_name = _("log entry")
        verbose_name_plural = _("log entries")
        db_table = "helpdesk_log"
        ordering = ("ticket", "action_time",)

    def __unicode__(self):
        return _("%s" % self.type)
