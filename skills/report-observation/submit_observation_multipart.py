#!/usr/bin/env python3                                  
"""Submit observation reports via HTTP POST"""          
import requests                                         
import sys                                              
import json                                             
import os                                               
                                                    
# Configuration - update these values                   
API_BASE_URL = os.getenv('OBSERVATION_API_URL', 'https://webhook.site/81a9c287-9965-46a0-853e-dadf9287df02')
API_KEY = os.getenv('OBSERVATION_API_KEY', '')  # Store in secrets or env                                         
                                                          
def submit_observation(observation_data, file_path=''):
    # endpoint = f"{API_BASE_URL}/v1/maintenance/observations"
    endpoint = f"{API_BASE_URL}"
                                                        
    # headers = {                                         
    #     'Content-Type': 'application/json',                                                                                                                                
    #     # 'Authorization': f'Bearer {API_KEY}',                                                                                     
    # }                                                                                                                             
                                                                                                                                
    try:
        if file_path:
            with open(file_path, 'rb') as f:
                # 'file' is the key expected by your target API's file slot
                files = {'file': (os.path.basename(file_path), f, 'image/jpg')}
                response = requests.post(
                    endpoint,
                    data=observation_data,
                    files=files,
                    timeout=30
                )
        else:
            response = requests.post(
                endpoint,
                data=observation_data,
                timeout=30
            )
        response.raise_for_status()                                                                                               
        print("response raised for status")
        # return response.json()                                                                                                    
    except requests.exceptions.HTTPError as e:                                                                                    
        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            message = ("HTTP 429 Too Many Requests.")
            if retry_after:
                message += f" Retry-After: {retry_after}."
            print(message, file=sys.stderr)
        else:
            print(
                f"HTTP Error {response.status_code}: {response.text}",
                file=sys.stderr
            )
        sys.exit(1)                                                                                                               
    # except requests.exceptions.RequestException as e:                                                                             
    #     print(f"Request failed: {e}", file=sys.stderr)                                                                            
    #     sys.exit(1)                                                                                                               

if __name__ == "__main__":                                                                                                        
    try:
        if len(sys.argv) not in (2, 3):
            raise ValueError(
                "Usage: submit_observation_multipart.py '<json_payload>' [image_path]"
            )
        payload = json.loads(sys.argv[1])
        file_path = sys.argv[2] if len(sys.argv) == 3 else ''
        # file_path = '/home/panda/.openclaw/workspace/media/inbound/openclaw-staged-36b0e6d4-cda7-4094-a7dc-6fdf55ea0c35/input-bca7a080-adb5-4df0-9412-d7896eb87345.jpg'
        # payload = {"key1":"value1"}
        result = submit_observation(payload, file_path)
        print(json.dumps(result,indent=2))                                                                                                                                               
    # except json.JSONDecodeError as e:                                                                                                                     
    #     print(f"Invalid JSON: {e}", file=sys.stderr)                                                                                                      
    #     sys.exit(1)                                                                                                                                       
    except Exception as e:                                                                                                                                
        print(f"Error: {e}", file=sys.stderr)                                                                                                             
        sys.exit(1)