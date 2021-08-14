import pandas as pd
from comtrade import Comtrade
import io

OUTPUT_COLUMNS = ["Time", "Name", "Channel", "Value"]

"""
Function that reads an uploaded comtrande file (.cfg and .dat)
and returns a comtrade reader
"""


def read_comtrade(files: list):
    comtrade_reader = Comtrade()
    cfg_file = [file for file in files if ".CFG" in file.name or ".cfg" in file.name][0]
    dat_file = [file for file in files if ".DAT" in file.name or ".dat" in file.name][0]
    # reading uploaded files and decoding them
    cfg_content = cfg_file.read().decode("UTF-8")
    dat_content = dat_file.read().decode("UTF-8")

    # saving files locally
    with open(cfg_file.name, "w", encoding="UTF-8") as f:
        for line in cfg_content.split("\n"):
            f.write(line)
        f.close()
    with open(dat_file.name, "w", encoding="UTF-8") as f:
        for line in dat_content.split("\n"):
            f.write(line)
        f.close()
    # loading comtrande files
    comtrade_reader.load(cfg_file.name, dat_file.name)
    return comtrade_reader


"""
create a dataframe with the channels of interest from the
comtrade reader.
"""


def clean_entry(comtrade_reader, first_channel, inrush_name):
    cleaned_values = []
    for channel in range(first_channel, first_channel + 3):
        current_channel = comtrade_reader.analog[channel - 1]
        n = len(current_channel)
        times = comtrade_reader.time
        cleaned_values.extend(
            [
                *zip(
                    times,
                    [inrush_name] * n,
                    [channel] * n,
                    current_channel,
                )
            ]
        )
    return pd.DataFrame(cleaned_values, columns=OUTPUT_COLUMNS)
