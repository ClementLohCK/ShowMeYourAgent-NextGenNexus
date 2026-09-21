#!/usr/bin/env python3                                  
"""Submit observation reports via HTTP POST"""          
import requests                                         
import sys                                              
import json                                             
import os                                               
                                                    
# Configuration - update these values                   
API_BASE_URL = os.getenv('OBSERVATION_API_URL', 'https://webhook.site/aa3ed27a-94b3-4072-acaf-55f3703d29a6')                          
API_KEY = os.getenv('OBSERVATION_API_KEY', '')  # Store in secrets or env                                         
                                                          
def submit_observation(observation_data):               
    """                                                 
    Submit observation report via HTTP POST             
                                                        
    Args:                                               
        observation_data: dict containing the observation payload                                       
                                                        
    Returns:                                            
        Response JSON or raises exception               
    """                                                 
    # endpoint = f"{API_BASE_URL}/v1/maintenance/observations"
    endpoint = f"{API_BASE_URL}"
                                                        
    headers = {                                         
        'Content-Type': 'application/json',                                                                                                                                
        # 'Authorization': f'Bearer {API_KEY}',                                                                                     
    }                                                                                                                             
                                                                                                                                
    try:                                                                                                                          
        response = requests.post(                                                                                                 
            endpoint,                                                                                                             
            json=observation_data,                                                                                                
            headers=headers,                                                                                                      
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
        payload = json.loads(sys.argv[1])                                                                                         
        result = submit_observation(payload)
        print(json.dumps(result,indent=2))                                                                                                                                               
    # except json.JSONDecodeError as e:                                                                                                                     
    #     print(f"Invalid JSON: {e}", file=sys.stderr)                                                                                                      
    #     sys.exit(1)                                                                                                                                       
    except Exception as e:                                                                                                                                
        print(f"Error: {e}", file=sys.stderr)                                                                                                             
        sys.exit(1)