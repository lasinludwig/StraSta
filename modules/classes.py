"""classes"""


import json
from dataclasses import dataclass, field
from typing import Any

from streamlit_lottie import st_lottie


@dataclass
class LottieAnimation:
    """Lottie Animations"""

    key: str
    height: int = 200
    file: str = field(init=False)
    speed: int = field(init=False)
    run: Any = field(init=False)

    def __post_init__(self) -> None:
        """fill fields after init"""
        folder = "animations/"
        dic = {
            "login": {
                "path": f"{folder}login.json",
            },
            "running": {"speed": 0.5},
            "graph_title": {
                "path": f"{folder}title_graph.json",
                "speed": 0.5,
            },
            "meteo_title": {
                "path": f"{folder}title_meteo.json",
                "speed": 0.3,
            },
            "arrow_right": {
                "speed": 0.5,
            },
            "arrow_left": {
                "speed": 0.5,
            },
        }

        if dic.get(self.key):
            self.file = dic[self.key].get("path") or f"{folder}{self.key}.json"
            self.speed = dic[self.key].get("speed") or 1
        else:
            self.file = f"{folder}{self.key}.json"
            self.speed = 1

    def load_lottie_file(self) -> Any:
        """Load a Lottie animation by providing a json file"""
        with open(self.file) as file:
            return json.load(file)

    def show_animation(self) -> None:
        """display the animation on a streamlit page"""
        return st_lottie(
            self.load_lottie_file(),
            height=self.height,
            speed=self.speed,
            key=f"lottie_{self.key}",
        )


@dataclass
class Page:
    """Streamlit pages"""

    page_id: str
    title: str = field(init=False)
    title_animation: str = field(init=False)

    def __post_init__(self) -> None:
        """fill fields after initiation"""

        dic: dict = {
            "login": {
                "page_tit": "Strava Statistics",
                "title_animation": "running",
            },
            "activities": {
                "page_tit": "Recorded Activities",
                "title_animation": "running",
            },
            "meteo": {
                "page_tit": "Meteorologische Daten",
                "title_animation": "meteo_title",
            },
        }

        if dic.get(self.page_id):
            self.title = dic[self.page_id]["page_tit"]
            self.title_animation = dic[self.page_id]["title_animation"]
