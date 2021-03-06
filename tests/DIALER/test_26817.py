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
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.cont1 = MockContacts().Contact_1
        self.cont1["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        self.dialer.callLog_clearAll()

        self.dialer.enterNumber(self.cont1["tel"]["value"])
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()
        
        self.dialer.openCallLog()
        
        _number_el = DOM.Dialer.call_log_number_xpath % self.cont1["tel"]["value"]
        self.UTILS.waitForElements( ("xpath", _number_el),
                           "The number %s in the call log" % self.cont1["tel"]["value"])
        self.UTILS.waitForNotElements( ("xpath", "%s//*[text()='%s']" % (_number_el, self.cont1["name"])),
                           "The name %s in the call log" % self.cont1["name"])
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Call log <i>before</i> adding contact details for this number:", x)
        
        self.contacts.launch()
        self.contacts.createNewContact(self.cont1)
        
        self.dialer.launch()
        self.dialer.openCallLog()

        self.UTILS.waitForElements( ("xpath", DOM.Dialer.call_log_name_xpath % self.cont1["name"]),
                           "The name %s in the call log" % self.cont1["name"])
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Call log <i>after</i> adding contact details for this number:", x)

        