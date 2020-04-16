from tethys_sdk.permissions import login_required
from django.shortcuts import render
from tethys_sdk.gizmos import SelectInput, RangeSlider

import json

from .utilities import get_forecast_netcdf_names
from .app import Chirps as App


@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    chirpsproducts = SelectInput(
        display_text='Select a CHIRPS product',
        name='chirpsproducts',
        multiple=False,
        original=True,
        options=(
            ('CHIRPS GEFS 5 day forecast (average)', 'gefs_05day'),
            ('CHIRPS GEFS 10 day forecast (average)', 'gefs_10day'),
            ('CHIRPS GEFS 15 day forecast (average)', 'gefs_15day'),
        ),
    )

    colorscheme = SelectInput(
        display_text='Forecast Layer Color Scheme',
        name='colorscheme',
        multiple=False,
        original=True,
        options=(
            ('Precipitation', 'precipitation'),
            ('Greyscale', 'greyscale'),
            ('Rainbow', 'rainbow'),
            ('OCCAM', 'occam'),
            ('Red-Blue', 'redblue'),
            ('ALG', 'alg'),
        )
    )

    opacity_raster = RangeSlider(
        display_text='Forecast Layer Opacity',
        name='opacity_raster',
        min=0,
        max=1,
        step=.05,
        initial=.5,
    )

    context = {
        'chirpsproducts': chirpsproducts,
        'colorscheme': colorscheme,
        'opacity_raster': opacity_raster,
        'filenames': json.dumps(get_forecast_netcdf_names()),
        'thredds_url': App.get_custom_setting('thredds_url'),
    }

    return render(request, 'chirps/home.html', context)
