from ambition_subject.models.patient_history import PatientHistory
from ambition_subject.models.week2.week2 import Week2
from django.core.exceptions import ObjectDoesNotExist
from edc_adverse_event.pdf_reports import AeReport as BaseAeReport
from reportlab.lib.units import cm
from reportlab.platypus.tables import Table


class AeReport(BaseAeReport):

    logo_data = {
        "app_label": "ambition_edc",
        "filename": "ambition_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }

    def get_weight_model_and_field(self):
        try:
            obj = Week2.objects.get(
                subject_visit__appointment__subject_identifier=self.subject_identifier
            )
        except ObjectDoesNotExist:
            try:
                obj = PatientHistory.objects.get(
                    subject_visit__appointment__subject_identifier=self.subject_identifier
                )
            except ObjectDoesNotExist:
                return {"model": None, "field": "weight"}
        return {"model": obj._meta.label_lower, "field": "weight"}

    def _draw_ae_drug_relationship(self, story):
        # relationship
        rows = [
            [
                "Is the incident related to the patient involvement in the study?",
                self.ae_initial.get_ae_study_relation_possibility_display(),
            ],
            [
                "Relationship to Fluconozole:",
                self.ae_initial.get_fluconazole_relation_display(),
            ],
            [
                "Relationship to Flucytosine:",
                self.ae_initial.get_flucytosine_relation_display(),
            ],
            [
                "Relationship to Amphotericin formulation:",
                self.ae_initial.get_amphotericin_relation_display(),
            ],
        ]
        t = Table(rows, (14 * cm, 4 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        story.append(t)
