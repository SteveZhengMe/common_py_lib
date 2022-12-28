from datetime import datetime
import logging
import os
import unittest
import json
from mylogging import *
from myaws import *

class LoggingUnitTest(unittest.TestCase):
    def setUp(self):
        # loop the parent folder and delete the files that with the extension of .log
        for root, dirs, files in os.walk(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):
            for file in files:
                if file.endswith(".log"):
                    os.remove(os.path.join(root, file))
        
    
    def tearDown(self):
        pass
    
    def test_logging(self):
        logger = getLogger("test_logging",log_level=logging.DEBUG, save_debug_log=True)
        self.assertTrue(logger is not None)
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        
        # read the log file from parent folder
        for root, dirs, files in os.walk(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):
            for file in files:
                if file.endswith(".log"):
                    with open(os.path.join(root, file), "r") as f:
                        # read the file as a list of lines
                        lines = f.readlines()
                        # if the file name contains "_debug", the line count should be 5
                        if "_debug" in file:
                            self.assertTrue(len(lines) == 5)
                        # if the file name contains "_info", the line count should be 4
                        if "_info" in file:
                            self.assertTrue(len(lines) == 4)
                        # if the file name contains "_warn", the line count should be 3
                        if "_warn" in file:
                            self.assertTrue(len(lines) == 3)
                        # if the file name contains "_error", the line count should be 2
                        if "_error" in file:    
                            self.assertTrue(len(lines) == 2)
                            
class AWSUnitTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_sns(self):
        messageId = SNS(aws_region='us-east-1',for_testing=True).init_session(aws_profile="dev-admin").publish("YOUR_TOPIC", "test message")
        self.assertTrue(len(messageId) > 0)
    
    def test_cloudwatch(self):
        cw = CloudWatch(for_testing=True).init_session(aws_profile="dev-admin")
        current_datetime = datetime.now()
        for i in range(5):
            cw.ensure_log_group_stream_exist("delete_me", "aws_library_test")
            response_token = cw.put_log_event("delete_me", "aws_library_test", f"test message at {current_datetime}")
            self.assertTrue(response_token is not None)
    
    def test_secretManager(self):
        sm = SecretManager().init_session(aws_profile="dev-admin")
        secret = sm.get_secret("YOUR_SECRET_NAME")
        self.assertTrue(len(secret) > 0)
        
        parameter = sm.get_parameters(["Current-Environment-Name"])
        self.assertEqual(parameter["Current-Environment-Name"], "Dev")
        
        parameter = sm.get_parameters(["Current-Environment-Name","Current-Region-Name","Not-Exist-Parameter"])
        self.assertEqual(parameter, {"Current-Environment-Name": "Dev", "Current-Region-Name": "us-east-1", "Not-Exist-Parameter": None})
        
        returned = sm.replace_by_secrets(
            {  
                'user': '${mysql-username}',  
                'password': '${mysql-password}',  
                'host': '${mysql-host}',  
                'database': 'db_${mysql-db_name}_1',
                'raise_on_warnings':True,
                'port': '${port}'
            },
            ["YOUR_SECRET_NAME_1","YOUR_SECRET_NAME_2"]
        )
        self.assertTrue("$" not in json.dumps(returned) )
    
    def test_appConfig(self):
        appConfig = AppConfig(
            application="[application]", 
            app_profile="[profile]",
            environment="[environment]"
        ).init_session(aws_profile="dev-admin")
        
        config = appConfig.get_config()
        # Replace the above with your own config
        #self.assertTrue(config["error"] is None)