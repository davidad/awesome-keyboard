from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

from collections import defaultdict
import math

class KeyboardWatcher(Process):

    def __init__(self,name,queue):
        self._name = name
        self._queue = queue
        self._display = Display()

    def handle_event(self,reply):
        """ This function is called when a xlib event is fired """
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self._display.display, None, None)
            if event.type == X.KeyPress and event.sequence_number == 0:
                key = event.detail
                self._queue.put([self._name,key])

    def run(self):
        root = self._display.screen().root
        ctx = self._display.record_create_context(
                    0,
                    [record.AllClients],
                    [{
                            'core_requests': (0, 0),
                            'core_replies': (0, 0),
                            'ext_requests': (0, 0, 0, 0),
                            'ext_replies': (0, 0, 0, 0),
                            'delivered_events': (0, 0),
                            'device_events': (X.KeyReleaseMask),
                            'errors': (0, 0),
                            'client_started': False,
                            'client_died': False,
                    }])

        self._display.record_enable_context(ctx, self.handle_event)
