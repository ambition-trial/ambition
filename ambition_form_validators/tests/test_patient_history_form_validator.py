from ambition_visit_schedule.constants import DAY1
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE, FEMALE
from edc_utils import get_utcnow

from ..constants import HEADACHE, VISUAL_LOSS
from ..form_validators import PatientHistoryFormValidator
from .models import ListModel, Appointment, SubjectVisit
from edc_registration.utils import get_registered_subject_model
from dateutil.relativedelta import relativedelta


class TestPatientHistoryFormValidator(TestCase):
    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier="11111111", appt_datetime=get_utcnow(), visit_code=DAY1
        )
        self.subject_visit = SubjectVisit.objects.create(appointment=appointment)

        self.registered_subject = get_registered_subject_model().objects.create(
            subject_identifier="11111111",
            dob=get_utcnow() - relativedelta(years=25),
            gender=FEMALE,
        )

    def test_headache_requires_headache_duration(self):
        """Assert that headache selection requires duration
        """
        ListModel.objects.create(name=HEADACHE, display_name=HEADACHE)

        cleaned_data = {"symptom": ListModel.objects.all(), "headache_duration": None}
        form_validator = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("headache_duration", form_validator._errors)

    def test_visual_loss_requires_duration(self):
        """Assert that visual_loss selection requires duration
        """
        ListModel.objects.create(name=VISUAL_LOSS, display_name=VISUAL_LOSS)

        cleaned_data = {
            "symptom": ListModel.objects.all(),
            "visual_loss_duration": None,
        }
        form_validator = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("visual_loss_duration", form_validator._errors)

    def test_tb_history_yes_tb_site_none_invalid(self):
        cleaned_data = {"tb_history": YES, "tb_site": NOT_APPLICABLE}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("tb_site", form._errors)

    def test_tb_treatment_taking_rifapicin_none_invalid(self):
        cleaned_data = {"tb_treatment": YES, "taking_rifampicin": NOT_APPLICABLE}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("taking_rifampicin", form._errors)

    def test_taking_rifapicin_started_date_none_invalid(self):
        cleaned_data = {"taking_rifampicin": YES, "rifampicin_started_date": None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("rifampicin_started_date", form._errors)

    def test_not_new_hiv_diagnosis_taking_arv_none_invalid(self):
        cleaned_data = {"new_hiv_diagnosis": NO, "taking_arv": NOT_APPLICABLE}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("taking_arv", form._errors)

    def test_taking_arv_initial_arv_date_none_invalid(self):
        cleaned_data = {"taking_arv": YES, "initial_arv_date": None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("initial_arv_date", form._errors)

    def test_initial_arv_date_estimated_invalid(self):
        cleaned_data = {"initial_arv_date": None, "initial_arv_date_estimated": YES}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("initial_arv_date_estimated", form._errors)

    def test_arv_date_estimated_valid(self):
        cleaned_data = {
            "initial_arv_date": None,
            "initial_arv_date_estimated": NOT_APPLICABLE,
        }
        form_validator = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_taking_arv_first_arv_regimen_none_invalid(self):
        ListModel.objects.create(name=NOT_APPLICABLE, display_name=NOT_APPLICABLE)
        cleaned_data = {
            "report_datetime": get_utcnow(),
            "subject_visit": self.subject_visit,
            "taking_arv": YES,
            "initial_arv_date": get_utcnow(),
            "initial_arv_regimen": ListModel.objects.all(),
        }
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("initial_arv_regimen", form._errors)

    def test_taking_arv_initial_arv_regimen_no(self):
        ListModel.objects.create(name=OTHER, display_name=OTHER)
        cleaned_data = {
            "taking_arv": NO,
            "initial_arv_regimen": ListModel.objects.all(),
        }
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("initial_arv_regimen", form._errors)

    def test_initial_arv_regimen_other_none_invalid(self):
        ListModel.objects.create(name=OTHER, display_name=OTHER)

        cleaned_data = {
            "initial_arv_regimen": ListModel.objects.all(),
            "initial_arv_regimen_other": None,
        }
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("initial_arv_regimen_other", form._errors)

    #     @tag("1")
    #     def test_taking_arv_patient_adherence_no(self):
    #         ListModel.objects.create(
    #             name=NOT_APPLICABLE, display_name=NOT_APPLICABLE)
    #         cleaned_data = {
    #             "taking_arv": NO,
    #             "initial_arv_regimen": ListModel.objects.all(),
    #             "current_arv_is_adherent": YES,
    #         }
    #         form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
    #         self.assertRaises(ValidationError, form.validate)
    #         self.assertIn("current_arv_is_adherent", form._errors)

    def test_current_arv_regimen_other_none_invalid(self):
        ListModel.objects.create(name=OTHER, display_name=OTHER)

        cleaned_data = {
            "current_arv_regimen": ListModel.objects.all(),
            "current_arv_regimen_other": None,
        }
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("current_arv_regimen_other", form._errors)

    #     def test_taking_arv_patient_adherence_none_invalid(self):
    #         cleaned_data = {"taking_arv": NO, "current_arv_is_adherent": None}
    #         form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
    #         self.assertRaises(ValidationError, form.validate)
    #         self.assertIn("current_arv_is_adherent", form._errors)

    def test_no_last_viral_load_date_invalid(self):
        cleaned_data = {"last_viral_load": None, "viral_load_date": get_utcnow()}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("viral_load_date", form._errors)

    def test_no_viral_load_date_estimated_invalid(self):
        cleaned_data = {"viral_load_date": None, "vl_date_estimated": "blah"}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("vl_date_estimated", form._errors)

    def test_no_last_cd4_date_invalid(self):
        cleaned_data = {"last_cd4": None, "cd4_date": get_utcnow()}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("cd4_date", form._errors)

    def test_no_cd4_date_estimated_invalid(self):
        cleaned_data = {"cd4_date": None, "cd4_date_estimated": "blah"}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("cd4_date_estimated", form._errors)

    def test_neurological_focal_neurologic_deficit_none_invalid(self):
        ListModel.objects.create(
            name="focal_neurologic_deficit", display_name="focal_neurologic_deficit"
        )

        cleaned_data = {
            "neurological": ListModel.objects.all(),
            "focal_neurologic_deficit": None,
        }
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("focal_neurologic_deficit", form._errors)

    def test_neurological_neurological_other_none_invalid(self):
        ListModel.objects.create(name=OTHER, display_name=OTHER)

        cleaned_data = {
            "neurological": ListModel.objects.all(),
            "neurological_other": None,
        }
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("neurological_other", form._errors)

    def test_specify_medications_NO_other_none_invalid(self):
        ListModel.objects.create(name=OTHER, display_name=OTHER)

        cleaned_data = {
            "specify_medications": ListModel.objects.all(),
            "specify_medications_other": None,
        }
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("specify_medications_other", form._errors)
