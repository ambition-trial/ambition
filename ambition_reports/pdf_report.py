from ambition_rando.models import RandomizationList
from ambition_subject.models.patient_history import PatientHistory
from edc_auth.group_names import RANDO
from edc_registration.models import RegisteredSubject
from edc_reports.crf_pdf_report import CrfPdfReport
from edc_utils import formatted_age
from reportlab.lib.units import cm
from reportlab.platypus import Table
from textwrap import fill


def get_weight_for_timepoint(subject_identifier=None, reference_dt=None):
    qs = PatientHistory.objects.filter(
        subject_visit__appointment__subject_identifier=subject_identifier,
        report_datetime__lte=reference_dt,
    ).order_by("-report_datetime")
    if qs:
        return qs[0].weight
    return None


class AmbitionCrfPdfReport(CrfPdfReport):

    logo_data = {
        "app_label": "ambition_edc",
        "filename": "ambition_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }

    def __init__(self, subject_identifier=None, **kwargs):
        super().__init__(**kwargs)
        self.subject_identifier = subject_identifier
        self.registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.subject_identifier
        )
        self.assignment = RandomizationList.objects.get(
            subject_identifier=self.subject_identifier
        ).get_assignment_display()

    @property
    def age(self):
        model_obj = getattr(self, self.model_attr)
        return formatted_age(
            self.registered_subject.dob, reference_dt=model_obj.report_datetime
        )

    def draw_demographics(self, story, **kwargs):

        model_obj = getattr(self, self.model_attr)
        weight = get_weight_for_timepoint(
            subject_identifier=self.subject_identifier,
            reference_dt=model_obj.report_datetime,
        )
        assignment = "*****************"
        if self.request.user.groups.filter(name=RANDO).exists():
            assignment = fill(self.assignment, width=80)
        rows = [
            ["Subject:", self.subject_identifier],
            [
                "Gender/Age:",
                f"{self.registered_subject.get_gender_display()} {self.age}",
            ],
            ["Weight:", f"{weight} kg"],
            [
                "Study site:",
                f"{self.registered_subject.site.id}: "
                f"{self.registered_subject.site.name.title()}",
            ],
            [
                "Randomization date:",
                self.registered_subject.randomization_datetime.strftime(
                    "%Y-%m-%d %H:%M"
                ),
            ],
            ["Assignment:", assignment],
        ]

        t = Table(rows, (4 * cm, 14 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        t.hAlign = "LEFT"
        story.append(t)
