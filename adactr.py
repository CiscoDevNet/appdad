#!/usr/bin/env python
import json, re, sys, os, json, subprocess, time, logging, requests, urllib3
import boto3

from subprocess import call, check_output
from requests.structures import CaseInsensitiveDict
urllib3.disable_warnings()
APPD_SECRET = os.getenv('APPD_SECRET_POST')
APPD_CLIENTID = os.getenv('APPD_CLIENTID_POST')
APPD_SECRET_BASIC = os.getenv('APPD_SECRET_BAS')
APPD_CLIENTID_BASIC = os.getenv('APPD_CLIENTID_BAS')
base_url = os.getenv('BASE_URL')
ten_name = os.getenv('TEN_NAME')

# get http token
def get_token(ten_id):
    tokenurl = base_url + "/auth/" + ten_id + "/default/oauth2/token"
    payload='grant_type=client_credentials&client_id=' + APPD_CLIENTID + '&client_secret=' + APPD_SECRET
    print(payload)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", tokenurl, headers=headers, data=payload)
    print(response.json)
    token_json = response.json()
    appd_token = token_json['access_token']
    print(appd_token)
    return(appd_token)

# get token with Basic auth
def get_token_basic(ten_id):
    tokenurl = base_url + "/auth/" + ten_id + "/default/oauth2/token"
    payload='grant_type=client_credentials'
    # Authorization is base encoded APPD_SECRET_BASIC:APPD_SECRET_BASIC
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic c3J2XzNSWjRNbHlKbFRkZWlDbGNsNVp1MjM6emJPTkZYVnhnNTY0ZWJmTkNSYjZIOHBaQXhLdXJvVDhOUkl6MDBGajdzUQ=='
    }
    response = requests.request("POST", tokenurl, headers=headers, data=payload)
    print(response.json)
    token_json = response.json()
    appd_token = token_json['access_token']
    print(appd_token)
    return(appd_token)



# given tenant name, get ten id
def get_ten_id():
    tenurl = "https://observe-tenant-lookup-api.saas.appdynamics.com/tenants/lookup/" + ten_name

    print(tenurl)
    headers = {
      #  'Content-Type': 'application/json',
        'Accept': '*/*'
    }
    response = requests.request("GET", tenurl, headers=headers)
    json_object = json.loads(response.text)
    ten_id = json_object['tenantId']
    print(ten_id)
    return(ten_id)

def get_all_ads(appd_token, base_url):
    url = base_url + "/troubleshooting/v1beta/cogeng/adConfig?filter=order=acs&max=10&cursor"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    if response.ok:
        json_object = json.loads(response.text)
        print("Configured AD's:")
        print(json.dumps(json_object, indent = 3))
    else:
        print("Unable to retrieve AD Configs.")


def create_ad(appd_token, base_url, ad_name):
    url = base_url + "/troubleshooting/v1beta/cogeng/adConfig"
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
        "name": ad_name,
        "enabled": "true",
        "domain": "Infra",
        "entityTypes": [
            "aws:ec2"
        ],
        "modelSensitivity": "MEDIUM",
        "testMode": "false"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    print(response)
    if response.ok:
        json_object = json.loads(response.text)
        print("AD Config created:")
        print(json.dumps(json_object, indent = 3))
        token_json = response.json()
        cid = token_json['id']
        os.environ['CID'] = cid
        print(cid)
    else:
        print ("Could not create AD. May already exist.")
    

def get_adid_by_name(appd_token, base_url, conf_name):
    url = base_url + "/troubleshooting/v1beta/cogeng/adConfig?filter=order=acs&max=10&cursor"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    if response.ok:
        json_object = json.loads(response.text)
        items = json_object['items']
        if not items:
            return None
        else:
            content = json_object['items']
            for item in content:
                if(item['name'] == conf_name):
                    return(item['id'])
            return None
    else:
        return None

def disable_ad(appd_token, base_url, adid):
    url = base_url + "/troubleshooting/v1beta/cogeng/adConfig/" + adid
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
      "enabled": "false"
    }
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(data))
    if response.ok:
        json_object = json.loads(response.text)
        print("AD disabled:")
        print(json.dumps(json_object, indent = 3))
        token_json = response.json()
    else:
        print ("Could not update AD.")

def enable_ad(appd_token, base_url, adid):
    url = base_url + "/troubleshooting/v1beta/cogeng/adConfig/" + adid
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
      "enabled": "true",
      "modelSensitivity": "LOW"
    }
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(data))
    if response.ok:
        json_object = json.loads(response.text)
        print("AD enabled:")
        print(json.dumps(json_object, indent = 3))
        token_json = response.json()
    else:
        print ("Could not update AD.")

