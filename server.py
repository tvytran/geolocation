from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
import requests
import smtplib
from email.message import EmailMessage



if __name__ == '__main__':
    url = ["https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/1", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/2", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/3",
           "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/4", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/6",
                "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/7"]
    
    #api_url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5" 
    

    for u in url:
        response = requests.get(u).json()
        print(response['features'][0]['geometry']['coordinates'])


    '''
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("liv82084@gmail.com", "Mangoapp2026!")
    # message to be sent
    message = "hello"
    # sending the mail
    s.sendmail("liv82084@gmail.com", "liv82084@gmail.com", message)
    # terminating the session
    s.quit()
    '''