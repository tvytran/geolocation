from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
import requests
import smtplib
from email.message import EmailMessage

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
    url = ["https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/1", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/2", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/3",
           "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/4", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5", "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/6",
                "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/7"]
    
    #api_url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/5" 
    

    for u in url:
        response = requests.get(u).json()
        print("===============================")
        if "error" in response:
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