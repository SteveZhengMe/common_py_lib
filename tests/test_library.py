import logging
import os
import unittest
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
        sns = SNS()
        self.assertTrue(sns is not None)
    
    def test_cloudwatch(self):
        cw = CloudWatch()
        self.assertTrue(cw is not None)
    
    def test_secretManager(self):
        pass
        # sm = SecretManager()
        # self.assertTrue(sm is not None)