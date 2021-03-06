from django import forms
from django.core.validators import FileExtensionValidator

from . import models
from .constants import ChartTypes, UploadFileTypes


class UploadForm(forms.Form):
    """ A form for uploading the data CSV files """
    FILE_TYPES = [
        (UploadFileTypes.BUILDING_DATA, 'Building Data'),
        (UploadFileTypes.HALF_HOURLY_DATA, 'Half Hourly Data'),
        (UploadFileTypes.METER_DATA, 'Meter Data')
    ]
    upload_file = forms.FileField(
        error_messages={'required': 'Please select a file'},
        label='File',
        required=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['csv']
        )]
    )
    file_type = forms.IntegerField(
        label='Type',
        required=True,
        widget=forms.Select(choices=FILE_TYPES)
    )


class VisualiseForm(forms.Form):
    """
    A form used on the visualisation page.
    The choices for meter_id are populated dynamically on init.
    """
    CHART_TYPES = {
        (ChartTypes.METER_TIME, 'Meter Consumption over time'),
        (ChartTypes.METER_TIME_DAY_AGG, 'Meter Consumption aggregated per day'),
        (ChartTypes.METER_INSTALLATION, 'Meter Installation by Fuel Type')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meter_id'] = forms.IntegerField(
            widget=forms.Select(choices=self.get_meter_id_choices()),
            error_messages={'required': 'Please enter a meter id'},
            label='Meter Id',
            required=True
        )

    def get_meter_id_choices(self):
        return [
            (m.id, str(m.id)) for m in models.Meter.objects.all()
        ]

    chart_type = forms.IntegerField(
        label='Chart Type',
        required=True,
        widget=forms.Select(choices=CHART_TYPES)
    )
