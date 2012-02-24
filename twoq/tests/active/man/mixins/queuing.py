# -*- coding: utf-8 -*-
'''manual queuing test mixins'''


class MQMixin(object):

    ###########################################################################
    ## queue manipulation #####################################################
    ###########################################################################

    def test_delitem(self):
        q = self.qclass(1, 2, 3, 4, 5, 6)
        del q[2]
        self.assertEquals(q.outsync().value(), [1, 2, 4, 5, 6])

    def test_remove(self):
        self.assertEquals(
            self.qclass(1, 2, 3, 4, 5, 6).remove(5).outsync().value(),
            [1, 2, 3, 4, 6],
        )

    def test_insert(self):
        q = self.qclass(1, 2, 3, 4, 5, 6)
        q.insert(2, 10)
        self.assertEquals(q.outsync().value(), [1, 2, 10, 4, 5, 6])

    def test_extend(self):
        self.assertEquals(
            self.qclass().extend([1, 2, 3, 4, 5, 6]).outsync().value(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendleft(self):
        self.assertEquals(
            self.qclass().extendleft([1, 2, 3, 4, 5, 6]).outsync().value(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        self.assertEquals(
            self.qclass().append('foo').outsync().value(), 'foo'
        )

    def test_appendleft(self):
        self.assertEquals(
            self.qclass().appendleft('foo').outsync().value(), 'foo'
        )

    def test_inclear(self):
        self.assertEqual(len(self.qclass([1, 2, 5, 6]).inclear()), 0)

    def test_outclear(self):
        self.assertEqual(len(self.qclass([1, 2, 5, 6]).outclear().outgoing), 0)

    ###########################################################################
    ## queue balancing ########################################################
    ###########################################################################

    def test_insync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).outshift().inclear().shift()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_inshift(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).outshift().sync()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_outsync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).outshift()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_outshift(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).outsync()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def test_index(self):
        self.assertEquals(self.qclass(1, 2, 3, 4, 5, 6).index(3), 2)

    def test_results(self):
        self.assertEquals(
            list(self.qclass(1, 2, 3, 4, 5, 6).outsync().results()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_contains(self):
        self.assertTrue(5 in self.qclass(1, 2, 3, 4, 5, 6))
