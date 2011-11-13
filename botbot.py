#!/usr/bin/python

import sys

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
        """ ??? """
        return None
    
    

def main(argv):

    logfile = open('csbot_logfile.txt', 'w')
    the_bot = Bot()
    
    while True:
        next = sys.stdin.readline()
        if not next:
            break        
        data = next.strip()
        
        logfile.write(data + '\n')

        data = data.split()
        if len(data) == 2:
            value = int(data[1])
            if data[0] == 'RUNDEN':
                the_bot.set_n_rounds(value)
            elif data[0] == 'RUNDE':
                the_bot.set_cur_round(value)
            elif data[0] == 'ANGEBOT':
                reply = the_bot.process_offer(value)
                """ Reaction: Send  JA or NEIN """
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
