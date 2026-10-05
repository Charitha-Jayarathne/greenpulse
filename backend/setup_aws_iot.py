"""
GreenPulse AWS IoT Core Automated Setup Script
Configures:
1. AWS IoT Thing ('greenpulse-001')
2. X.509 Device Certificate & Private Key (active)
3. Download Amazon Root CA 1
4. IoT Policy with Connect, Publish, Subscribe permissions
5. Attach Policy and Thing to Certificate
6. AWS IoT Topic Rule ('greenpulse_sensor_rule') -> AWS Lambda ('greenpulse-process-sensor')
7. Lambda invoke permission for AWS IoT Core
8. Exports certificates and firmware/secrets.h for ESP32
"""

import json
import os
from pathlib import Path
import boto3
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
FIRMWARE_DIR = BASE_DIR.parent / "firmware"
CERTS_DIR = FIRMWARE_DIR / "certs"

load_dotenv(BASE_DIR / ".env")

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
DEVICE_ID = os.getenv("DEVICE_ID", "greenpulse-001")
LAMBDA_FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME", "greenpulse-process-sensor")
POLICY_NAME = "GreenPulseIoTPolicy"
RULE_NAME = "greenpulse_sensor_rule"
MQTT_TOPIC = "greenpulse/sensor/data"

iot_client = boto3.client("iot", region_name=AWS_REGION)
lambda_client = boto3.client("lambda", region_name=AWS_REGION)
sts_client = boto3.client("sts", region_name=AWS_REGION)

