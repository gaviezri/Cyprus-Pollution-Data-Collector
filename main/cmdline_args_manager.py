import logging
import os.path
import sys
import json
from constants.config import CONFIG_PATH, EMAIL_TARGETS, POLLUTANTS, STATIONS, REPORT_PATH
from constants.manual import SWITCHES, print_man_page

config: dict = json.load(open(CONFIG_PATH, 'r'))


class ArgsManager:

    @staticmethod
    def handle_args():
        args = sys.argv[1:]
        if not ArgsManager.handle_help_or_misuse(args):
            match args[0][1:2]:
                case 'm':
                    specified_config = config[EMAIL_TARGETS]
                    handler = ArgsManager.modify_email_targets
                case 'r':
                    specified_config = config
                    handler = ArgsManager.modify_report_path
                case 'p':
                    specified_config = config[POLLUTANTS]
                    handler = ArgsManager.modify_pollutants
                case 's':
                    specified_config = config[STATIONS]
                    handler = ArgsManager.modify_stations
                case _:
                    print_man_page()
                    return
            ArgsManager.handle_request(specified_config, args, handler)

    @staticmethod
    def handle_help_or_misuse(args):
        misuse = True if sum([1 if arg.startswith('-') else 0 for arg in args]) > 1 else False
        unknown_flag = not (args[0] in SWITCHES)
        help_or_misuse = '-h' in args or misuse or unknown_flag
        if help_or_misuse:
            print_man_page()
        return help_or_misuse

    @staticmethod
    def handle_request(specified_config, args, handler):
        message, success = handler(specified_config, args)
        if message:
            print(message)
            if success:
                logging.info(message)
                json.dump(config, open(CONFIG_PATH, 'w'))
            else:
                logging.error(message)

    @staticmethod
    def modify_email_targets(specified_config, args):
        return ArgsManager.modify_resource(specified_config, args, "email targets")

    @staticmethod
    def modify_pollutants(specified_config, args):
        return ArgsManager.modify_resource(specified_config, args, "pollutants")

    @staticmethod
    def modify_stations(specified_config, args):
        return ArgsManager.modify_resource(specified_config, args, "stations")

    @staticmethod
    def modify_report_path(specified_config, args):
        new_report_path = args[1]
        if os.path.isdir(new_report_path):
            specified_config[REPORT_PATH] = new_report_path
            return f"successfully set report path to {new_report_path}", True
        else:
            return f"failed. {new_report_path} is not a valid directory.", False

    @staticmethod
    def modify_resource(specified_config, args, resource_name):
        if args[0][-1] == '+':
            specified_config.extend([args[1]])
            return f"successfully added {args[1]} to {resource_name}.", True
        elif args[0][-1] == '-':
            try:
                specified_config.remove(args[1])
                return f"successfully removed {args[1]} from {resource_name}.", True
            except ValueError:
                return f"could not remove {args[1]} from{resource_name}.", False
        return None, False
