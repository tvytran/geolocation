import json
import time
import requests
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def mail(id):
    api_key = os.environ.get('APP_P')

    send = "tvytran2@gmail.com"
    receive = "x0vgum+c1cpdu7rkexfk@sharklasers.com"
    password = api_key

    subject = "Testing Sprinter Mail - Thuy-Vy"
    body = "Alert: Clinician # " + str(id) + " is out of range!"

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


#main method to test if api is 
def testing_api(out_of_range):
    #obtaining all possible phlebotomists
    url = ["https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/1", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/2", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/3",
           "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/4", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/6"]
    #api_url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5" 

    number = 0
    for u in url:
        number+=1
        #turning api response to dictionary
        response = requests.get(u).json()
        #print("===============================")

        #error checking
        if "features" not in response:
            print("An error has occured.")
        else:
            coord = response['features'][0]['geometry']['coordinates'] #first features is coordinate to test
            coordInRange = False
            
            wholeFeature = response['features']
            #multiple range locations could be features list
            for p in range(1, len(wholeFeature)):
                box = response['features'][p]['geometry']['coordinates']
                #multiple range location could be in coordinates list
                for b in box:
                    #print(b, "\n")
                    if coord_in_range(coord,b):
                        coordInRange = True
            if coordInRange == False:
                if number not in out_of_range:
                    mail(number)
                    out_of_range.add(number)
            else:
                if number in out_of_range:
                    out_of_range.remove(number)
                
            #print(coordInRange)


if __name__ == '__main__':
    
    #mail(7)
    #seconds = time.time()
    
    out_of_range = set()
    for x in range(3600, 0, -1):
        testing_api(out_of_range)
        seconds = x%60
        minutes = int(x/60)%60
        print(f"00:{minutes:02}:{seconds:02}")
        time.sleep(1)
    
    #testing_api()


    