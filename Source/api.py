import sys
import json
import requests

# Getting phone information via the FonApi.
class FonApi:

    # Url to the specific API
    __ApiUrl = 'https://fonoapi.freshpixl.com/v1/'

    # Initialize api Class.
    def __init__(self, apikey, url=None):
        self.__ApiUrl = FonApi.__ApiUrl
        if url is not None:
            self.__ApiUrl = url
        self.__ApiKey = apikey

    # Initialize the getDevicefunction of the API. Which returns a specific phone.
    def getdevice(self, device, position=None, brand=None):

        # Initialze relevant postdata / headers to the API. Return results.
        url = self.__ApiUrl + 'getdevice'
        postdata = {'brand': brand,
                    'device': device,
                    'position': position,
                    'token': self.__ApiKey}
        headers = {'content-type': 'application/json'}
        result = self.sendpostdata(url, postdata, headers)
        try:
            return result.json()
        except AttributeError:
            return result

    # Initialize the getlatestBrand function of the API. Which returns the lates phones from a brand.
    def getlatestBrand(self, limit, brand):

        # Initialze relevant postdata / headers to the API. Return results.
        url = self.__ApiUrl + 'getlatest'
        postdata = {'brand': brand,
                    'limit': limit,
                    'token': self.__ApiKey}
        headers = {'content-type': 'application/json'}
        result = self.sendpostdata(url, postdata, headers)
        try:
            return result.json()
        except AttributeError:
            return result

    # Initialize the getlatest function of the API. Which returns 100 phones unrelated to anything.
    def getlatest(self, limit):

        # Initialze relevant postdata / headers to the API. Return results.
        url = self.__ApiUrl + 'getlatest'
        postdata = {
                    'limit': limit,
                    'token': self.__ApiKey}
        headers = {'content-type': 'application/json'}
        result = self.sendpostdata(url, postdata, headers)
        try:
            return result.json()
        except AttributeError:
            return result

    # Send the json call to the servers from the API.
    def sendpostdata(self, url, postdata, headers, result = None):

        # Make the request.
        try:
            result = requests.post(url, data=json.dumps(postdata), headers=headers)

            # Consider any status other than 2xx an error.
            if not result.status_code // 100 == 2:
                return "Error status page: " + str(result)

            # Try send the result text else send the error.
            try:
                if result.json()['status'] == 'error':
                    if result.json()['message'] == 'Invalid Token. Generate a Token at fonoapi.freshpixl.com.':
                        return "Check __ApiKey"

                return result.json()['message']
            except:
                pass
            return result
        except requests.exceptions.RequestException as e:

            # A serious problem happened, like an SSLError or InvalidURL.
            return "Connect error. Check URL"

# Initialize fonAPI with secret key.
fon = FonApi('3618ac67ea1695322d52be3bca323ac4eb29caca9570dbe5')

# Getting a picture with a given keyword with the Qwant API.
class Qwant:

    # Returns image url of given phone.
    def get_image(phone):

        # Initialize headers and url.
        headers = {'User-Agent': 'Tellic'}
        url = "https://api.qwant.com/api/search/images?count=10&offset=1&q="+phone

        # Make the request
        data = requests.get(url, headers=headers).json()

        # Return only the specific picture url from the given json data set.
        return data['data']['result']['items'][0]['media']
