import logging

logging.basicConfig(filename="out.log",
                    format="%(asctime)s ### %(levelname)s ### %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S",
                    level=logging.INFO)
