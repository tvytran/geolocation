# Geo-Location

This project is a service that monitors the status of some clinicians and emails a specific address if any
is out of the designated safety zone. 

This solution is solved using three methods: mail(id), coords_in_range(coord, box), testing_api(out_of_range). 

mail(id) uses to SMTP (Simple-Mail-Transfer-Protocol) which sends messages to any valid email address on the internet. To send emails, I used a generated password by Google and stored it in an environmental file to be secure. Then I used the typical method to send emails with the library. The method also takes an id parameter in order to email the specific clinician that is out of range. 

coords_in_range(coord, box) is a ray-casting similar method that figures out if a the given coordinate is within the range of the polygon box given as well.

testing_api(u) is the main method that parses the json returned from calling the API in order to figure out if our clinician is in range. The first dictionary in the features list is always the location of the clinician. After that, the coordintes are the range of where the clinician should be. Once we get the range and the location of the clinician, we will call the coords_in_range method to test if the clinician is in range. There is also a global variable out_of_range set which should be a set that has all of the clinicians that are out of range. If a clinician turns out to be out of range, then the mail(id) function will be called and their id number will be added into the set so we avoid duplicating emails to the email address that will get the alerts. When we repeat this method, if the clinician that was out of range goes in range, they will be removed from the out of range set. 

Lastly, in the main method, a for loop will count down 3600 iterations, where each time it calls the testing_api(out_of_range) method with a ThreadPoolExecutor in order to only call the method every one second which will come out to 6 requests per second. 

