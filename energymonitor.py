import requests
import getpass
import json
from time import sleep


class Tesla():
    '''
        Methods:
        get_id - Vehicle identification number
        get_vehicle_general - Retrieve a list of your owned vehicles (includes vehicles not yet shipped!)
        get_charge_status - Information on the state of charge in the battery and its various settings.
        get_vehicle_data - A rollup of all the data request endpoints plus vehicle configuration.
        get_climate_state - Information on the current internal temperature and climate control system.
        get_drive_state - Returns the driving and position state of the vehicle.
        get_gui_settings - Returns various information about the GUI settings of the car, such as unit format and range display.
        get_vehicle_state - Returns the vehicle's physical state, such as which doors are open.
        get_vehicle_config - Returns the vehicle's configuration information including model, color, badging and wheels.
        get_mobile_enabled - Lets you know if the Mobile Access setting is enabled in the car.
        get_nearby_charging_sites - Returns a list of nearby Tesla-operated charging stations.
        wakeup - Wakes up the car from a sleeping state.


    '''
    def __init__(self):
        '''
            Initialization method serving to authenticate client and define necessary endpoints.
        '''
        # Client ID and Secret extracted from reverse engineered endpoint: https://tesla-api.timdorr.com/api-basics/authentication 
        self.URI = "https://owner-api.teslamotors.com"
        self.TESLA_CLIENT_ID = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384"
        self.TELSA_CLIENT_SECRET = "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"
        # Authenticate on instantiation
        self.auth()
        # Extract Vehicle ID on instantiation
        self.get_id()

        self.ENDPOINTS = {"vehicle_general" : "/api/1/vehicles",
                          "charge_status" : "/api/1/vehicles/{}/data_request/charge_state".format(self.id),
                          "vehicle_data" : "/api/1/vehicles/{}/vehicle_data".format(self.id),
                          "climate_state" : "/api/1/vehicles/{}/data_request/climate_state".format(self.id),
                          "drive_state" : "/api/1/vehicles/{}/data_request/drive_state".format(self.id),
                          "gui_settings" : "/api/1/vehicles/{}/data_request/gui_settings".format(self.id),
                          "vehicle_state" : "/api/1/vehicles/{}/data_request/vehicle_state".format(self.id),
                          "vehicle_config" : "/api/1/vehicles/{}/data_request/vehicle_config".format(self.id),
                          "mobile_enabled" : "/api/1/vehicles/{}/mobile_enabled".format(self.id),
                          "nearby_charging_sites" : "/api/1/vehicles/{}/nearby_charging_sites".format(self.id),
                          "wakeup" : "/api/1/vehicles/{}/wake_up".format(self.id),
                          "diagnostics" : "/api/1/diagnostics"
                          }

    def auth(self):
        '''
            Authentication method posts an authentication payload pre-defined with values provided by operator
            in the initialization parameters.
        '''
        auth_uri = "/oauth/token?grant_type=password"
        email = input("Please enter Tesla account email address: ")
        password = getpass.getpass(prompt='Please enter Tesla account password: ')
        self.auth_payload = {"grant_type": "password",
                             "client_id" : self.TESLA_CLIENT_ID,
                             "client_secret" : self.TELSA_CLIENT_SECRET,
                             "email" : email,
                             "password" : password
                            }

        response = requests.post('{}{}'.format(self.URI, auth_uri), json=self.auth_payload)
        response = json.loads(response.text)
        self.response = response
        self.access_token = response['access_token']
        self.refresh_token = response['refresh_token']
        # All requests invocations require an Authorization Bearer with access token
        self.header = {"Authorization" : "Bearer {}".format(self.access_token)}


    def get_id(self):
        '''
            Returns string with vehicle identification information.
        '''
        endpoint = "/api/1/vehicles"
        response = requests.get('{}{}'.format(self.URI, endpoint), headers=self.header)
        response = json.loads(response.text)
        response = response['response'][0]
        self.id = response['id']


    def get_charge_state(self):
        endpoint = self.ENDPOINTS['charge_status']
        response = requests.get('{}{}'.format(self.URI, endpoint), headers=self.header)
        response = json.loads(response.text)
        return response


    def get_vehicle_data(self):
        endpoint = self.ENDPOINTS['vehicle_data']
        response = requests.get('{}{}'.format(self.URI, endpoint), headers=self.header)
        response = json.loads(response.text)
        return response


    def get_vehicle_config(self):
        endpoint = self.ENDPOINTS['vehicle_config']
        response = requests.get('{}{}'.format(self.URI, endpoint), headers=self.header)
        response = json.loads(response.text)
        return response


    def wakeup(self):
        endpoint = self.ENDPOINTS['wakeup']
        response = requests.post('{}{}'.format(self.URI, endpoint), headers=self.header)
        response = json.loads(response.text)
        return response


    def diagnostics(self):
        endpoint = self.ENDPOINTS['diagnostics']
        response = requests.post('{}{}'.format(self.URI, endpoint), headers=self.header)
        response = json.loads(response.text)
        return response


