#Recaller

Get SMS about your upcoming events on your calendar.

Currently Supported:
    Google Calendar

Get Started:
    Add the following files to the application root directory before scheduling the script.
    
    1.Register the application in your Google console and download the client_id.json file.
    
    2.Create a calendars.json file and add your calendar array list in the below format.
        [ {
            "name" : <calendar name>,
            "type" : <calendar type>,
            "calendarId" : <find your calendar Id with your Calendar Provider>
        } ]
    
    3.create a sms-config.json file and your way2sms credentials as below.
        {
            "username" : <your way2sms mobile number>,
            "password" : <your way2sms password>
        }
    
    4.create a contacts.txt file and add one mobile number per line to send sms.
    
SMS Provider:
    Way2sms