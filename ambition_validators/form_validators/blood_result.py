from ambition_labs.panels import cd4_panel, viral_load_panel, fbc_panel
from ambition_labs.panels import chemistry_panel, chemistry_alt_panel
from ambition_subject.constants import ALREADY_REPORTED
from ambition_visit_schedule.constants import DAY1
from django.apps import apps as django_apps
from django.forms import forms
from edc_constants.constants import NO, YES, NOT_APPLICABLE
from edc_form_validators import FormValidator
from edc_lab import CrfRequisitionFormValidatorMixin
from edc_reportable import site_reportables, NotEvaluated, GRADE3, GRADE4


class BloodResultFormValidator(CrfRequisitionFormValidatorMixin, FormValidator):

    def clean(self):
        Site = django_apps.get_model('sites.site')
        self.required_if_true(
            any([self.cleaned_data.get(f) is not None
                 for f in [f for f in self.instance.ft_fields]]),
            field_required='ft_requisition')
        self.validate_requisition(
            'ft_requisition', 'ft_assay_datetime', chemistry_panel, chemistry_alt_panel)

        self.required_if_true(
            any([self.cleaned_data.get(f) is not None
                 for f in [f for f in self.instance.cbc_fields]]),
            field_required='cbc_requisition')
        self.validate_requisition(
            'cbc_requisition', 'cbc_assay_datetime', fbc_panel)

        self.required_if_true(
            self.cleaned_data.get('cd4') is not None,
            field_required='cd4_requisition')
        self.validate_requisition(
            'cd4_requisition', 'cd4_assay_datetime', cd4_panel)

        self.required_if_true(
            self.cleaned_data.get('vl') is not None,
            field_required='vl_requisition')
        self.validate_requisition(
            'vl_requisition', 'vl_assay_datetime', viral_load_panel)

        subject_identifier = self.cleaned_data.get(
            'subject_visit').subject_identifier
        RegisteredSubject = django_apps.get_model(
            'edc_registration.registeredsubject')
        subject_visit = self.cleaned_data.get('subject_visit')
        registered_subject = RegisteredSubject.objects.get(
            subject_identifier=subject_identifier)
        gender = registered_subject.gender
        dob = registered_subject.dob

        # check normal ranges and grade result values
        opts = dict(
            gender=gender, dob=dob, report_datetime=subject_visit.report_datetime)
        for field, value in self.cleaned_data.items():
            grp = site_reportables.get('ambition').get(field)
            if value and grp:
                self.evaluate_result(field, value, grp, **opts)

        # results_abnormal
        self.validate_final_assessment(
            field='results_abnormal', responses=[YES], suffix='_abnormal', word='abnormal')
        self.applicable_if(
            YES, field='results_abnormal',
            field_applicable='results_reportable')
        self.validate_final_assessment(
            field='results_reportable', responses=[GRADE3, GRADE4],
            suffix='_reportable', word='reportable')

        if self.cleaned_data.get('subject_visit').visit_code == DAY1:
            if (Site.objects.get_current().name not in ['gaborone', 'blantyre']
                    and self.cleaned_data.get('bios_crag') != NOT_APPLICABLE):
                raise forms.ValidationError(
                    {f'bios_crag': 'This field is not applicable'})
            self.applicable_if(
                YES,
                field='bios_crag',
                field_applicable='crag_control_result')

            self.applicable_if(
                YES,
                field='bios_crag',
                field_applicable='crag_t1_result')

            self.applicable_if(
                YES,
                field='bios_crag',
                field_applicable='crag_t2_result')

    def evaluate_result(self, field, value, grp, **opts):
        """Evaluate a single result value.

        Grading is done first. If the value is not gradeable,
        the value is checked against the normal limits.

        Expected field naming convention:
            * {field}
            * {field}_units
            * {field}_abnormal [YES, (NO)]
            * {field}_reportable [(NOT_APPLICABLE), NO, GRADE3, GRADE4]
        """
        abnormal = self.cleaned_data.get(f'{field}_abnormal')
        reportable = self.cleaned_data.get(f'{field}_reportable')
        units = self.cleaned_data.get(f'{field}_units')
        opts.update(units=units)
        if not units:
            raise forms.ValidationError(
                {f'{field}_units': f'Units required.'})
        try:
            grade = grp.get_grade(value, **opts)
        except NotEvaluated as e:
            raise forms.ValidationError({field: str(e)})

        if grade and grade.grade and reportable != str(grade.grade):
            if reportable != ALREADY_REPORTED:
                raise forms.ValidationError({
                    field: f'{field.upper()} is reportable. Got {grade.description}.'})
        elif not grade and reportable not in [NO, NOT_APPLICABLE]:
            raise forms.ValidationError({
                f'{field}_reportable': 'Invalid. Expected \'No\' or \'Not applicable\'.'})
        else:
            try:
                normal = grp.get_normal(value, **opts)
            except NotEvaluated as e:
                raise forms.ValidationError({field: str(e)})
            if not normal and abnormal == NO:
                descriptions = grp.get_normal_description(**opts)
                raise forms.ValidationError({
                    field:
                    f'{field.upper()} is abnormal. Normal ranges: {", ".join(descriptions)}'})
            elif normal and not grade and abnormal == YES:
                raise forms.ValidationError({
                    f'{field}_abnormal': 'Invalid. Result is not abnormal'})

        if abnormal == YES and reportable == NOT_APPLICABLE:
            raise forms.ValidationError(
                {f'{field}_reportable': 'This field is applicable if result is abnormal'})
        elif abnormal == NO and reportable != NOT_APPLICABLE:
            raise forms.ValidationError(
                {f'{field}_reportable': 'This field is not applicable'})

    def validate_final_assessment(self, field=None, responses=None, suffix=None, word=None):
        """Common code to validate fields `results_abnormal`
        and `results_reportable`.
        """
        answers = list({k: v for k, v in self.cleaned_data.items()
                        if k.endswith(suffix)}.values())
        if len([True for v in answers if v is not None]) == 0:
            raise forms.ValidationError(
                {'results_abnormal': f'No results have been entered.'})
        answers_as_bool = [True for v in answers if v in responses]
        if self.cleaned_data.get(field) == NO:
            if any(answers_as_bool):
                are = 'is' if len(answers_as_bool) == 1 else 'are'
                raise forms.ValidationError(
                    {field: f'{len(answers_as_bool)} of the above results {are} {word}'})
        elif self.cleaned_data.get(field) == YES:
            if not any(answers_as_bool):
                raise forms.ValidationError(
                    {field: f'None of the above results are {word}'})
