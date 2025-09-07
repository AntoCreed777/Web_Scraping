from dataclasses import dataclass


@dataclass
class AppSettings:
    base_url: str = "https://www.sensacine.com/series-tv/"


settings = AppSettings()
