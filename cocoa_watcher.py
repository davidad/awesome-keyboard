from Foundation import NSObject, NSLog
from Cocoa import NSEvent, NSKeyDownMask
from AppKit import NSApplication, NSApp
from PyObjCTools import AppHelper, KeyValueCoding
import sys
 
class KeyboardWatcher:
  def __init__(self,name,queue):
      self._queue = queue
      self._name = name

  def handler(self,event):
      try:
          self._queue.put([self._name,KeyValueCoding.getKey(event,"keyCode")])
      except KeyboardInterrupt:
          AppHelper.stopEventLoop()
   
  class AppDelegate(NSObject):
      def applicationDidFinishLaunching_(self, notification):
          mask = NSKeyDownMask
          NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, self.handler)
   
  def run(self):
      app = NSApplication.sharedApplication()
      delegate = self.AppDelegate.alloc().init()
      delegate.handler = self.handler
      NSApp().setDelegate_(delegate)
      AppHelper.runEventLoop(installInterrupt=True)
