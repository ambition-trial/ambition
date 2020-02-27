from ambition_visit_schedule import DAY1
from collections import OrderedDict
from django.apps import apps as django_apps
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from edc_reportable import IU_LITER, TEN_X_9_PER_LITER

from .reportables import alt_ref, neutrophil_ref, platelets_ref


class EarlyWithdrawalEvaluator:

    """A class that determines if a subject is eligible
    for early withdrawal.

    Reference ranges for each clinical value are in `reportables`.

    Used by `Eligibility`.
    """

    subject_screening_model = "ambition_screening.subjectscreening"
    blood_result_model = "ambition_subject.bloodresult"

    def __init__(
        self,
        subject_identifier=None,
        screening_identifier=None,
        subject_screening=None,
        alt=None,
        neutrophil=None,
        platelets=None,
        allow_none=None,
        request=None,
    ):
        self._day_one_blood_results = None
        self._subject_screening = subject_screening
        self.allow_none = allow_none
        self.request = request
        self.reasons_ineligible = {}
        self.screening_identifier = screening_identifier
        self.subject_identifier = subject_identifier

        self.blood_results = OrderedDict(
            alt=alt, neutrophil=neutrophil, platelets=platelets
        )
        self.update_blood_results(self.subject_screening)
        self.update_blood_results(self.day_one_blood_results)
        self.evaluate()

    def evaluate(self):
        """Evaluates the blood_results and sets the `eligible`
        flag (T/F) and updates the `reasons_ineligible` dictionary.
        """
        alt, neutrophil, platelets = [v for v in self.blood_results.values()]
        if not alt and not neutrophil and not platelets and self.allow_none:
            self.eligible = True
            if self.request:
                messages.warning(self.request, "Screening blood results are required.")
        elif not alt and not neutrophil and not platelets and not self.allow_none:
            self.eligible = False
        else:
            if alt and not alt_ref.in_bounds(value=float(alt), units=IU_LITER):
                self.reasons_ineligible.update(
                    alt=f"High ALT: {alt}. Ref: {alt_ref.description()}."
                )
            if neutrophil and not neutrophil_ref.in_bounds(
                float(neutrophil), units=TEN_X_9_PER_LITER
            ):
                self.reasons_ineligible.update(
                    neutrophil=(
                        f"Low neutrophil: {neutrophil}. Ref: "
                        f"{neutrophil_ref.description()}."
                    )
                )
            if platelets and not platelets_ref.in_bounds(
                float(platelets), units=TEN_X_9_PER_LITER
            ):
                self.reasons_ineligible.update(
                    platelets=(
                        f"Low platelets: {platelets}. "
                        f"Ref: {platelets_ref.description()}."
                    )
                )
            self.eligible = True if len(self.reasons_ineligible) == 0 else False
        return None

    @property
    def subject_screening(self):
        """Returns a subject's SubjectScreening
        model instance or None.
        """
        if not self._subject_screening:
            model_cls = django_apps.get_model(self.subject_screening_model)
            try:
                self._subject_screening = model_cls.objects.get(
                    screening_identifier=self.screening_identifier
                )
            except ObjectDoesNotExist:
                pass
        return self._subject_screening

    @property
    def day_one_blood_results(self):
        """Returns a subject's DAY1 BloodResult
        model instance or None.
        """
        if not self._day_one_blood_results:
            model_cls = django_apps.get_model(self.blood_result_model)
            try:
                self._day_one_blood_results = model_cls.objects.get(
                    subject_visit__subject_identifier=self.subject_identifier,
                    subject_visit__visit_code=DAY1,
                    subject_visit__visit_code_sequence=0,
                )
            except ObjectDoesNotExist:
                pass
        return self._day_one_blood_results

    def update_blood_results(self, obj):
        """Updates the blood results dictionary from `obj`.
        """
        if obj:
            if obj.alt:
                self.blood_results.update(alt=obj.alt)
            if obj.neutrophil:
                self.blood_results.update(neutrophil=obj.neutrophil)
            if obj.platelets:
                self.blood_results.update(platelets=obj.platelets)
        return None
