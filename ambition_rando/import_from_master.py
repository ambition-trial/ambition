import csv
import os

from .utils import get_site_name


def import_from_master(path=None, source_prefix=None, destination_filename=None):
    """
    Import the rando list from the original files from the LSTM Statistician

    For example:

        import_from_master(
            path='/Users/erikvw/Documents/ambition/rando',
            source_prefix='randlistsite',
            destination_filename='rando_combined.csv')
    """
    source_files = [f for f in os.listdir(path) if f.startswith(source_prefix)]
    source_files.sort()

    for index, source_filename in enumerate(source_files):
        with open(os.path.join(path, source_filename), "r") as source, open(
            os.path.join(path, destination_filename), "a+"
        ) as destination:
            reader = csv.DictReader(source)
            fieldnames = [
                "sid",
                "assignment",
                "site_name",
                "orig_site",
                "orig_allocation",
                "orig_desc",
            ]
            writer = csv.DictWriter(destination, fieldnames=fieldnames)
            if index == 0:
                writer.writeheader()
            for row in reader:
                rowdict = dict(
                    sid=row.get("random_number"),
                    assignment=row.get("allocation"),
                    site_name=get_site_name(row.get("site")),
                    orig_site=get_site_name(row.get("site"), row=row),
                    orig_allocation=row.get("allocation"),
                    orig_desc=row.get("description"),
                )
                writer.writerow(rowdict)
