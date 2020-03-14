from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class Chirps(TethysAppBase):
    """
    Tethys app class for CHIRPS Precipitation Tool.
    """

    name = 'CHIRPS Precipitation Tool'
    index = 'chirps:home'
    icon = 'chirps/images/rain.png'
    package = 'chirps'
    root_url = 'chirps'
    color = '#1cae3x'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        return (
            UrlMap(
                name='home',
                url='chirps',
                controller='chirps.controllers.home'
            ),
        )

    def custom_settings(self):
        return (
            CustomSetting(
                name='thredds_path',
                type=CustomSetting.TYPE_STRING,
                description='Path to the DATA shared by TDS',
                required=True,
                default="/Users/rileyhales/thredds/chirpsapp/"
            ),
            CustomSetting(
                name='thredds_url',
                type=CustomSetting.TYPE_STRING,
                description='Url to the chirpsapp directory on the TDS',
                required=True,
                default="http://127.0.0.1:7000/thredds/wms/data/chirpsapp/",
            ),
        )
