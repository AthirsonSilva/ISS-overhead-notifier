from time import sleep
import requests
from datetime import datetime
import smtplib

MY_EMAIL = 'botpythonmain@gmail.com'
ADDRS_EMAIL = 'athirsonarceus@gmail.com'
MY_PASSWORD = 'python310'
LAT = -23.534640
LNG = -46.423770


def near_me():
    '''
    ISS near user checker
    Gets the current user latitude and longitude cordinates
    and if the ISS satelyte is near him by plus or minus 5 or less
    it will return True
    Returns:
        bool: Returns True or False accordingly to the conditional check
    '''

    global LAT, LNG
    near_lat = False
    near_lng = False

    if iss_latitude == LAT or iss_latitude + 5 == LAT or iss_latitude - 5 == LAT:
        near_lat = True

    if iss_longitude == LAT or iss_longitude + 5 == LAT or iss_longitude - 5 == LAT:
        near_lng = True

    if near_lat and near_lng:
        return True

    else:
        return False


def is_dark():
    '''
    Night-time checker
    Checks if, in the user latitude and longitude cordinates,
    is night-time accordingly to the sunset-sunrise API reponse
    Returns:
        bool: Returns True or False accordingly to the conditional check
    '''

    global time_now, sunset

    if time_now.hour == sunset:
        return True

    return False


def email_sending(addrs):
    '''
    Email sender
    Simply sends a email to the destination
    provided on the function params
    Args:
        addrs (str): The destination email address
    Returns:
        str: A success message flag to know if the opperation was successfull
    '''

    global MY_EMAIL, MY_PASSWORD

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=addrs,
                            msg='Subject:ISS overhead\n\n'
                            'Look up! The ISS Satelyte is over your head passing through the space')

        return 'Success'


def main():
    '''
    Main code
    This function only exists so i can run it 
    every 60 seconds, nothing more
    '''

    global ADDRS_EMAIL

    # If the ISS is close to my current position and it is currently dark
    if near_me() and is_dark():
        # Then send me an email to tell me to look up.
        flag = email_sending(ADDRS_EMAIL)

        if flag == 'Success':
            print('Nice')


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": LAT,
    "lng": LNG,
    "formatted": 0,
}

response = requests.get(
    "https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now()


# BONUS: run the code every 60 seconds.

while True:
    if __name__ == '__main__':
        main()
        sleep(60)
