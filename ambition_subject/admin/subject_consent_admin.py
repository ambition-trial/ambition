from ambition_screening.models.subject_screening import SubjectScreening
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from edc_consent.modeladmin_mixins import ModelAdminConsentMixin
from edc_constants.constants import ABNORMAL
from edc_model_admin import audit_fieldset_tuple, SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_identifier import is_subject_identifier_or_raise, SubjectIdentifierError

from ..admin_site import ambition_subject_admin
from ..forms import SubjectConsentForm
from ..models import SubjectConsent, SubjectVisit


@admin.register(SubjectConsent, site=ambition_subject_admin)
class SubjectConsentAdmin(
    ModelAdminConsentMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = SubjectConsentForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "screening_identifier",
                    "subject_identifier",
                    "first_name",
                    "last_name",
                    "initials",
                    "language",
                    "is_literate",
                    "witness_name",
                    "consent_datetime",
                    "dob",
                    "is_dob_estimated",
                    "guardian_name",
                    "identity",
                    "identity_type",
                    "confirm_identity",
                    "is_incarcerated",
                )
            },
        ),
        (
            "Sample collection and storage",
            {"fields": ("may_store_samples", "may_store_genetic_samples")},
        ),
        (
            "Review Questions",
            {
                "fields": (
                    "consent_reviewed",
                    "study_questions",
                    "assessment_score",
                    "consent_signature",
                    "consent_copy",
                ),
                "description": "The following questions are directed to the interviewer.",
            },
        ),
        audit_fieldset_tuple,
    )

    search_fields = ("subject_identifier", "screening_identifier", "identity")

    radio_fields = {
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "consent_signature": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL,
        "is_literate": admin.VERTICAL,
        "language": admin.VERTICAL,
        "may_store_genetic_samples": admin.VERTICAL,
        "may_store_samples": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
    }

    def delete_view(self, request, object_id, extra_context=None):
        """Prevent deletion if SubjectVisit objects exist.
        """
        extra_context = extra_context or {}
        obj = SubjectConsent.objects.get(id=object_id)
        try:
            protected = [
                SubjectVisit.objects.get(subject_identifier=obj.subject_identifier)
            ]
        except ObjectDoesNotExist:
            protected = None
        except MultipleObjectsReturned:
            protected = SubjectVisit.objects.filter(
                subject_identifier=obj.subject_identifier
            )
        extra_context.update({"protected": protected})
        return super().delete_view(request, object_id, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        """Returns a form after replacing 'participant' with
        'next of kin'.
        """
        form = super().get_form(request, obj=obj, **kwargs)
        if obj:
            screening_identifier = obj.screening_identifier
        else:
            screening_identifier = request.GET.get("screening_identifier")
        try:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=screening_identifier
            )
        except ObjectDoesNotExist:
            pass
        else:
            if subject_screening.mental_status == ABNORMAL:
                form = self.replace_label_text(
                    form, "participant", "next of kin", skip_fields=["is_incarcerated"]
                )
        return form

    def get_next_options(self, request=None, **kwargs):
        """Returns the key/value pairs from the "next" querystring
        as a dictionary.
        """
        next_options = super().get_next_options(request=request, **kwargs)
        try:
            is_subject_identifier_or_raise(next_options["subject_identifier"])
        except SubjectIdentifierError:
            next_options["subject_identifier"] = SubjectScreening.objects.get(
                subject_identifier_as_pk=next_options["subject_identifier"]
            ).subject_identifier
        except KeyError:
            pass
        return next_options
