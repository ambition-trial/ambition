import pandas as pd

from edc_pdutils import ColumnApply, ColumnMap


class ToTimestamp(ColumnApply):

    """Converts a datetime columns to string timestamp.
    """

    column_names = ["drawn_datetime"]
    format = "%Y-%m-%d %H:%M"

    def apply(self, value):
        return value if pd.isnull(value) else value.strftime(self.format)


class ToRandoArm(ColumnMap):
    column_names = ["rx"]
    mappings = dict(
        rx={
            "enc1:::c623fb3d561354d55cf9312c0cf840ebf199adc740115bbca80d7b8963500942": "A",
            "enc1:::f474f2b3e162ea58b01c89076309deb20d4a6c2779e93651c1fb110bef6e3468": "B",
        }
    )


class ColumnHandler:

    handlers = [ToTimestamp, ToRandoArm]

    def __init__(self, dataframe=None):
        self.dataframe = dataframe
        for handler_cls in self.handlers:
            handler = handler_cls(self.dataframe)
            self.dataframe = handler.dataframe
