# This is a program to calculate the monthly averages of selected pollutants.
after the calculation, a summary of the results will be emailed to targets specified in config.json
data is collected from here - https://www.data.gov.cy/node/4441?language=en


Manual

To execute the collection and analysis of last month's data, simply invoke the program.
I found it best to work under Windows Task Scheduler.



 

The program currently supports the following flags; 

the application currently supports a single flag per invocation.

 

    -h                                     # print man page

    -m+ <email address>                    # add recipient

    -m- <email address>                    # delete recipient

    -r <absoulute path to save report>     # set report path

    -p+ <pollutant id>                     # add pollutant to collect averages on

    -p- <pollutant id>                     # remove pollutant...

    -s+ <station id>                       # add station to collect data from

    -s- <station id>                       # remove station...


Make sure to change SMTP server in email_reporter.

Also, in the same directory of config.json, create cred.json which should contain credentials for SMTP:

     {
       "username": <username>,
       "password": <password>
     }
  
