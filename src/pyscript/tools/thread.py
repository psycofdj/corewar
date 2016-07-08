# -*- coding: utf-8
#-----------------------------------------------------------------------------#

import threading
import time

from pyscript.logger.object import LoggingObject

#-----------------------------------------------------------------------------#

class SafeThread(threading.Thread, LoggingObject):
    def __init__(self, p_loopInterval, p_threadName):
        threading.Thread.__init__(self)
        LoggingObject.__init__(self, p_threadName)
        self.m_terminated = False
        self.m_loopInterval = p_loopInterval

    def work(self):
        raise NotImplemented

    def run(self):
        self.m_terminated = False
        self.info("starting thread...")
        while not self.m_terminated:
            self.debug("starting loop...")
            self.work()
            self.debug("loop ended")
            if not self.m_terminated:
                self.debug("sleeping...")
                time.sleep(self.m_loopInterval)
        self.info("thread ended")

    def stop(self):
        self.info("stopping thread...")
        self.m_terminated = True

    def safe_join(self):
        self.info("joining thread...")
        while True:
            try:
                self.join(1)
                if not self.isAlive():
                    break
            except KeyboardInterrupt:
                self.warning("recieved keyboard interrupt, preaparing for exit")
                self.stop()
        self.info("thread joined")



#-----------------------------------------------------------------------------#
