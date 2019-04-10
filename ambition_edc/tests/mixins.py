import os

from ambition_permissions.group_names import CLINIC_USER_GROUPS
from ambition_permissions.group_names import LAB_USER_GROUPS, TMG_USER_GROUPS
from ambition_sites.sites import ambition_sites
from ambition_subject.constants import PATIENT
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls.base import reverse
from edc_action_item.models.action_type import ActionType
from edc_appointment.constants import IN_PROGRESS_APPT, SCHEDULED_APPT, INCOMPLETE_APPT
from edc_appointment.constants import NEW_APPT
from edc_appointment.models import Appointment
from edc_constants.constants import YES
from edc_lab.constants import TUBE
from edc_selenium.mixins import (
    SeleniumLoginMixin,
    SeleniumModelFormMixin,
    SeleniumUtilsMixin,
)
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy
from selenium.webdriver.common.by import By
from edc_dashboard.url_names import url_names


class AmbitionEdcSeleniumMixin(
    SeleniumLoginMixin, SeleniumModelFormMixin, SeleniumUtilsMixin
):

    clinic_user_group_names = CLINIC_USER_GROUPS
    lab_user_group_names = LAB_USER_GROUPS
    tmg_user_group_names = TMG_USER_GROUPS

    default_sites = ambition_sites
    appointment_model = "edc_appointment.appointment"
    subject_screening_model = "ambition_screening.subjectscreening"
    subject_consent_model = "ambition_subject.subjectconsent"
    subject_visit_model = "ambition_subject.subjectvisit"
    subject_requisition_model = "ambition_subject.subjectrequisition"
    action_item_model = "edc_action_item.actionitem"
    extra_url_names = ["home_url", "administration_url"]

    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    def go_to_subject_visit_schedule_dashboard(
        self,
        visit_schedule_name=None,
        schedule_name=None,
        visit_code=None,
        save_only=None,
        screenshot=True,
    ):
        """Add screening, add subject consent, proceed
        to dashboard and update appointment to in_progress.
        """
        if not save_only:
            url_name = url_names.get("screening_listboard_url")
            url = reverse(url_name)
            self.selenium.get("%s%s" % (self.live_server_url, url))
            if screenshot:
                self.selenium.save_screenshot(
                    os.path.join(settings.BASE_DIR, "screenshots", "new_subject1.png")
                )
            element = self.wait_for("Add Subject Screening")
            element.click()

        # add a subject screening form
        subject_screening = self.fill_subject_screening(save_only=save_only)
        if screenshot:
            self.selenium.save_screenshot(
                os.path.join(settings.BASE_DIR, "screenshots", "new_subject2.png")
            )

        if not save_only:
            # add a subject consent for the newly screened subject
            element = self.wait_for(
                text=f"subjectconsent_add_{subject_screening.screening_identifier}",
                by=By.ID,
            )
            element.click()

        subject_consent = self.fill_subject_consent(
            subject_screening, save_only=save_only
        )
        if screenshot:
            self.selenium.save_screenshot(
                os.path.join(settings.BASE_DIR, "screenshots", "new_subject3.png")
            )
        subject_identifier = subject_consent.subject_identifier

        self.complete_previous_visits(
            subject_identifier=subject_identifier,
            visit_schedule_name=visit_schedule_name,
            schedule_name=schedule_name,
            visit_code=visit_code,
        )
        # set appointment in progress
        appointment = self.fill_appointment_in_progress(
            subject_identifier, save_only=save_only
        )
        if screenshot:
            self.selenium.save_screenshot(
                os.path.join(settings.BASE_DIR, "screenshots", "new_subject4.png")
            )
        return appointment

    def go_to_subject_visit_dashboard(
        self,
        visit_schedule_name=None,
        schedule_name=None,
        visit_code=None,
        save_only=None,
        screenshot=None,
        **kwargs,
    ):
        appointment = self.go_to_subject_visit_schedule_dashboard(
            visit_schedule_name=visit_schedule_name,
            schedule_name=schedule_name,
            visit_code=visit_code,
            save_only=save_only,
            **kwargs,
        )
        if save_only:
            subject_visit = self.fill_subject_visit(appointment, save_only=save_only)
        else:
            self.selenium.save_screenshot(
                os.path.join(settings.BASE_DIR, "screenshots", "new_subject5.png")
            )
            self.selenium.find_element_by_partial_link_text("Start").click()
            subject_visit = self.fill_subject_visit(appointment)
            if screenshot:
                self.selenium.save_screenshot(
                    os.path.join(settings.BASE_DIR, "screenshots", "new_subject6.png")
                )
            self.wait_for_edc()
        return subject_visit

    def fill_subject_screening(self, save_only=None):
        """Add a subject screening form.
        """
        model_obj = mommy.prepare_recipe(self.subject_screening_model)
        if save_only:
            model_obj.save()
        else:
            model_obj = self.fill_form(
                model=self.subject_screening_model,
                obj=model_obj,
                exclude=["subject_identifier", "report_datetime"],
            )
            self.wait_for_edc()
        return model_obj

    def fill_subject_consent(self, model_obj, save_only=None):
        """Add a subject consent for the newly screening subject.
        """
        model_obj = mommy.prepare_recipe(
            self.subject_consent_model,
            **{
                "screening_identifier": model_obj.screening_identifier,
                "dob": model_obj.estimated_dob,
                "gender": model_obj.gender,
            },
        )
        model_obj.initials = f"{model_obj.first_name[0]}{model_obj.last_name[0]}"
        if save_only:
            model_obj.save()
        else:
            model_obj = self.fill_form(
                model=self.subject_consent_model,
                obj=model_obj,
                exclude=[
                    "subject_identifier",
                    "citizen",
                    "legal_marriage",
                    "marriage_certificate",
                    "subject_type",
                    "gender",
                    "study_site",
                ],
                verbose=False,
            )
            self.wait_for_edc()
        return model_obj

    def fill_appointment_in_progress(self, subject_identifier, save_only=None):
        appointment = Appointment.objects.filter(
            subject_identifier=subject_identifier, appt_status=NEW_APPT
        ).order_by("timepoint")[0]
        if save_only:
            appointment.appt_status = IN_PROGRESS_APPT
            appointment.appt_reason = SCHEDULED_APPT
            appointment.save()
        else:
            self.selenium.find_element_by_id(
                f"start_btn_{appointment.visit_code}_"
                f"{appointment.visit_code_sequence}"
            ).click()
            appointment = self.fill_form(
                model=self.appointment_model,
                obj=appointment,
                values={"appt_status": IN_PROGRESS_APPT, "appt_reason": SCHEDULED_APPT},
                exclude=[
                    "subject_identifier",
                    "timepoint_datetime",
                    "timepoint_status",
                    "facility_name",
                ],
                verbose=False,
            )
            self.wait_for_edc()
        return appointment

    def fill_subject_visit(self, appointment, save_only=None):
        model_obj = mommy.prepare_recipe(
            self.subject_visit_model,
            **{"appointment": appointment, "reason": SCHEDULED, "info_source": PATIENT},
        )
        if save_only:
            model_obj.save()
        else:
            model_obj = self.fill_form(
                model=self.subject_visit_model, obj=model_obj, verbose=False
            )
            self.wait_for_edc()
        return model_obj

    def fill_subject_requisition(self, subject_visit, save_only=None):
        model_obj = mommy.prepare_recipe(
            self.subject_requisition_model,
            **{
                "subject_visit": subject_visit,
                "is_drawn": YES,
                "drawn_datetime": get_utcnow(),
                "item_type": TUBE,
                "item_count": 1,
                "estimated_volume": 0.5,
            },
        )
        if save_only:
            model_obj.save()
        else:
            model_obj = self.fill_form(
                model=self.subject_requisition_model,
                obj=model_obj,
                verbose=False,
                exclude=["report_datetime"],
            )
            self.wait_for_edc()
        return model_obj

    def fill_action_item(self, subject_identifier=None, name=None, click_add=None):
        # add action item
        if click_add:
            self.selenium.find_element_by_id("edc_action_item_actionitem_add").click()
        action_type = ActionType.objects.get(name=name)
        obj = mommy.prepare_recipe(
            self.action_item_model,
            subject_identifier=subject_identifier,
            action_type=action_type,
        )
        model_obj = self.fill_form(
            model=self.action_item_model,
            obj=obj,
            exclude=["action_identifier"],
            verbose=False,
        )
        return model_obj

    def complete_previous_visits(
        self,
        subject_identifier=None,
        visit_schedule_name=None,
        schedule_name=None,
        visit_code=None,
    ):
        """Completes previous appointments and visits up to
        but not including the given visit_code.

        Directly manipulates data instead on using selenium.
        """
        if visit_code:
            visit_codes = (
                site_visit_schedules.get_visit_schedule(visit_schedule_name)
                .schedules.get(schedule_name)
                .visits
            )
            subject_visit_model_cls = django_apps.get_model(self.subject_visit_model)
            for code in visit_codes:
                if visit_code == code:
                    break
                else:
                    appointment = Appointment.objects.get(
                        subject_identifier=subject_identifier, visit_code=code
                    )
                    appointment = self.fill_appointment_in_progress(
                        subject_identifier, save_only=True
                    )
                    try:
                        subject_visit_model_cls.objects.get(appointment=appointment)
                    except ObjectDoesNotExist:
                        self.fill_subject_visit(appointment, save_only=True)
                        appointment.appt_status = INCOMPLETE_APPT
                        appointment.save()