def update_ad(appd_token, base_url, adid, ad_name):
    url = base_url + "/troubleshooting/v1beta/cogeng/adConfig/" + adid 
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
              "name": "Sample AD Configuration",
              "enabled": true,
              "domain": "APM",
              "entityTypes": [
                "apm:service"
              ],
              "includeObjectFilter": "entities(apm:service)[attributes(\"service.name\") = 'valhalla']",
              "excludeObjectFilter": "entities(apm:service)[attributes(\"service.name\") = 'valhalla']",
              "modelSensitivity": "LOW"
    }

    
    response = requests.request("PUT", url, headers=headers, data=json.dumps(data))
    if response.ok:
        json_object = json.loads(response.text)
        print("AD Config updated:")
        print(json.dumps(json_object, indent = 3))
        token_json = response.json()
        cid = token_json['id']
        os.environ['CID'] = cid
        print(cid)
    else:
        print ("Could not update Health Rule.")

def delete_ad(appd_token, adid):
    url = base_url + "/troubleshooting/v1beta/cogeng/adConfig/" + adid
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    response = requests.request("DELETE", url, headers=headers)
    if response.ok:
        print("Successfully deleted health rule.")
    else:
        print ("Could not delete Configuration object.")

def get_all_actions(appd_token, base_url):
    url = base_url + "/alerting/v1beta/actions"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    if response.ok:
        json_object = json.loads(response.text)
        print("Configured Actions:")
        print(json.dumps(json_object, indent = 3))
    else:
        print("Unable to retrieve Actions. Regenerate API token and try again.")

def create_action(appd_token, base_url, action_name):
    url = base_url + "/alerting/v1beta/actions"
    print(action_name)
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
          "name": action_name,
          "type": "HTTP_REQUEST",
          "requestParameters": {
            "encodingType": "UTF-8",
            "rawUrl": "https://hooks.slack.com/services/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",
            "requestType": "POST"
          },
          "authentication": {
            "authenticationType": "NONE"
          },
          "requestHeaders": [

          ],
          "customVariables": [

          ],
          "requestPayload": {
            "encodingType": "UTF-8",
            "contentType": "application/json",
            "rawPayload": "{\"attachments\":[{\"text\": \"HRNAME=${eventList[0].health_rule_name},HRID=${eventList[0].health_rule_id},EVENT=${eventList[0].event_type_display_name}\"}],\"channel\": \"C03E507CAHM\",\"username\": \"Test alert\",\"icon_emoji\": \":appd:\"}"
          },
          "failureCriteria": [

          ],
          "successCriteria": [

          ],
          "connectionTimeoutMillis": "5000",
          "socketTimeoutMillis": "15000",
          "maxRedirects": "0"
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    if response.ok:
        json_object = json.loads(response.text)
        print("Action created:")
        print(json.dumps(json_object, indent = 3))
        token_json = response.json()
        cid = token_json['id']
        os.environ['CID'] = cid
        print(cid)
    else:
        print ("Could not create Action. May already exist.")

def get_actionid_by_name(appd_token, base_url, conf_name):
    url = base_url + "/alerting/v1beta/actions"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    #params = {'filter': 'displayName eq "' + conf_name + "\""}
    params = {}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    if response.ok:
        json_object = json.loads(response.text)
        items = json_object['items']
        if not items:
            return None
        else:
            content = json_object['items']
            for item in content:
                if(item['name'] == conf_name):
                    return(item['id'])
            return None
    else:
        return None

def update_action(appd_token, base_url, action_id, action_name):
    url = base_url + "/alerting/v1beta/actions/" + action_id
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
            "name": action_name,
            "enabled": "true",
            "type": "HTTP_REQUEST",
            "requestParameters": {
                "requestType": "POST",
                "rawUrl": "https://hooks.slack.com/services/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",
                "encodingType": "UTF-8"
            },
            "authentication": {
                "authenticationType": "NONE"
            }
        }

    response = requests.request("PUT", url, headers=headers, data=json.dumps(data))
    print(response)
    if response.ok:
        json_object = json.loads(response.text)
        print("Action updated:")
        print(json.dumps(json_object, indent = 3))
    else:
        print(response)
        print ("Could not update Action. May already exist.")

