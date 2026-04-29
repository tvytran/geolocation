import json
import time
import requests
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import concurrent.futures

load_dotenv()

def mail(id):
    api_key = os.environ.get('APP_P')

    send = "tvytran2@gmail.com"
    receive = "coding-challenges+alerts@sprinterhealth.com"
    password = api_key

    subject = "Testing Sprinter Mail - Thuy-Vy"
    body = "Alert: Clinician # " + str(id) + " is out of range!"

    message = MIMEMultipart()
    message["From"] = send
    message["To"] = receive
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=5) as server:
        server.starttls()
        server.login(send, password)
        server.send_message(message)

    print("email sent!")

def mail_error(id):
    api_key = os.environ.get('APP_P')

    send = "tvytran2@gmail.com"
    receive = "coding-challenges+alerts@sprinterhealth.com"
    password = api_key

    subject = "Testing Sprinter Mail - Thuy-Vy"
    body = "Alert: Clinician # " + str(id) + " is unreachable!"

    message = MIMEMultipart()
    message["From"] = send
    message["To"] = receive
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=5) as server:
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

def testing_api(u):
    #print("method called")
    number = u[-1]
    try:
        response = requests.get(u, timeout=5).json()
        print(response)
        coord = response['features'][0]['geometry']['coordinates'] #first features is coordinate to test
        coordInRange = False
        
        wholeFeature = response['features']
        #multiple range locations could be features list
        for p in range(1, len(wholeFeature)):
            geo_type =  response['features'][p]['geometry']['type']
            box = response['features'][p]['geometry']['coordinates']

            if geo_type == "Polygon":
                #multiple range location could be in coordinates list
                polygon_accept = box[0]
                if coord_in_range(coord, polygon_accept):
                    coordInRange = True
                for i in range(1, len(box)):
                    b = response['features'][p]['geometry']['coordinates'][i]
                    #print(b, "\n")
                    if coord_in_range(coord,b):
                        coordInRange = False
            elif geo_type == "MultiPolygon":
                for b in box:
                    polygon_accept = b[0]
                    if coord_in_range(coord, polygon_accept):
                        coordInRange = True




        if coordInRange == False:
            if number not in out_of_range:
                mail(number)
                out_of_range.add(number)
        else:
            if number in out_of_range:
                out_of_range.remove(number)
        if number in no_reach:
            no_reach.remove(number)
        print(out_of_range)
    except:
        if number not in no_reach:
            mail_error(number)
            no_reach.add(number)
        print("Error occured for clinician #", number)


#main method to test if api is 
'''
def testing_api(out_of_range):
    #obtaining all possible phlebotomists
    url = ["https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/1", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/2", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/3",
           "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/4", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/6"]
    #api_url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5" 

    number = 0
    for u in url:
        number+=1
        #turning api response to dictionary
        #print("===============================")

        #error checking
        try:
            response = requests.get(u).json()
            print(response)
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
        except:
            print("Error occured for clinician #", number)
            
        #print(coordInRange)


'''
if __name__ == '__main__':
    
    #mail(7)
    #seconds = time.time()
    #out_of_range = set()
    #no_reach = set()
    #testing_api("https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/2")
    
    
    out_of_range = set()
    no_reach = set()
    url = ["https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/1", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/2", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/3",
           "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/4", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/6"]
    
    for x in range(3600, 0, -1):
        s = time.time()
        with concurrent.futures.ThreadPoolExecutor(6) as executor:
            executor.map(testing_api, url)
            #print(out_of_range)
        #testing_api(out_of_range)

        seconds = x%60
        minutes = int(x/60)%60
        print(f"00:{minutes:02}:{seconds:02}")
        current_time = time.time() - s
        time.sleep(max(0, 1-current_time))
        #print(out_of_range)
    
    
    

    #testing_api(out_of_range)
    #testing_api()


    