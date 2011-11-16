#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import random
from math import sqrt


DEFAULT_OFFER = 500
REPLY_POSITIVE = 'JA'
REPLY_NEGATIVE = 'NEIN'

class Bot:
    def __init__(self):
        self.n_rounds = 0
        self.cur_round = 0
        self.offers = []
        self.my_offers = []
        self.points = []
        self.points_added = 0

        self.logfile = open('bot_logfile.txt', 'w')
        self.logfile.write("--- %s\n" % self.__class__.__name__)

        return None

    def set_n_rounds(self, n):
        self.n_rounds = n
        return None
    
    def set_cur_round(self, r):
        self.cur_round = r
        return None

    def process_offer(self, offer):
        """ Evaluate offer and send reply """
        reply = REPLY_POSITIVE
        self.offers.append((offer, reply))
        return reply

    def make_offer(self):
        """ Make an offer (that cannot be refused) """
        self.last_offer = DEFAULT_OFFER
        return '%s' % self.last_offer

    def process_reply(self, reply):
        """ Evaluate reply to latest offer """
        self.my_offers.append((self.last_offer, reply))
        return None

    def receive_points(self, points):
        self.points.append(points)
        self.points_added += points
        return None
    
    def postprocess(self):
        """ !!! """
        
      

        
        self.logfile.close()
        return None
    




class cjtbot0(Bot):
    """
    uses static optimum and never defects
    """ 
    def make_offer(self):
        """ find optimal value """
        offer = 300
        self.last_offer = offer
        return '%s' % self.last_offer  






class cjtbot1(Bot):
    """
    tries to find the minimum, yielding in avg the max payoff
    """ 
    
    def __init__(self):
        Bot.__init__(self)

        self.std = 300
        self.var = 100
        return None



    def make_offer(self):
        """ find optimal value """

        MAX_BRAIN=100
        MIN_BRAIN=25
        SWITCH_BEHAV=47
        DEFAULT_OFFER=300
        
        if self.n_rounds<=SWITCH_BEHAV:
            #too short game for goods statistics
            offer = DEFAULT_OFFER
        elif self.cur_round<SWITCH_BEHAV:
            #start with some test balloons without attracting attention 
            
            #TODO: using gaussians?
            offer = random.randint(0, 19)*25 #in 25 schritten von 0 bis 475
                

        else:
            self.logfile.write("------------------------------\n")
            self.logfile.write(": %s\t" % self.cur_round)
            
            #precalc based on dynamic history aka "brain"
            length=max(min(len(self.my_offers), int(self.var), MAX_BRAIN), MIN_BRAIN) #if var=0 or too large, limit length to [MIN_BRAIN,MAX_BRAIN] entries
            brain=self.my_offers[-length:]
             
            #mittelwert und var holen
            (self.std, self.var)=statistics([x[0] for x in brain])
            self.logfile.write("=== brain: %s # µ=%s o=%s ===\n" % (len(brain), self.std, self.var))



            #
            offer=300
            self.logfile.write(": %s\n" % offer)


            
        self.last_offer = offer
        return '%s' % self.last_offer        





    def process_offer(self, offer):
        reply = REPLY_POSITIVE
        self.offers.append((offer, reply))
        return reply










def statistics(vallist):
    if len(vallist)==0:
        return (0,0)
    s2 = 0
    s = 0
    N=len(vallist)
    for e in vallist:
        s += e
        s2 += e * e
    return (s/N, sqrt((s2-(s*s)/N) /N))





def main(argv):

    logfile = open('csbot_logfile.txt', 'w')
    #~ the_bot = Bot()
    the_bot = cjtbot1()
    
    while True:
        next = sys.stdin.readline()
        if not next:
            break
        data = next.strip()
        
        logfile.write(": "+ data + '\n')

        data = data.split()
        if len(data) == 2:
            value = int(data[1])
            if data[0] == 'RUNDEN':
                the_bot.set_n_rounds(value)
            elif data[0] == 'RUNDE':
                the_bot.set_cur_round(value)
            elif data[0] == 'ANGEBOT':
                reply = the_bot.process_offer(value)
                """ Reaction: Send JA or NEIN """
                sys.stdout.write('%s\n' % reply)
                sys.stdout.flush()
            elif data[0] == 'PUNKTE':
                the_bot.receive_points(value)
        elif len(data) == 1:
            if data[0] == 'START':
                """ Reaction: Send offer \in [0,1000] """
                offer = the_bot.make_offer()
                sys.stdout.write('%s\n' % offer)
                sys.stdout.flush()
                pass
            elif data[0] == 'ENDE':
                """ Reaction: Postprocessing and shut down """
                the_bot.postprocess()
                break
            elif data[0] == 'JA' or data[0] == 'NEIN':
                """ Reaction: Process reply (optionally) """
                """ Can only occur after replying to a START cmd """
                the_bot.process_reply(data[0])
                pass
            else:
                pass
        else:
            pass
                

    # print 'DONE'
    logfile.close()

    return None


if __name__ == '__main__': main(sys.argv[1:])

