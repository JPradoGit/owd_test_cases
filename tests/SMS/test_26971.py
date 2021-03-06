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
class test_main(GaiaTestCase):
        
    _email        = "owdqatestone@gmail.com"
    _TestMsg     = "Test " + _email + " this."
    
    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.browser    = Browser(self)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.UTILS.getNetworkConnection()
        
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        self.messages.deleteAllThreads() 
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], self._TestMsg)
         
        #
        # Wait for the last message in this thread to be a 'received' one
        # and click the link.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(x, "Received a message.", True) 
        
        #
        #Verify that a valid URL appears highlight on message received.
        #
        y=x.find_element("tag name", "a")
        self.UTILS.TEST(y.text==self._email , "The email link is in the message received")
        
        #
        # Get the link of the first message
        #    
        w = self.UTILS.getElement( ("id", "message-1"), "Message sent")
        
        #
        #Verify that a valid URL appears highlight
        #
        z=w.find_element("tag name", "a")
        self.UTILS.TEST(z.text==self._email , "The email link is in the message sent")
                