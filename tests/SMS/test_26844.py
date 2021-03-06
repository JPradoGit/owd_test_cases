#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts

class test_main(GaiaTestCase):
    
    _TestMsg     = "Test message."
    
    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        #
        # Establish which phone number to use and set up the contact.
        #
        self.contact_1 = MockContacts().Contact_1
        
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")
        
        self.contact_1["tel"]["value"] = self.num1

        self.data_layer.insert_contact(self.contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch messages app.
        #
        self.messages.launch()
         
        #
        # Send a message to myself (long and short number to get a few threads).
        #
        self.messages.createAndSendSMS([self.num1,self.num2], "Test message")
        
        # Waiting for the replies isn't really part of the test, so just continue...
        
        x = self.UTILS.getElements(DOM.Messages.threads_list, "Threads")
        bool_1_target_ok  = False
        bool_2_target_ok  = False
        bool_1_time_ok    = False
        bool_2_time_ok    = False
        bool_1_snippet_ok = False
        bool_2_snippet_ok = False
        counter           = 1
        for i in x:
            #
            # Target details.
            #
            y = i.find_element('xpath', './/p[@class="name"]')
            self.UTILS.logResult("info", "Thread target: " + y.text)
            if y.text == self.contact_1["name"]:
                bool_1_target_ok = True
            if y.text == self.num2:
                bool_2_target_ok = True
                
            #
            # Time details.
            #
            y = i.find_element('tag name', 'time')
            self.UTILS.logResult("info", "Thread time: " + y.text)
            if counter == 1:
                bool_1_time_ok = True
            else:
                bool_2_time_ok = True
                
            #
            # Conversation snippet details.
            #
            y = i.find_element('xpath', './/span[@class="body-text"]')
            self.UTILS.logResult("info", "Thread conversation snippet: " + y.text)
            if counter == 1:
                bool_1_snippet_ok = True
            else:
                bool_2_snippet_ok = True
            
            #
            # Increment the counter.
            #    
            counter = counter + 1
            
        self.UTILS.TEST(bool_1_target_ok, "A thread exists for target " + self.contact_1["name"])
        self.UTILS.TEST(bool_2_target_ok, "A thread exists for target " + str(self.num2))
        
        self.UTILS.TEST(bool_1_time_ok, "A timestamp exists for thread 1.")
        self.UTILS.TEST(bool_2_time_ok, "A timestamp exists for thread 2.")
        
        self.UTILS.TEST(bool_1_snippet_ok, "A conversation snippet exists for thread 1.")
        self.UTILS.TEST(bool_2_snippet_ok, "A conversation snippet exists for thread 2.")
        
        