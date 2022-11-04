# Every AWS service is a class, the relevant methods will be included in the class

import json
import os
import base64
import time
import boto3
from mylogging import *

#################### SecretManager ####################
# TODO: Refactor, don't use Lambda
class SecretManager():
    def __init__(self, aws_account_id=None, aws_region=None):
        self.aws_logger = getLogger("my-aws")
        if aws_region is None:
            self.aws_region = os.environ.get("AWS_DEFAULT_REGION","")
        else:
            self.aws_region = aws_region
        
        if aws_account_id is None:
            self.aws_account_id = os.environ.get("AWS_ACCOUNT_ID","")
        else:
            self.aws_account_id = aws_account_id

    def get_secret(self, config_json, customized_secret_name=None, customized_lambda_function_name=None):
        # If there is the value in the parameter, use it. Otherwise use the value in the environment variable
        if customized_secret_name is None:
            secret_name = os.environ.get("SecretName","")
        else:
            secret_name = customized_secret_name
            
        if customized_lambda_function_name is None:
            lambda_function_name = os.environ.get("SecretsFunctionName","")
        else:
            lambda_function_name = customized_lambda_function_name
        
        if len(secret_name) > 0 and len(lambda_function_name) > 0 and len(self.aws_account_id) > 0 and len(self.aws_region) > 0:
            # Get the secrets    
            payload = {
                'secret': secret_name,
                'body': base64.b64encode(json.dumps(config_json).encode('utf-8')).decode('utf-8')
            }

            secrets_response = boto3.client("lambda").invoke(
                FunctionName = f"arn:aws:lambda:{self.aws_region}:{self.aws_account_id}:function:{lambda_function_name}",
                InvocationType = "RequestResponse",
                Payload=json.dumps(payload)
            )
            secret_content = secrets_response["Payload"].read().decode('utf-8')

            if secrets_response["StatusCode"] == 200:
                return json.loads(base64.b64decode(secret_content).decode('utf-8'))
            else:
                self.aws_logger.warning(f"Failed to get secret {secret_name} in {lambda_function_name}, ({self.aws_account_id}@{self.aws_region})")
        else:
            self.aws_logger.error(f"secret name, function name, account id or region is not set, secret_name={secret_name}, function_name={lambda_function_name}, account_id={self.aws_account_id}, region={self.aws_region}")
        
        return None

#################### SNS ####################
class SNS():
    def __init__(self, aws_account_id=None, aws_region=None, for_testing=False):
        self.aws_logger = getLogger("my-aws")
        if for_testing:
            self.adding_testing_message = "[[IGNORE THIS MESSAGE, IT'S FOR TESTING]] >>>>> "
        else:
            self.adding_testing_message = ""

        if aws_account_id is None:
            self.aws_account_id = os.environ.get("AWS_ACCOUNT_ID","")
        else:
            self.aws_account_id = aws_account_id
        
        if aws_region is None:
            self.aws_region = os.environ.get("AWS_DEFAULT_REGION","")
        else:
            self.aws_region = aws_region

    def publish(self, topic_name, message):
        sns_client = boto3.client('sns')
        
        response = sns_client.publish(
            TopicArn=f"arn:aws:sns:{self.aws_region}:{self.aws_account_id}:{topic_name}",
            Message=self.adding_testing_message + message
        )
        return response['MessageId']

#################### CloudWatch ####################
class CloudWatch():
    def __init__(self, for_testing=False):
        if for_testing:
            self.adding_testing_message = "[[IGNORE THIS MESSAGE, IT'S FOR TESTING]] >>>>> "
        else:
            self.adding_testing_message = ""

    def put_log_event(self, log_group_name, log_stream_name, message):
        # create a single log event as a list
        return self.put_log_events_list(log_group_name, log_stream_name, [message])
    
    def put_log_events_list(self, log_group_name, log_stream_name, message_list):
        # get the current timestamp
        timestamp = int(round(time.time() * 1000))
        # loop the message_list, add the timestamp to each message
        message_dict_list = []
        for message in message_list:
            message_dict_list.append({
                'timestamp':timestamp,
                'message':self.adding_testing_message + message
            })
        
        logs_client = boto3.client('logs')
        # push the log event to cloudwatch
        # get the sequence token by exactly matching the log stream name
        available_log_streams = logs_client.describe_log_streams(
            logGroupName=log_group_name, 
            logStreamNamePrefix=log_stream_name
        )['logStreams']
        
        # loop the log stream list, get the sequence token if the log stream name matches log_stream_name
        next_token = None
        for log_stream in available_log_streams:
            if log_stream['logStreamName'] == log_stream_name:
                # if the key uploadSequenceToken exists, use it
                if 'uploadSequenceToken' in log_stream:
                    next_token = log_stream['uploadSequenceToken']
                    break
        
        # send the log event
        if next_token is None:
            # for the first log, there is no sequence token
            response = logs_client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=message_dict_list
            )
        else:
            response = logs_client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=message_dict_list,
                sequenceToken=next_token
            )
        return response['nextSequenceToken']

    def put_metric(self,namespace,name,value,unit=None,timestamp=None,dimension_dict_list=None):
        metric_data = {
            'MetricName':name,
            'Value': value
        }
        if unit is not None:
            metric_data['Unit']: unit
        if dimension_dict_list is not None:
            metric_data['Dimensions'] = dimension_dict_list
        if timestamp is not None:
            metric_data['Timestamp'] = timestamp
        self.put_metric_list(namespace, [metric_data])

    def put_metric_list(self,namespace,metric_data_list):
        metric_client = boto3.client('cloudwatch')
        metric_client.put_metric_data(
            Namespace=namespace,
            MetricData=metric_data_list
        )

    