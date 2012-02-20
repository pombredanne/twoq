# -*- coding: utf-8 -*-
'''active twoq'''

from bisect import bisect_right
from collections import deque,  Iterable

from stuf.six import string_types

from twoq.core import coreq

__all__ = ['twoq']


def iterexcept(func, exception, first=None):
    '''
    call a function repeatedly until an exception is raised

    Converts a call-until-exception interface to an iterator interface.
    Like __builtin__.iter(func, sentinel) but uses an exception instead
    of a sentinel to end the loop.
    '''
    try:
        if first is not None:
            yield first()
        while 1:
            yield func()
    except exception:
        pass


class SyncContext(object):

    '''sync context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(SyncContext, self).__init__()
        self._outextend = queue._outextend
        self._inextend = queue._inextend
        self._outappend = queue._outappend
        self._inclear = queue._inclear
        self._outclear = queue._outclear
        self._outgoing = queue.outgoing

    def __enter__(self):
        self._outclear()
        return self

    def __exit__(self, t, v, e):
        # clear incoming items
        self._inclear()
        # extend incoming items with outgoing items
        self._inextend(self._outgoing)

    def __call__(self, args):
        self._outextend(args)

    def iter(self, args):
        self._outextend(iter(args))

    def append(self, args):
        self._outappend(args)


class baseq(coreq):

    '''base active queue'''

    def __init__(self, incoming, outgoing):
        '''
        init

        @param incoming: incoming queue
        @param outgoing: outgoing queue
        '''
        super(baseq, self).__init__(incoming, outgoing)
        #######################################################################
        ## incoming things ####################################################
        #######################################################################
        # incoming things right append
        self._inappend = self.incoming.append
        # incoming things left append
        self._inappendleft = self.incoming.appendleft
        # incoming things incomng clear
        self._inclear = self.incoming.clear
        # incoming things right extend
        self._inextend = self.incoming.extend
        # incoming things left extend
        self._inextendleft = self.incoming.extendleft
        #######################################################################
        ## outgoing things ####################################################
        #######################################################################
        # outgoing things right append
        self._outappend = self.outgoing.append
        # outgoing things right extend
        self._outextend = self.outgoing.extend
        self._outclear = self.outgoing.clear
        # outgoing things right pop
        self.pop = self.outgoing.pop
        # outgoing things left pop
        self.popleft = self.outgoing.popleft

    def __delitem__(self, index):
        incoming = self.incoming
        incoming.rotate(-index)
        incoming.popleft()
        incoming.rotate(index)

    def __contains__(self, value):
        return value in self.incoming

    def __len__(self):
        return len(self.incoming)

    @property
    def sync(self):
        '''sync incoming things with outgoing things'''
        return SyncContext(self)

    def clear(self):
        '''clear all queues'''
        self.call = None
        self._outclear()
        self._inclear()
        return self

    def append(self, thing):
        '''incoming things right append'''
        self._inappend(thing)
        return self

    def appendleft(self, thing):
        '''incoming things left append'''
        self._inappendleft(thing)
        return self

    def inclear(self):
        '''incoming things clear'''
        self._inclear()
        return self

    def outclear(self):
        '''incoming things clear'''
        self._inclear()
        return self

    def extend(self, things):
        '''incoming things right extend'''
        self._inextend(things)
        return self

    def extendleft(self, things):
        '''incoming things left extend'''
        self._inextendleft(things)
        return self

    def remove(self, thing):
        '''
        remove thing from incoming things

        @param thing: some thing
        '''
        incoming = self.incoming
        position = bisect_right(incoming, thing) - 1
        incoming.rotate(-position)
        incoming.popleft()
        incoming.rotate(position)
        return self

    def insert(self, index, value):
        '''
        insert thing into incoming things

        @param index: index position
        @param thing: some thing
        '''
        incoming = self.incoming
        incoming.rotate(-index)
        incoming.popleft()
        incoming.appendleft(value)
        incoming.rotate(index)
        return self

    def shift(self):
        '''sync incoming things with outgoing things'''
        # clear incoming items
        self._inclear()
        # extend incoming items with outgoing items
        self._inextend(self.outgoing)
        return self

    def index(self, thing):
        '''
        insert thing into incoming things

        @param thing: some thing
        '''
        return bisect_right(self.outgoing, thing) - 1

    def results(self):
        '''iterate over outgoing things, clearing as it goes'''
        for thing in iterexcept(self._outpop, IndexError):
            yield thing

    def reversed(self):
        '''iterate over reversed outgoing things, clearing as it goes'''
        for thing in iterexcept(self._outpopleft, IndexError):
            yield thing


class twoq(baseq):

    '''processing queue'''

    def __init__(self, *args):
        '''init'''
        incoming = deque()
        # extend if just one argument
        if len(args) == 1:
            args = args[0]
            if all([
                isinstance(args, Iterable), not isinstance(args, string_types)
            ]):
                incoming.extend(args)
            else:
                incoming.append(args)
        else:
            incoming.extend(args)
        super(twoq, self).__init__(incoming, deque())
