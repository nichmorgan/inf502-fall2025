# this is just the start for you.  You will need at least the following libraries, so let's do the import
import os
from datetime import timedelta
from pathlib import Path
from typing import Literal

import pandas as pd
from tqdm import tqdm

Measure = Literal["METs", "Steps", "Calories", "Intensities"]


# we can start by defining the loadFitbit function.
def loadFitbit(
    path_str: str = "./data/fitbit",
    measures: list[Measure] = ["METs", "Steps", "Calories", "Intensities"],
) -> pd.DataFrame:
    # by using measures=[] above, we are setting some default values.  If you provide a second input, those will overwrite the default here.
    path: Path = Path(path_str)

    if not path.exists():
        raise FileNotFoundError(f"Non existing path: {path.as_posix()}")
    if path.is_file() and not path.name.lower().endswith(".csv"):
        raise ValueError("File must be an CSV.")

    path_list = path.glob("**/*.csv") if path.is_dir() else [path]
    path_list = filter(
        lambda p: any(measure.lower() in p.name.lower() for measure in measures),
        path_list,
    )
    path_list = tqdm(list(path_list), unit=" file", desc="Loading fitbit")
    df = pd.concat(map(loadFitbitFile, path_list), ignore_index=True).sort_values(
        ["Subject", "DateTime"]
    )
    return df


def loadFitbitFile(path: Path) -> pd.DataFrame:
    date_format = "%m/%d/%Y %I:%M:%S %p"
    clinical = path.name.split("_", 1)[0]

    metric_name: str | None = None
    for subject in Measure.__args__:
        if subject.lower() in path.name.lower():
            metric_name = subject
            break
    if not metric_name:
        raise ValueError(f"Filename with unknown subject: {path.name}")

    df = pd.read_csv(path)
    metric_columns = list(df.keys())[1:][:-2]

    df["ActivityHour"] = pd.to_datetime(df["ActivityHour"], format=date_format)
    df = df.melt(
        ["ActivityHour"],
        metric_columns,
        value_name="value",
    ).rename(columns={"variable": "sensor", "ActivityHour": "DateTime"})

    df["Clinical"] = clinical
    df["Filename"] = path.name
    df["Subject"] = metric_name

    return df


def loadActigraph(path):
    try:
        os.scandir(path)
    except NotADirectoryError:
        # it wasn't a directory that was passed in
        print("Filename provided")
    # you can fill in the rest, I know you can.
    # do watch out for the funkyness of the actigraph files though.
    # how can you skip some number of lines when reading in a csv to a DataFrame?
    # dang it, those columns aren't labeled!  So ... how can you specify column names on that load as well?


def loadActigraphFile(this_file):
    date_format = "%m/%d/%Y %H:%M:%S"  # the time format is a bit different in the actigraph.  Use this one.
    delta = timedelta(minutes=1)
    # maybe you need to read N lines of the file, and look for clues as to the start date and start time?
