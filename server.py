import json
import requests
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def mail():
    load_dotenv()
    api_key = os.environ.get('APP_P')

    send = "tvytran2@gmail.com"
    receive = "tvytran2@gmail.com"
    password = api_key

    subject = "Testing Sprinter Mail"
    body = "Hello, I am testing this."

    message = MIMEMultipart()
    message["From"] = send
    message["To"] = receive
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(send, password)
        server.send_message(message)

    print("email sent!")


def coord_in_range(coord, box):
    vertices = len(box)
    x = coord[0]
    y = coord[1]
    inside = False

    c1 = box[0]
    #print("c1", c1[1])

    for i in range(1, vertices+1):
        c2 = box[i%vertices]

        if y > min([c1[1],c2[1]]):
            if y <= max(c1[1],c2[1]):
                if x <= max(c1[0],c2[0]):
                    x_intersection = (y-c1[1]) * (c2[0]-c1[0])/(c2[1]-c1[1]) + c1[0]

                    if c1[0] == c2[0] or x <= x_intersection:
                        inside = not inside
        
        c1 = c2
    return inside

if __name__ == '__main__':

    mail()


    #obtaining all possible phlebotomists
    url = ["https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/1", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/2", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/3",
           "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/4", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/6",
                "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/7"]
    
    #api_url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5" 

    load_dotenv()
    api_key = os.environ.get('APP_P')
    print(api_key)
    
    for u in url:
        #turning api response to dictionary
        response = requests.get(u).json()
        print("===============================")
        if "features" not in response:
            print("An error has occured.")
        else:
            coord = response['features'][0]['geometry']['coordinates']
        # print(type(coord[0]))

            coordInRange = False
            
            wholeFeature = response['features']
            for p in range(1, len(wholeFeature)):
                box = response['features'][p]['geometry']['coordinates']
                for b in box:
                    print(b, "\n")
                    if coord_in_range(coord,b):
                        coordInRange = True
            print(coordInRange)



            #print(box)
            #print(type(box))
            #print(coord_in_range(coord,box))
        
    


    


    

