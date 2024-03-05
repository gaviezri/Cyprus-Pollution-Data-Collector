MANUAL_LINES = ["ONLY ONE FLAG PER RUN",
                "-h print man page",
                "-m+ <email address>                            # add recipient",
                "-m- <email address>                            # delete recipient",
                "-r <path to save report (absoulute/relative)>  # set report path",
                "-p+ <pollutant id>                             # add pollutant to collect averages on",
                "-p- <pollutant id>                             # remove pollutant...",
                "-s+ <station id>                               # add station to collect data from",
                "-s- <station id>                               # remove station..."
                ]

SWITCHES = {'-h', '-m+', '-m-', '-r', '-p+', '-p-', '-s+', '-s-'}


def print_man_page():
    for line in MANUAL_LINES:
        print(f"\t{line}\n")
