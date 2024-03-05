import logging, traceback, time
import os
import shutil
from sys import argv
from api.data_fetcher import DataFetcher as Fetcher
from api.timestamp_maker import TimestampMaker as TSM
from data_processing.csv_manager import CSVManager
from data_processing.data_processor import DataProcessor
from main.cmdline_args_manager import ArgsManager
from report.email_reporter import EmailReporter
from report.sharepoint_reporter import SharePointReporter


class Driver:
    @staticmethod
    def run():
        try:
            if len(argv) > 1:
                ArgsManager.handle_args()
            else:
                Driver.routine_data_collection()

        except Exception as e:
            logging.critical(f"{e}\n{traceback.format_exc()}")



    @staticmethod
    def routine_data_collection():
        fetcher = Fetcher()
        prev_month_start, prev_month_end, prev_month_dt = TSM.get_prev_month_timestamps()
        relevant_stations_data = fetcher.fetch(prev_month_start, prev_month_end)
        station_2_code_notation_2_monthly_average, enough_data = DataProcessor(relevant_stations_data).process()
        report = SharePointReporter()
        if enough_data:
            report_path = CSVManager.update_entry(station_2_code_notation_2_monthly_average, prev_month_dt)
            message = f"Processed {prev_month_dt.strftime("%m/%Y")} data - status OK "
            report.message = message
            report.report_path = report_path
            if report.send():
                os.remove(report_path)
                logging.info("Deleted report from host - find it on sharepoint.")
        else:
            logging.warning("Not enough data from source..." +
                            "is it the beginning of a new month already?")





