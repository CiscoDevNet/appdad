# Use Anomaly Detection to Monitor Entity Health with Cloud Cloud Observability
## Contents
        Use Cases
        Pre-requisites, Guidelines
        Python API Client - Anamoly Detection, Actions, Trigger 
        Getting the API Token
        Exploring Anamoly Detection API
        Exploring Actions API
        Exploring Trigger API
        Data Generation to trigger and clear events
        De-provisioning

### Use Cases
        * As a Cloud Admin, you have already provisioned cloud connections to AWS leveraging AppD 
        Cloud Connections API to pull metrics data from AWS Services (Load 
        Balancers, Storage, Hosts, Databases)
        * As Infra Ops, set up anomaly detection for AWS EC2 instances to alert on thresholds exceeded for CPU Utilization
        * As DevOps/AppOps, be notified of thresholds exceeded for the underlying infrastructure

### Pre-requisites, Guidelines

1. Requires Cloud Cloud Observability Tenant, ClientID and Secret. For the purposes of this exercise, we will reserve a sandbox and get the required data from it.

https://dcloud2-rtp.cisco.com/content/instantdemo/appdynamics-observability-in-aws

Copy the valiues in the last column under DevNet. You will set the ENV variables for these parameters that will be used in the API Client:

![Copy Global Variables](https://github.com/prathjan/images/blob/main/reserve2.png?raw=true)

### Python API Client - Anamoly Detection, Actions, Trigger

Check out a sample python client to exercise the Anamoly Detection/Actions/Triggers API's here: 
https://github.com/CiscoDevNet/appdhr/blob/main/hractr.py 

Before running the python client, set up the following environment variables (sample values displayed):

        %env APPD_CLIENTID_AGT=agt_6DbMBU1d6zmQqBlEQCr7ir
        %env APPD_SECRET_AGT=k4hOZYQrZ5B5zHh3r0mn4ZrqwebVrQN18b-yTdDaO9Q
        %env APPD_CLIENTID_POST=srv_3yvuCrMr0FCpNuVigRsvqk
        %env APPD_SECRET_POST=Hjl5tOMqpTixfBo8LxsFVYk7m_OW5nPMTFTG29LdyvM
        %env APPD_CLIENTID_BASIC=srv_eAbU1aJOWGcjsxKUta9b8
        %env APPD_SECRET_BASIC=0oiakaHCkzSRmuRdHOJiAoCN2wN8xdFtzCFAOyCLdNs
        %env TENANT_NAME=cisco-devnet
        %env AWS_ACCESS_KEY=AKIAXQ7ZIQP4W7VTJIXC
        %env ID=AKIAXQ7ZIQP4W7VTJIXC
        %env AWS_SECRET_KEY=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
        %env AWS_CONNECTION_NAME=prathjan-a3ed1d35c8b1427db12033d921d747fc
        %env CL_ID=agt_6DbMBU1d6zmQqBlEQCr7ir
        %env CL_SEC=k4hOZYQrZ5B5zHh3r0mn4ZrqwebVrQN18b-yTdDaO9Q

 Try the Python API Client provided to execute the following:

### Getting the API Token

        * Generate Tenant ID - get_ten_id()
        * Generate token with POST authentication - get_token(ten_id)
        * Generate token with Basic authentication - get_token_basic(ten_id)


### Exploring Anamoly Detection API

Please refer to the following devnet resource for a complete API definition: 

https://developer.cisco.com/docs/appdynamics/anomaly-detection/#!api-reference

Some of the API's included in the sample python client are as follows and accounts for the anomaly detection config resource lifecycle. 

        * Get the list of anomaly detection configs for a tenant - get_all_ads(appd_token, base_url)
        * Create anomaly detection config for a tenant - create_ad(appd_token, base_url, ad_name)
        * Get anomaly detection config ID by name - get_adid_by_name(appd_token, base_url, conf_name)
        * Disable the anomaly detection config - disable_ad(appd_token, base_url, adid)
        * Enable the anomaly detection config - enable_ad(appd_token, base_url, adid)
        * Modify a anomaly detection config - update_ad(appd_token, base_url, adid, ad_name)
        * Delete a anomaly detection config - delete_ad(appd_token, adid)

### Exploring Actions API

Please refer to the follwing devnet resources for a complete API definition: 

https://developer.cisco.com/docs/appdynamics/actions/#!introduction

Some of the API's included in the sample python client are as follows and accounts for the actions object lifecycle. 

        * Get All Actions - get_all_actions(appd_token, base_url)
        * Get an Action by Identifier - get_actionid_by_name(appd_token, base_url, conf_name)
        * Create an Action - create_action(appd_token, base_url, action_name)
        * Update an Action by Identifier - update_action(appd_token, base_url, action_id, action_name)
        * Delete an Action by Identifier - delete_action(appd_token, action_id)

### Exploring Trigger API

Please refer to the follwing devnet resources for a complete API definition: 

https://developer.cisco.com/docs/appdynamics/actions/#!introduction 

Some of the API's included in the sample python client are as follows and accounts for the trigger object lifecycle. 

        * Get All Triggers - get_all_triggers(appd_token, base_url)
        * Create a Trigger - create_trigger(appd_token, base_url, tr_name, hr_id, ac_id)
        * Get a Trigger by Identifier - get_id_by_name(appd_token, url, conf_name)
        * Update a Trigger by Identifier - update_trigger(appd_token, base_url, tr_name, tr_id, hr_id, ac_id)
        * Delete a Trigger by Identifier - delete_trigger(appd_token, base_url, tr_name, tr_id)

### Data Generation to trigger and clear events

#### Create Anamoly Detection, Action, Trigger

Use the above API's to do the following before you generate data. This is assuming that you do not have a HR, action,trigger provisioned.

* Create a Anamoly Detection

* Create an Action 

* Create a Trigger 

#### Prepare Data Generator

You will be running the datagenerator from your local computer. To run the data generator, you will need java installed on your local computer.

Open a Terminal and create a datagen directory: <your_local_datagen_dir>.

In this directory, you will git clone the following data generator git repo, prepare the data files and run the data generator from you local computer:

git clone https://github.com/CiscoDevNet/appdhrdata.git

You will see the following files in the datagen directory: <your_local_datagen_dir>:

        ati-vodka-local-all.jar	
        platformtarget.yml	
        trigger.yml
        clear.yml		
        resource.yml

#### Data generation for Anomaly Detection

It takes 48 hours for Anomaly Detection to become available for your monitored entities. During that time, the machine learning models train on the entities in your application.

We will not be able to wait for 48 hours for the machine learning to complete in this learning lab due to its limited activity time. However, we will cover the utilities and methodologies that you can use in your own AppDynamics Platform to experiment with this.

To generate some utilization data that is in the range of CPU Utilization of 25% - 35% and train the ML models, you can use gennormdata.yml. 

        cat gennormdata.yml

                payloadFrequencySeconds: 30
                payloadCount: 300
                metrics:
                - name: infra:system.cpu.used.utilization
                unit: '%'
                otelType: summary
                valueFunction: 'randomSummary(25, 55, "", 5)'
                quantiles: [0, 0.5, 1]
                reportingEntities: [ec2]
                isDouble: true 

#### Resource configuration

Let's simulate EC2 resources here. The health rules have been configured for EC2 resources and so thresholds configured will apply to these EC2 instances.

We will generate some unique EC2 instance ID's using the AWS account number configured for this lab. 

Execute the following code blocks to generate resource.yml which you will then copy to <your_local_datagen_dir>/resource.yml.

        cat resource.yml
        echo $ID
        echo "ID is" $ID
        sed "s/%accnum%/$ID/g" resource.yml > /tmp/resource.yml
        cat /tmp/resource.yml

#### Update local resource.yml

Cut and paste contents of /tmp/resource.yml above to your local <your_local_datagen_dir>/resource.yml.

#### Platform configuration

To run the data generator, we need to configure the agent client ID and secret. Execute the following code blocks to generate platformtarget.yml which you will then copy to /platformtarget.yml.

        cat platformtarget.yml
        echo $CL_ID
        echo "CL_ID is" $CL_ID
        echo $CL_SEC
        echo "CL_SEC is" $CL_SEC
        sed "s/%clientId%/$CL_ID/g" platformtarget.yml > /tmp/platformtarget1.yml
        sed "s/%clientsec%/$CL_SEC/g" /tmp/platformtarget1.yml > /tmp/platformtarget.yml
        cat /tmp/platformtarget.yml

#### Update local platformtarget.yml

Cut and paste contents of /tmp/platformtarget.yml above to your local <your_local_datagen_dir>/platformtarget.yml.

#### Trigger high CPU Utilization event

To generate high CPU utilization data that will trigger the threshold exceeded events in CNAO, let's run the following script in <your_local_datagen_dir>. 

Let it run contunuously to give it time to generate some valid data to populate the UI as well as send notifications to Slack.You can view data in UI and Slack before you stop this data generation.

        cd <your_local_datagen_dir>
        java -jar ati-vodka-local-all.jar -c /tmp/platformtarget.yml -e /tmp/resource.yml -m gennormdata.yml

#### View AWS EC2 Metrics in UI

Click on Observe in your reservation window and you will land in the Observe page of Cloud Native Application Observability.

![dCloud page](https://github.com/prathjan/images/blob/main/reserve2.png?raw=true)

Click on the following and pick the host that applies to your sandbox. It will be of the format "Lab i-" <your AWS account#>:
https://cisco-devnet.observe.appdynamics.com/ui/observe/infra/host?filter=isActive%20%3D%20true&since=now-1h

![alt text](https://github.com/prathjan/images/blob/main/hostlist.png?raw=true)

Click on the applicable host to view details:

![alt text](https://github.com/prathjan/images/blob/main/metuiex.png?raw=true)

#### Anomaly Detection Events

As indicated earlier, it takes about 48 hours for the machine learning models to train. Above, we generated EC2 utilization data in the range of 25%-35%.

To generate AD notifications, we can now generate data above the range that we trained for. You can use genabnormdata.yml for this. This starts generating utilization data in the range of 75-95% which is much above the model that we trained for. 

Before you run the java utility listed below, make sure you have terminated the previous datageneration that you started above.

        cat genabnormdata.yml
                payloadFrequencySeconds: 30
                payloadCount: 300
                metrics:
                - name: infra:system.cpu.used.utilization
                unit: '%'
                otelType: summary
                valueFunction: 'randomSummary(75, 95, "", 5)'
                quantiles: [0, 0.5, 1]
                reportingEntities: [ec2]
                isDouble: true 

        cd <your_local_datagen_dir>
        java -jar ati-vodka-local-all.jar -c /tmp/platformtarget.yml -e /tmp/resource.yml -m genabnormdata.yml

#### Monitor  Anamolies

If anamolies were detected, you will see updates to the following and will see your AD Configuration flagged here:

![alt text](https://github.com/prathjan/images/blob/main/metuicl.png?raw=true)

For more info on Monitoring Anamolies, please refer to:

[Monitor Anamolies](https://docs.appdynamics.com/fso/cloud-native-app-obs/en/monitor-entity-health/anomaly-detection/monitor-anomalies).

### De-provisioning

The API client provides routines to do the following.

* Delete a health rule

* Delete an Action by Identifier

* Delete a Trigger by Identifier

cat trigger.yml 

        
