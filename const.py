from dataclasses import dataclass


@dataclass
class AppSettings:
    base_url: str = "https://www.sensacine.com/"

    @property
    def series_tv_link(self):
        return self.base_url + "series-tv/"


settings = AppSettings()
