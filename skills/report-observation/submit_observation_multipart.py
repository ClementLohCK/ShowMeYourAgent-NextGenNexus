#!/usr/bin/env python3                                  
"""Submit observation reports via HTTP POST"""          
import requests                                         
import sys                                              
import json                                             
import os                                               
                                                    
# Configuration - update these values                   
API_BASE_URL = os.getenv('OBSERVATION_API_URL', 'https://webhook.site/aa3ed27a-94b3-4072-acaf-55f3703d29a6')                          
API_KEY = os.getenv('OBSERVATION_API_KEY', '')  # Store in secrets or env                                         
                                                          
def submit_observation(file_path, observation_data):
    # endpoint = f"{API_BASE_URL}/v1/maintenance/observations"
    endpoint = f"{API_BASE_URL}"
                                                        
    # headers = {                                         
    #     'Content-Type': 'application/json',                                                                                                                                
    #     # 'Authorization': f'Bearer {API_KEY}',                                                                                     
    # }                                                                                                                             
                                                                                                                                
    try:
        with open(file_path, 'rb') as f:
            # 'file' is the key expected by your target API's file slot
            files = {'file': (file_path.split('/')[-1], f, 'image/jpg')}
            response = requests.post(                                                                                                 
                endpoint,                                                                                                             
                data=observation_data,                                                                                                
                files=files,
                timeout=30                                                                                                            
            )                                                                                                                         
        response.raise_for_status()                                                                                               
        print("response raised for status")
        # return response.json()                                                                                                    
    except requests.exceptions.HTTPError as e:                                                                                    
        print(f"HTTP Error {response.status_code}: {response.text}", file=sys.stderr)                                             
        sys.exit(1)                                                                                                               
    # except requests.exceptions.RequestException as e:                                                                             
    #     print(f"Request failed: {e}", file=sys.stderr)                                                                            
    #     sys.exit(1)                                                                                                               

if __name__ == "__main__":                                                                                                        
    # if len(sys.argv) != 2:                                                                                                        
    #     print("Usage: submit_observation.py '<json_payload>'", file=sys.stderr)                                                   
    #     sys.exit(1)                                                                                                               
                                                                                                                                
    try:
        file_path = sys.argv[1]
        payload = json.loads(sys.argv[2])
        # file_path = '/home/panda/.openclaw/workspace/media/inbound/openclaw-staged-36b0e6d4-cda7-4094-a7dc-6fdf55ea0c35/input-bca7a080-adb5-4df0-9412-d7896eb87345.jpg'
        # payload = {"key1":"value1"}
        result = submit_observation(file_path, payload)
        print(json.dumps(result,indent=2))                                                                                                                                               
    # except json.JSONDecodeError as e:                                                                                                                     
    #     print(f"Invalid JSON: {e}", file=sys.stderr)                                                                                                      
    #     sys.exit(1)                                                                                                                                       
    except Exception as e:                                                                                                                                
        print(f"Error: {e}", file=sys.stderr)                                                                                                             
        sys.exit(1)