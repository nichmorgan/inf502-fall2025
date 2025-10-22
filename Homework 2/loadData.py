# this is just the start for you.  You will need at least the following libraries, so let's do the import
import os
from datetime import timedelta
from pathlib import Path
from typing import Iterable, Literal
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
from itertools import islice

Measure = Literal["METs", "Steps", "Calories", "Intensities"]


def get_metric_from_path(path: Path) -> Measure | None:
    for measure in Measure.__args__:
        if str(measure).lower() in path.as_posix().lower():
            return measure
    return None


def group_df_by_fitbit_metric(path_list: Iterable[Path]) -> dict[Measure, pd.DataFrame]:
    df_by_metric = defaultdict(pd.DataFrame)
    for path in path_list:
        metric_name = get_metric_from_path(path)
        if not metric_name:
            raise ValueError(f"Metric name not found for: {path.as_posix()}")
        df_by_metric[metric_name] = pd.concat(
            [df_by_metric[metric_name], loadFitbitFile(path, metric_name)],
            ignore_index=True,
        )
    return df_by_metric


def get_files(path_str: str, glob_pattern: str = "**/*.csv") -> list[Path]:
    path = Path(path_str)

    if not path.exists():
        raise FileNotFoundError(f"Non existing path: {path.as_posix()}")
    if path.is_file() and not path.name.lower().endswith(".csv"):
        raise ValueError("File must be an CSV.")

    path_list = path.glob(glob_pattern) if path.is_dir() else [path]
    return list(path_list)


# we can start by defining the loadFitbit function.
def loadFitbit(
    path: str = "./data/fitbit",
    measures: list[Measure] = ["METs", "Steps", "Calories", "Intensities"],
) -> pd.DataFrame:
    # by using measures=[] above, we are setting some default values.  If you provide a second input, those will overwrite the default here.
    path_list = filter(
        lambda p: any(measure.lower() in p.name.lower() for measure in measures),
        get_files(path),
    )

    path_list = tqdm(list(path_list), unit=" file", desc="Loading fitbit")
    df_by_metric = group_df_by_fitbit_metric(path_list)

    df = df_by_metric.popitem()[1]
    merge_keys = ["Subject", "DateTime"]
    for metric_df in tqdm(
        df_by_metric.values(),
        desc="Merging metrics",
        unit=" Metric",
    ):
        df = pd.merge(
            df,
            metric_df,
            how="left",
            on=merge_keys,
        )

    df.sort_values(merge_keys, inplace=True)

    return df


def loadFitbitFile(path: Path, metric_name: Measure) -> pd.DataFrame:
    date_format = "%m/%d/%Y %I:%M:%S %p"
    subject = path.name.split("_", 1)[0]

    df = pd.read_csv(path)
    metric_columns = list(df.keys())[1:][:-2]

    df["ActivityHour"] = pd.to_datetime(df["ActivityHour"], format=date_format)
    df = df.melt(
        ["ActivityHour"],
        metric_columns,
        value_name=metric_name,
    ).rename(columns={"variable": "minute", "ActivityHour": "DateTime"})

    df["minute"] = pd.to_numeric(df["minute"].str.slice(-2), downcast="unsigned")
    df["minute"] = pd.to_timedelta(df["minute"], "minute")
    df["DateTime"] += df.pop("minute")

    df["Subject"] = subject

    return df


def loadActigraph(path: str = "./data/actigraph"):
    path_list = tqdm(get_files(path), desc="Loading actigraph", unit=" file")
    df = pd.concat(map(loadActigraphFile, path_list), ignore_index=True)
    df.sort_values(["Subject", "DateTime"], inplace=True)
    return df

    # you can fill in the rest, I know you can.
    # do watch out for the funkyness of the actigraph files though.
    # how can you skip some number of lines when reading in a csv to a DataFrame?
    # dang it, those columns aren't labeled!  So ... how can you specify column names on that load as well?


def loadActigraphFile(path: Path) -> pd.DataFrame:
    date_format = "%m/%d/%Y %H:%M:%S"  # the time format is a bit different in the actigraph.  Use this one.
    subject = path.name.split("_", 1)[0]

    with path.open() as f:
        header_txts = list(islice(f, 5))

    start_time_str = header_txts[2].strip().split()[-1]
    start_date_str = header_txts[3].strip().split()[-1]
    timedelta_str = header_txts[4].strip().split()[-1]

    start_datetime = pd.to_datetime(
        f"{start_date_str} {start_time_str}",
        format=date_format,
    )
    timedelta = pd.to_timedelta(timedelta_str)

    df = pd.read_csv(path, skiprows=10, header=None, usecols=[3], names=["Steps"])
    df["DateTime"] = start_datetime + (timedelta * df.index)
    df["Subject"] = subject

    return df
