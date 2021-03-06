# Generated by Django 2.1.5 on 2019-02-01 02:46

import _socket
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_revision.revision_field
import edc_action_item.managers
import edc_model.validators.date
import edc_utils
import edc_model_fields.fields.hostname_modification_field
import edc_model_fields.fields.userfield
import edc_model_fields.fields.uuid_auto_field
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sites", "0002_alter_domain_unique"),
        ("edc_action_item", "0016_auto_20190131_2004"),
        ("ambition_ae", "0022_auto_20190114_0250"),
    ]

    operations = [
        migrations.CreateModel(
            name="AeSusar",
            fields=[
                (
                    "created",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "user_created",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                    ),
                ),
                (
                    "hostname_modified",
                    edc_model_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                ("device_created", models.CharField(blank=True, max_length=10)),
                ("device_modified", models.CharField(blank=True, max_length=10)),
                (
                    "id",
                    edc_model_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "report_status",
                    models.CharField(
                        choices=[
                            ("open", "Open. Some information is still pending."),
                            ("closed", "Closed. This report is complete"),
                        ],
                        max_length=25,
                        verbose_name="What is the status of this report?",
                    ),
                ),
                (
                    "report_closed_datetime",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        validators=[edc_model.validators.date.datetime_not_future],
                        verbose_name="Date and time report closed.",
                    ),
                ),
                ("tracking_identifier", models.CharField(max_length=30, unique=True)),
                ("action_identifier", models.CharField(max_length=50, unique=True)),
                ("subject_identifier", models.CharField(max_length=50)),
                (
                    "parent_action_identifier",
                    models.CharField(
                        help_text="action identifier that links to parent reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "related_action_identifier",
                    models.CharField(
                        help_text="action identifier that links to related reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        validators=[edc_model.validators.date.datetime_not_future],
                        verbose_name="Report date and time",
                    ),
                ),
                (
                    "submitted_datetime",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        validators=[edc_model.validators.date.datetime_not_future],
                        verbose_name="AE SUSAR submitted on",
                    ),
                ),
                (
                    "action_item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="edc_action_item.ActionItem",
                    ),
                ),
                (
                    "ae_initial",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="ambition_ae.AeInitial",
                    ),
                ),
                (
                    "parent_action_item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="edc_action_item.ActionItem",
                    ),
                ),
                (
                    "related_action_item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="edc_action_item.ActionItem",
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="sites.Site",
                    ),
                ),
            ],
            options={"verbose_name": "AE SUSAR Report"},
            managers=[
                ("on_site", edc_action_item.managers.ActionIdentifierSiteManager()),
                ("objects", edc_action_item.managers.ActionIdentifierManager()),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalAeSusar",
            fields=[
                (
                    "created",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "user_created",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                    ),
                ),
                (
                    "hostname_modified",
                    edc_model_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                ("device_created", models.CharField(blank=True, max_length=10)),
                ("device_modified", models.CharField(blank=True, max_length=10)),
                (
                    "id",
                    edc_model_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                    ),
                ),
                (
                    "report_status",
                    models.CharField(
                        choices=[
                            ("open", "Open. Some information is still pending."),
                            ("closed", "Closed. This report is complete"),
                        ],
                        max_length=25,
                        verbose_name="What is the status of this report?",
                    ),
                ),
                (
                    "report_closed_datetime",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        validators=[edc_model.validators.date.datetime_not_future],
                        verbose_name="Date and time report closed.",
                    ),
                ),
                ("tracking_identifier", models.CharField(db_index=True, max_length=30)),
                ("action_identifier", models.CharField(db_index=True, max_length=50)),
                ("subject_identifier", models.CharField(max_length=50)),
                (
                    "parent_action_identifier",
                    models.CharField(
                        help_text="action identifier that links to parent reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "related_action_identifier",
                    models.CharField(
                        help_text="action identifier that links to related reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "history_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        validators=[edc_model.validators.date.datetime_not_future],
                        verbose_name="Report date and time",
                    ),
                ),
                (
                    "submitted_datetime",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        validators=[edc_model.validators.date.datetime_not_future],
                        verbose_name="AE SUSAR submitted on",
                    ),
                ),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "action_item",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_action_item.ActionItem",
                    ),
                ),
                (
                    "ae_initial",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="ambition_ae.AeInitial",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent_action_item",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_action_item.ActionItem",
                    ),
                ),
                (
                    "related_action_item",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_action_item.ActionItem",
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="sites.Site",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical AE SUSAR Report",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