def setup_aws_iot():
    print("=" * 65)
    print("GreenPulse AWS IoT Core Setup (MQTT + TLS / mTLS Port 8883)")
    print("=" * 65)

    account_id = sts_client.get_caller_identity()["Account"]
    print(f"AWS Account ID : {account_id}")
    print(f"AWS Region     : {AWS_REGION}")
    print(f"Device ID      : {DEVICE_ID}")

    # 1. Get IoT Data ATS Endpoint
    endpoint_res = iot_client.describe_endpoint(endpointType="iot:Data-ATS")
    iot_endpoint = endpoint_res["endpointAddress"]
    print(f"IoT Endpoint   : {iot_endpoint}")

    # 2. Create IoT Thing
    print(f"\n[1/7] Creating IoT Thing '{DEVICE_ID}'...")
    try:
        iot_client.create_thing(thingName=DEVICE_ID)
        print("      Created successfully.")
    except iot_client.exceptions.ResourceAlreadyExistsException:
        print("      Thing already exists.")

    # 3. Create Keys and Certificate
    print("\n[2/7] Generating X.509 Keys and Certificate (Active)...")
    cert_res = iot_client.create_keys_and_certificate(setAsActive=True)
    certificate_arn = cert_res["certificateArn"]
    certificate_id = cert_res["certificateId"]
    certificate_pem = cert_res["certificatePem"]
    private_key = cert_res["keyPair"]["PrivateKey"]
    public_key = cert_res["keyPair"]["PublicKey"]
    print(f"      Certificate ID: {certificate_id}")

    # 4. Download Amazon Root CA 1
    print("\n[3/7] Fetching Amazon Root CA 1...")
    root_ca_url = "https://www.amazontrust.com/repository/AmazonRootCA1.pem"
    ca_res = requests.get(root_ca_url, timeout=10)
    root_ca_pem = ca_res.text
    print("      Amazon Root CA 1 downloaded.")

    # Save certs locally
    CERTS_DIR.mkdir(parents=True, exist_ok=True)
    (CERTS_DIR / "AmazonRootCA1.pem").write_text(root_ca_pem, encoding="utf-8")
    (CERTS_DIR / "certificate.pem.crt").write_text(certificate_pem, encoding="utf-8")
    (CERTS_DIR / "private.pem.key").write_text(private_key, encoding="utf-8")
    (CERTS_DIR / "public.pem.key").write_text(public_key, encoding="utf-8")
    print(f"      Saved all certs to {CERTS_DIR}")

    # 5. Create IoT Policy
    print(f"\n[4/7] Configuring IoT Policy '{POLICY_NAME}'...")
    policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["iot:Connect"],
                "Resource": f"arn:aws:iot:{AWS_REGION}:{account_id}:client/*"
            },
            {
                "Effect": "Allow",
                "Action": ["iot:Publish", "iot:Receive"],
                "Resource": f"arn:aws:iot:{AWS_REGION}:{account_id}:topic/greenpulse/*"
            },
            {
                "Effect": "Allow",
                "Action": ["iot:Subscribe"],
                "Resource": f"arn:aws:iot:{AWS_REGION}:{account_id}:topicfilter/greenpulse/*"
            }
        ]
    }

    try:
        iot_client.create_policy(
            policyName=POLICY_NAME,
            policyDocument=json.dumps(policy_doc)
        )
        print("      Created policy.")
    except iot_client.exceptions.ResourceAlreadyExistsException:
        print("      Policy already exists.")

    # 6. Attach Policy & Thing to Certificate
    print("\n[5/7] Attaching Policy and Thing to Certificate...")
    iot_client.attach_policy(policyName=POLICY_NAME, target=certificate_arn)
    iot_client.attach_thing_principal(thingName=DEVICE_ID, principal=certificate_arn)
    print("      Attached.")

    # 7. Create IoT Topic Rule to trigger Lambda
    print(f"\n[6/7] Creating IoT Rule to trigger Lambda '{LAMBDA_FUNCTION_NAME}'...")
    lambda_info = lambda_client.get_function(FunctionName=LAMBDA_FUNCTION_NAME)
    lambda_arn = lambda_info["Configuration"]["FunctionArn"]

    rule_payload = {
        "sql": f"SELECT * FROM '{MQTT_TOPIC}'",
        "description": "Routes GreenPulse sensor telemetry to Lambda decision engine and DynamoDB",
        "actions": [
            {
                "lambda": {
                    "functionArn": lambda_arn
                }
            }
        ],
        "ruleDisabled": False
    }

    iot_client.create_topic_rule(
        ruleName=RULE_NAME,
        topicRulePayload=rule_payload
    )
    print("      IoT Rule created.")

    # Grant IoT permission to invoke Lambda
    rule_arn = f"arn:aws:iot:{AWS_REGION}:{account_id}:rule/{RULE_NAME}"
    try:
        lambda_client.add_permission(
            FunctionName=LAMBDA_FUNCTION_NAME,
            StatementId=f"iot-invoke-{RULE_NAME}",
            Action="lambda:InvokeFunction",
            Principal="iot.amazonaws.com",
            SourceArn=rule_arn
        )
        print("      Lambda invoke permission granted to IoT Core.")
    except lambda_client.exceptions.ResourceConflictException:
        print("      Lambda invoke permission already present.")

    # 8. Generate firmware/secrets.h
    print("\n[7/7] Generating firmware/secrets.h for ESP32...")
    secrets_content = f"""#ifndef SECRETS_H
#define SECRETS_H

#include <pgmspace.h>

// WiFi Configuration (Enter your WiFi or Mobile Hotspot credentials)
const char WIFI_SSID[] = "YOUR_WIFI_NAME";
const char WIFI_PASSWORD[] = "YOUR_WIFI_PASSWORD";

// AWS IoT Core Configuration
const char AWS_IOT_ENDPOINT[] = "{iot_endpoint}";
const int  AWS_IOT_PORT = 8883;
const char DEVICE_ID[] = "{DEVICE_ID}";
const char MQTT_PUB_TOPIC[] = "{MQTT_TOPIC}";

// Amazon Root CA 1
const char AWS_CERT_CA[] PROGMEM = R"EOF(
{root_ca_pem.strip()}
)EOF";

// Device Certificate
const char AWS_CERT_CRT[] PROGMEM = R"EOF(
{certificate_pem.strip()}
)EOF";

// Device Private Key
const char AWS_CERT_PRIVATE[] PROGMEM = R"EOF(
{private_key.strip()}
)EOF";

#endif
"""
    secrets_path = FIRMWARE_DIR / "secrets.h"
    secrets_path.write_text(secrets_content, encoding="utf-8")
    print(f"      Generated {secrets_path}")

    print("\n" + "=" * 65)
    print("[OK] All AWS IoT Core components created & configured successfully!")
    print(f"Endpoint: {iot_endpoint}:8883")
    print(f"Topic   : {MQTT_TOPIC}")
    print("=" * 65)

if __name__ == "__main__":
    setup_aws_iot()
