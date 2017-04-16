#Recaller

Get SMS about your upcoming events on your calendar.

Currently Supported:
    Google Calendar

Get Started:
    Add the following files to the application root directory before scheduling the script.
    
    1.Register the application in your Google console and download the client_id.json file.
    
    2.Create a calendars.json file and add your calendar array list in the below format.
        [ {
            "name" : <calendar_name>,
            "type" : <calendar_type>,
            "calendarId" : <find_your_calendar_Id_with_your_Calendar_Provider>
        } ]
    
    3.create a sms-config.json file and your way2sms credentials as below.
        {
            "username" : <your_way2sms_mobile_number>,
            "password" : <your_way2sms_password>
        }
    
    4.create a contacts.txt file and add one mobile number per line to send sms.
    
    Run the script to and follow the instructions to sign in.
 
To schedule the script to run daily:
    Linux:
        use crontab
        open the crontab file using the following command
          
           crontab -e
          
        Add the following line in the file
           
           <min> <hour> * * * cd <path_to_the_recaller_directory>/recaller && ./recaller.py
    
    
SMS Provider:
    Way2sms