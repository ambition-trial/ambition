from dateutil.relativedelta import relativedelta
from django.utils.timezone import localtime
from edc_utils import get_utcnow
from edc_constants.constants import FEMALE, MALE
from edc_reportable import AgeEvaluator, NormalReference, ValueBoundryError
from edc_reportable import IU_LITER, TEN_X_9_PER_LITER


class MyAgeEvaluator(AgeEvaluator):
    def __init__(self, **kwargs):
        self.reasons_ineligible = None
        super().__init__(**kwargs)

    def eligible(self, age=None):
        self.reasons_ineligible = None
        eligible = False
        if age:
            try:
                self.in_bounds_or_raise(age=age)
            except ValueBoundryError:
                self.reasons_ineligible = "age<18."
            else:
                eligible = True
        return eligible

    def in_bounds_or_raise(self, age=None):
        self.reasons_ineligible = None
        dob = localtime(get_utcnow() - relativedelta(years=age)).date()
        age_units = "years"
        report_datetime = localtime(get_utcnow())
        return super().in_bounds_or_raise(
            dob=dob, report_datetime=report_datetime, age_units=age_units
        )


age_evaluator = MyAgeEvaluator(age_lower=18, age_lower_inclusive=True)

alt_ref = NormalReference(
    name="alt",
    upper=200,
    upper_inclusive=True,
    units=IU_LITER,
    gender=[MALE, FEMALE],
    age_lower=18,
    age_lower_inclusive=True,
)


neutrophil_ref = NormalReference(
    name="neutrophil",
    lower=0.5,
    lower_inclusive=True,
    units=TEN_X_9_PER_LITER,
    gender=[MALE, FEMALE],
    age_lower=18,
    age_lower_inclusive=True,
)


platelets_ref = NormalReference(
    name="platelets",
    lower=50,
    lower_inclusive=True,
    units=TEN_X_9_PER_LITER,
    gender=[MALE, FEMALE],
    age_lower=18,
    age_lower_inclusive=True,
)