def delete_action(appd_token, action_id):
    url = base_url + "/alerting/v1beta/actions/" + action_id
    print(url)
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    response = requests.request("DELETE", url, headers=headers)
    if response.ok:
        print("Successfully deleted action.")
    else:
        print ("Could not delete action.")

def get_all_triggers(appd_token, base_url):
    url = base_url + "/alerting/v1beta/triggers"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    if response.ok:
        json_object = json.loads(response.text)
        print("Configured Triggers:")
        print(json.dumps(json_object, indent = 3))
    else:
        print("Unable to retrieve Triggers.")

def create_trigger(appd_token, base_url, tr_name, hr_id, ac_id):
    url = base_url + "/alerting/v1beta/triggers"
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
      "name": tr_name,
      "actionIds": [
        ac_id 
      ],
      "enabled": "true",
      "triggerCriteria": [
        {
          "eventType": "alerting:healthrule.violation",
          "matchingConditions": [
            {
              "property": "event_type",
              "operator": "CONTAINS",
              "values": [
                "Violation Started: Warning",
                "Violation Continues: Warning",
                "Violation Cancelled: Warning"
              ]
            },
            {
              "property": "config_id",
              "operator": "EQUALS",
              "values": [
                hr_id 
              ]
            }
          ]
        }
      ]
    }
    print("data:")
    print(data)

    
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    print(response)
    if response.ok:
        json_object = json.loads(response.text)
        print("Trigger created:")
        print(json.dumps(json_object, indent = 3))
        token_json = response.json()
        cid = token_json['id']
        os.environ['CID'] = cid
        print(cid)
    else:
        print ("Could not create Trigger. May already exist.")
    
def get_id_by_name(appd_token, url, conf_name):
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    if response.ok:
        json_object = json.loads(response.text)
        items = json_object['items']
        if not items:
            return None
        else:
            content = json_object['items']
            for item in content:
                print(item)
                if(item['name'] == conf_name):
                    return(item['id'])
            return None
    else:
        return None

def update_trigger(appd_token, base_url, tr_name, tr_id, hr_id, ac_id):
    url = base_url + "/alerting/v1beta/triggers/" + tr_id
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
      "name": tr_name ,
      "actionIds": [
        ac_id 
      ],
      "enabled": "true",
      "triggerCriteria": [
        {
          "eventType": "alerting:healthrule.violation",
          "matchingConditions": [
            {
              "property": "event_type",
              "operator": "CONTAINS",
              "values": [
                "Violation Started: Warning",
                "Violation Continues: Critical",
                "Violation Cancelled: Critical"
              ]
            },
            {
              "property": "config_id",
              "operator": "EQUALS",
              "values": [
                hr_id 
              ]
            }
          ]
        }
      ]
    }
    
    response = requests.request("PUT", url, headers=headers, data=json.dumps(data))
    if response.ok:
        json_object = json.loads(response.text)
        print("Trigger updated:")
        print(json.dumps(json_object, indent = 3))
    else:
        print ("Could not update Trigger")

def delete_trigger(appd_token, base_url, tr_name, tr_id):
    url = base_url + "/alerting/v1beta/triggers/" + tr_id
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
    }
    
    response = requests.request("DELETE", url, headers=headers, data=json.dumps(data))
    if response.ok:
        print("Trigger deleted:" + tr_name)
    else:
        print ("Could not update Trigger")

#ten_id=get_ten_id()
#appd_token = get_token(ten_id)
#appd_token = get_token_basic(ten_id)

#Anomaly Detection
#get_all_ads(appd_token, base_url)
#create_ad(appd_token, base_url, ad_name)
#get_adid_by_name(appd_token, base_url, conf_name)
#disable_ad(appd_token, base_url, adid)
#enable_ad(appd_token, base_url, adid)
#update_ad(appd_token, base_url, adid, ad_name)
#delete_ad(appd_token, adid)

#Actions
#get_all_actions(appd_token, base_url)
#create_action(appd_token, base_url, action_name)
#get_actionid_by_name(appd_token, base_url, conf_name)
#update_action(appd_token, base_url, action_id, action_name)
#delete_action(appd_token, action_id)

#Triggers
#get_all_triggers(appd_token, base_url)
#create_health_rule(appd_token, base_url, hr_name)
#create_action(appd_token, base_url, action_name)
#create_trigger(appd_token, base_url, tr_name, hr_id, ac_id)
#get_id_by_name(appd_token, url, conf_name)
#update_trigger(appd_token, base_url, tr_name, tr_id, hr_id, ac_id)
#delete_trigger(appd_token, base_url, tr_name, tr_id)




