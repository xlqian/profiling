# -*- coding: utf-8 -*-
"""
    profiling.remote.background
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Utilities to run a profiler in a background thread.

"""
from __future__ import absolute_import
import os
import signal
import threading

from ..profiler import ProfilerWrapper


__all__ = ['SIGNUM', 'BackgroundProfiler']


SIGNUM = signal.SIGUSR2


class BackgroundProfiler(ProfilerWrapper):

    def __init__(self, profiler, signum=SIGNUM):
        super(BackgroundProfiler, self).__init__(profiler)
        self.signum = signum
        self.event = threading.Event()

    def prepare(self):
        """Registers :meth:`_signal_handler` as a signal handler to start
        and/or stop the profiler from the background thread.  So this function
        must be called at the main thread.
        """
        return signal.signal(self.signum, self._signal_handler)

    def run(self):
        self._send_signal()
        yield
        self._send_signal()

    def _send_signal(self):
        self.event.clear()
        os.kill(os.getpid(), self.signum)
        self.event.wait()

    def _signal_handler(self, signum, frame):
        if self.profiler.is_running():
            self.profiler.stop()
        else:
            self.profiler.start()
        self.event.set()
