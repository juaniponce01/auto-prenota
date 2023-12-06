import pytextnow

client = pytextnow.Client("username", sid_cookie="sid", 
csrf_cookie="csrf")

client.send_sms("number", "Hello World!")
