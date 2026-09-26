#!/usr/bin/env python3                                  
"""Submit observation reports via HTTP POST"""          
import requests                                         
import sys                                              
import json                                             
import os                                               
from datetime import datetime, timedelta
                                                    
# Configuration - update these values                   
API_BASE_URL = os.getenv('OBSERVATION_API_URL', 'https://webhook.site/d9691851-0919-49ff-b3ba-1e13979cfb3c')
API_KEY = os.getenv('OBSERVATION_API_KEY', '')  # Store in secrets or env                                         
                                                          
def log(level, message):
    level_labels = {'INFO': 'LOG', 'WARNING': 'WRN', 'ERROR': 'ERR'}
    label = level_labels[level.upper()]
    now = datetime.now().astimezone()
    workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(workspace_dir, 'logs')
    log_path = os.path.join(log_dir, f'{now.strftime("%Y%m%d")}.log')
    try:
        os.makedirs(log_dir, exist_ok=True)
        oldest_date = now.date() - timedelta(days=6)
        for filename in os.listdir(log_dir):
            try:
                log_date = datetime.strptime(filename, '%Y%m%d.log').date()
            except ValueError:
                continue
            if log_date < oldest_date:
                os.remove(os.path.join(log_dir, filename))
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f'{now.strftime("%Y%m%d_%H%M")}, {label}, {message}\n')
    except OSError:
        pass

def submit_observation(observation_data, file_path=''):
    # endpoint = f"{API_BASE_URL}/v1/maintenance/observations"
    endpoint = f"{API_BASE_URL}"
    headers = {
        'Accept': 'application/json',
        # 'Authorization': f'Bearer {API_KEY}'
        }
                                                                                                                                
    try:
        if file_path:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'image/jpg')}
                response = requests.post(
                    endpoint,
                    headers=headers,
                    data=observation_data,
                    files=files,
                    timeout=30
                )
        else:
            response = requests.post(
                endpoint,
                headers=headers,
                json=observation_data,
                timeout=30
            )
        response.raise_for_status()                                                                                               
        log('INFO', "response raised for status")
        return {"ok": True, "data": response.status_code}
    except requests.exceptions.HTTPError as e:                                                                                    
        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            log('ERROR', f"<<<<<<\nHTTPError 429 Too Many Requests, Retry-After: {retry_after}\n{response.text}\n>>>>>>")
        else:
            log('ERROR', f"<<<<<<\nHTTPError {response.status_code}: {response.text}\n>>>>>>")
        return {"ok": False, "data": str(e)}
    except requests.exceptions.RequestException as e:                                                                             
        log('ERROR', f"<<<<<<\nRequestException: {e}\n>>>>>>")
        return {"ok": False, "data": str(e)}

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
        print(json.dumps(result), flush=True)
    except json.JSONDecodeError as e:
        log('ERROR', f"<<<<<<\nInvalid JSON: {e}\n>>>>>>")
        print(json.dumps({"ok": False, "data": str(e)}), flush=True)
    except Exception as e:                                                                                                                                
        log('ERROR', f"<<<<<<\nError: {e}\n>>>>>>")
        print(json.dumps({"ok": False, "data": str(e)}), flush=True)