"""general functions"""

import base64
import datetime
import os
import time
from typing import Any

import streamlit as st
from github import Github
from pytz import timezone


# timer decorator
def timer() -> None:
    """function-timer for debugging"""

    def decorator(func: Any) -> Any:
        def wrapper(*args, **kwargs) -> None:
            start_time = time.perf_counter()
            if "dic_exe_time" not in st.session_state:
                st.session_state["dic_exe_time"] = {}
            result = func(*args, **kwargs)
            st.session_state["dic_exe_time"][func.__name__] = (
                time.perf_counter() - start_time
            )
            return result

        return wrapper

    return decorator


def del_session_state_entry(key: str) -> None:
    """Eintrag in st.session_state löschen"""
    if key in st.session_state:
        del st.session_state[key]


def get_com_date() -> None:
    """commit message and date from GitHub"""

    utc = timezone("UTC")
    eur = timezone("Europe/Berlin")
    date_now = datetime.datetime.now()
    tz_diff = (
        utc.localize(date_now) - eur.localize(date_now).astimezone(utc)
    ).seconds / 3600

    # pat= personal access token - in github
    # click on your profile and go into
    # settings -> developer settings -> personal access tokens
    pat = os.getenv("GITHUB_PAT")
    gith = Github(pat)
    repo = gith.get_user().get_repo("StraSta")
    branch = repo.get_branch("master")
    sha = branch.commit.sha
    commit = repo.get_commit(sha).commit
    st.session_state["com_date"] = commit.author.date + datetime.timedelta(
        hours=tz_diff
    )
    st.session_state["com_msg"] = commit.message.split("\n")[-1]


# svg in streamlit app darstellen (z.B. UTEC-Logo)
def render_svg(svg_path: str = "logo/UTEC_logo_text.svg") -> str:
    """Renders the given svg string."""
    # lines = open(svg_path).readlines()
    with open(svg_path) as lines:
        svg = "".join(lines.readlines())
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}"/>'


def nachkomma(value: float) -> str:
    """Nachkommastellen je nach Ziffern in Zahl"""
    if abs(value) >= 1000:
        return str(f"{value:,.0f}").replace(",", ".")
    if abs(value) >= 100:
        return str(f"{value:,.0f}").replace(".", ",")
    if abs(value) >= 10:
        return str(f"{value:,.1f}").replace(".", ",")

    return str(f"{value:,.2f}").replace(".", ",")
