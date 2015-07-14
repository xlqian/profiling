# -*- coding: utf-8 -*-
"""
    profiling.util
    ~~~~~~~~~~~~~~
"""
from __future__ import absolute_import
from collections import deque

try:
    from . import speedup
except ImportError:
    speedup = False


__all__ = ['frame_stack']


if speedup:
    def frame_stack(frame, top_frame=None, top_code=None):
        """Returns a deque of frame stack."""
        return speedup.frame_stack(frame, top_frame, top_code)
else:
    def frame_stack(frame, top_frame=None, top_code=None):
        """Returns a deque of frame stack."""
        frames = deque()
        while frame is not None:
            frames.appendleft(frame)
            if frame is top_frame or frame.f_code is top_code:
                break
            frame = frame.f_back
        return frames
