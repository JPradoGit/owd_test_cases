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
    
    _RESTART_DEVICE = True
    _now=""
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        self.num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.UTILS.setTimeToNow()
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # When this is unblocked it will be much quicker to do this
        # than reset the device.
        #
#         self.messages.launch()
#         self.messages.deleteAllThreads()

        #
        # Remember the 'real' current date and time.
        #
        one_day        = 24*60*60
        self.NOW_EPOCH = time.time()
        self._now      = self.UTILS.getDateTimeFromEpochSecs(self.NOW_EPOCH)

        #
        #=============================================================================
        #
        self.UTILS.logResult("info", " ")
        self.UTILS.logResult("info", "--------------------------")
        self.UTILS.logResult("info", "<b><u>Reading an sms from 2 months ago ...</u></b>")
        
        t = self.UTILS.getDateTimeFromEpochSecs(self.NOW_EPOCH - (64 * one_day))
        x = self.UTILS.setTimeToSpecific(p_year=t.year, p_month=t.mon, p_day=t.mday)
        
        expected_str = "%s/%s/%s" % (str(t.mon).zfill(2), str(t.mday).zfill(2), t.year)
          
        self._sendSMS("2 months ago", True)         
        self._checkTimeStamp(expected_str)
  
 
        #
        #=============================================================================
        #
        self.UTILS.logResult("info", " ")
        self.UTILS.logResult("info", "--------------------------")
        self.UTILS.logResult("info", "<b><u>Reading an sms from 6 days ago ...</u></b>")
        
        t = self.UTILS.getDateTimeFromEpochSecs(self.NOW_EPOCH - (64 * one_day))
        x = self.UTILS.setTimeToSpecific(p_year=t.year, p_month=t.mon, p_day=t.mday)
        
        expected_str = "%s/%s/%s" % (str(t.mon).zfill(2), str(t.mday).zfill(2), t.year)
          
        self._sendSMS("6 days ago")         
        self._checkTimeStamp(expected_str)
          

        #
        #=============================================================================
        #
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(5,1,-1):
  
            self.UTILS.logResult("info", " ")
            self.UTILS.logResult("info", "--------------------------")
            t = self.UTILS.getDateTimeFromEpochSecs(self.NOW_EPOCH - (i * one_day))
            x = self.UTILS.setTimeToSpecific(p_year=t.year, p_month=t.mon, p_day=t.mday)
            
            _dayname = days[x.tm_wday]
            self.UTILS.logResult("info", "<b><u>Reading an sms from %s days ago (%s) ...</u></b>" % (str(i), _dayname))
              
            self._sendSMS("DAY: %s (%s days ago)." % (_dayname, str(i)))
            self._checkTimeStamp(_dayname)
              
              
        #
        #=============================================================================
        #
        self.UTILS.logResult("info", " ")
        self.UTILS.logResult("info", "--------------------------")
        self.UTILS.logResult("info", "<b><u>Reading an sms from yesterday ...</u></b>")
        t = self.UTILS.getDateTimeFromEpochSecs(self.NOW_EPOCH - (1 * one_day))
        x = self.UTILS.setTimeToSpecific(p_year=t.year, p_month=t.mon, p_day=t.mday)
        self._sendSMS("DAY: YESTERDAY")
        self._checkTimeStamp("YESTERDAY")
    
    
        #
        #=============================================================================
        #
        self.UTILS.logResult("info", " ")
        self.UTILS.logResult("info", "--------------------------")
        self.UTILS.logResult("info", "<b><u>Reading an sms from today ...</u></b>")
        self.data_layer.set_time( self.NOW_EPOCH * 1000)
 
        self._sendSMS("DAY: TODAY")
        self._checkTimeStamp("TODAY")
        
        
    def _sendSMS(self, p_str, p_first_time=False):
        #
        # Sends an sms (a little quicker if not p_firs_time).
        #
        self.messages.launch()
        if p_first_time:
            # No thread yet, so start from scratch.
            self.messages.createAndSendSMS([self.num], p_str)
        else:
            # Thread exists, so just use it.
            self.messages.openThread(self.num)
            self.messages.enterSMSMsg(p_str)
            self.messages.sendSMS()
            
        self.messages.waitForReceivedMsgInThisThread()
        self.apps.kill_all()
        
    def _checkTimeStamp(self, p_str):
        #
        # Sets the device time back to 'now', opens the sms / thread and
        # checks that the expected timestamp header is present.
        #
        # This is slow, but I can't find a way to see headers that are off the top
        # of the screen, so I ended up doing it this way.
        #
        self.UTILS.logResult("info", "Setting device time back to the 'real' date and time.")
        self.data_layer.set_time(self.NOW_EPOCH * 1000)

        self.UTILS.waitForDeviceTimeToBe( p_year=self._now.year,
                                          p_month=self._now.mon,
                                          p_day=self._now.mday,
                                          p_hour=self._now.hour, 
                                          p_minute=self._now.min)

        self.messages.launch()
        self.messages.openThread(self.num)
        x = self.UTILS.getElements(DOM.Messages.message_timestamps, "Message timestamp headers", False)[-1]
        self.UTILS.TEST(p_str.lower() in x.text.lower(), 
                        "<b>Last message timestamp header contains <u>'%s'</u> </b>(it was <b>'%s'</b>)." % \
                        (p_str, x.text))

       
