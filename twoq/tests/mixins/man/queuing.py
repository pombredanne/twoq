# -*- coding: utf-8 -*-
'''manual call chain queuing test mixins'''


class MQMixin(object):

    ###########################################################################
    ## queue manipulation #####################################################
    ###########################################################################

    def test_delitem(self):
        q = self.qclass(1, 2, 3, 4, 5, 6)
        del q[2]
        self.assertEqual(q.outsync().end(), [1, 2, 4, 5, 6])

    def test_remove(self):
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).remove(5).outsync().end(),
            [1, 2, 3, 4, 6],
        )

    def test_insert(self):
        q = self.qclass(1, 2, 3, 4, 5, 6)
        q.insert(2, 10)
        self.assertEqual(q.outsync().end(), [1, 2, 10, 3, 4, 5, 6])

    def test_extend(self):
        self.assertEqual(
            self.qclass().extend([1, 2, 3, 4, 5, 6]).outsync().end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendleft(self):
        self.assertEqual(
            self.qclass().extendleft([1, 2, 3, 4, 5, 6]).outsync().end(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        self.assertEqual(
            self.qclass().append('foo').outsync().end(), 'foo'
        )

    def test_appendleft(self):
        self.assertEqual(
            self.qclass().appendleft('foo').outsync().end(), 'foo'
        )

    def test_inclear(self):
        self.assertEqual(len(list(self.qclass([1, 2, 5, 6]).inclear())), 0)

    def test_outclear(self):
        self.assertEqual(
            len(list(self.qclass([1, 2, 5, 6]).outclear().outgoing)), 0
        )

    ###########################################################################
    ## queue balancing ########################################################
    ###########################################################################

    def test_insync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).outshift().inclear().shift()
        self.assertEqual(list(q.incoming), list(q.outgoing))

    def test_inshift(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).outshift().sync()
        self.assertEqual(list(q.incoming), list(q.outgoing))

    def test_outsync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).outshift()
        self.assertEqual(list(q.incoming), list(q.outgoing))

    def test_outshift(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).outsync()
        self.assertEqual(list(q.incoming), list(q.outgoing))

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def test_index(self):
        self.assertEqual(self.qclass(1, 2, 3, 4, 5, 6).index(3), 2)

    def test_results(self):
        self.assertEqual(
            list(self.qclass(1, 2, 3, 4, 5, 6).outsync().results()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_contains(self):
        self.assertTrue(5 in self.qclass(1, 2, 3, 4, 5, 6))
