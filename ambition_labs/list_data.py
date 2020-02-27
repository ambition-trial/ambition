from edc_list_data import PreloadData


model_data = {
    "edc_lab.consignee": [
        {
            "name": "Botswana-Harvard Partnership",
            "contact_name": "Dr Sikhulile Moyo",
            "address": "Private Bag BO 320, Bontleng",
            "postal_code": "Plot 1836, Gaborone",
            "city": "Gaborone",
            "state": "",
            "country": "Botswana",
            "telephone": "+267 3902671",
            "mobile": "",
            "fax": "+267 3901284",
            "email": "",
        }
    ]
}

unique_field_data = {
    "edc_lab.consignee": {
        "name": (
            "Botswana-Harvard Partnership",
            "Botswana-Harvard AIDS Institute Partnership",
        )
    }
}

preload_data = PreloadData(
    list_data=None, model_data=model_data, unique_field_data=unique_field_data
)
