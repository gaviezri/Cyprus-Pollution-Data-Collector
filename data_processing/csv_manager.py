import datetime
import os
from io import StringIO
import pandas as pd
import json
from constants.config import REPORT_PATH, CONFIG_PATH
from pathlib import Path
from os import getcwd


class CSVManager:

    @staticmethod
    def update_entry(station_2_code_notation_2_monthly_average, month_dt:datetime.datetime):
        with open(CONFIG_PATH) as config:
            config_dict = json.load(config)
            if config_dict[REPORT_PATH] != "":
                report_path = Path(config_dict[REPORT_PATH])
            else:
                report_path = Path(getcwd()) / "reports"
                if not os.path.exists(report_path):
                    os.mkdir(report_path)
            report_path = report_path / f"{month_dt.strftime("%Y%m")}.xlsx"
        df = pd.read_json(StringIO(json.dumps(station_2_code_notation_2_monthly_average)))
        df.to_excel(report_path)
        return report_path
