import textwrap
import urllib3
import sys
import argparse
import platform
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_if_up(response, sub, name):
   try:
      if(response == 0):
       f = open("{0}.txt".format(name), 'a')
       if response == 0:
        print("{0} is up".format(sub))
        f.write("{0} is up \n".format(sub))
        f.close()
      else:
        print("{0} is down".format(sub))


   except KeyboardInterrupt:
    print("Keyboard interrupt exception Caught")


def pingoriginal(sub, name):
   try:
    if (platform.system().lower() == 'windows'):
        response = os.system("ping " + sub)

    else:
        response = os.system("ping " + sub)

    check_if_up(response, sub, name)

   except KeyboardInterrupt:
    print("Keyboard interrupt exception Caught")


def controlling_the_number_of_packets(sub, num, name):
   try:
      if (platform.system().lower() == 'windows'):
        response = os.system("ping -n " + num +" "+ sub)

      else:
       response = os.system("ping -c " + num +" "+ sub)

      check_if_up(response, sub, name)
   except KeyboardInterrupt:
      print("Keyboard interrupt exception Caught")


def controlling_the_size_of_packet(sub, num, num1, name):
    try:
       if (platform.system().lower() == 'windows'):
        response = os.system("ping -s " + num + " -n " + num1 +" "+ sub)
       else:
        response = os.system("ping -s " + num + " -c " + num1 +" "+ sub)

       check_if_up(response, sub, name)

    except KeyboardInterrupt:
      print("Keyboard interrupt exception Caught")


def changing_the_time_interval(sub, num, num1, name):
  try:
    if (platform.system().lower() == 'windows'):
        response = os.system("ping -i " + num +" -n "+num1+" "+ sub)
    else:
        response = os.system("ping -i " + num +" -c "+num1+" "+ sub)

    check_if_up(response, sub, name)
  except KeyboardInterrupt:
      print("Keyboard interrupt exception Caught")


def summary(sub, num, name):
   try:
    if (platform.system().lower() == 'windows'):
        response = os.system("ping -n " + num + " -q " + sub)

    else:
        response = os.system("ping -c " + num + " -q " + sub)

    check_if_up(response, sub, name)

   except KeyboardInterrupt:
      print("Keyboard interrupt exception Caught")
      

def timeout(sub, num, name):
   try:
    response = os.system("ping -t " + num +" "+ sub)
    check_if_up(response, sub, name)

   except KeyboardInterrupt:
      print("Keyboard interrupt exception Caught")


def flooding(sub, name):
   try:
    response = os.system("ping -f " + sub)
    check_if_up(response, sub, name)
   except KeyboardInterrupt:
      print("Keyboard interrupt exception Caught")


def timestamp(sub, typeoftimestamp, num, name):
   try:
      if (platform.system().lower() == "windows"):
         if (typeoftimestamp == 'tsonly'):
            response = os.system("ping -t tsonly " + "-n " + num +" "+ sub)
         else:
            response = os.system("ping -t tsandaddr " + "-n " + num +" "+ sub)

      else:
        if (typeoftimestamp == 'tsonly'):
            response = os.system("ping -t tsonly " + "-c " + num +" "+ sub)
        else:
            response = os.system("ping -t tsandaddr " + "-c " + num +" "+ sub)
        check_if_up(response, sub, name)

   except KeyboardInterrupt:
      print("Keyboard interrupt exception Caught")



def time_to_wait_for_response(sub, num, num1, name):
   try:
    if (platform.system().lower() == 'windows'):
        response = os.system("ping -n " + num + " -W " + num1 +" "+ sub)


    else:
        response = os.system("ping -c " + num + " -W " + num1 +" "+ sub)

    check_if_up(response, sub, name)
   except KeyboardInterrupt:
      print("Keyboard interrupt exception Caught")



def fill_packet_with_data(sub, num, fill, name):
   try:
    if (platform.system().lower() == 'windows'):
        response = os.system("ping -n " + num + " -p " + fill +" "+ sub)

    else:
        response = os.system("ping -c " + num + " -p " + fill +" "+ sub)

    check_if_up(response, sub, name)
   except KeyboardInterrupt:
      print("Keyboard interrupt exception Caught")



def specify_TTL(sub, num, num1, name):
   try:
      if (platform.system().lower() == 'windows'):
        response = os.system("ping -n " + num + " -t " + num1 +" "+ sub)

      else:
        response = os.system("ping -c " + num + " -t " + num1 +" "+ sub)

        check_if_up(response, sub, name)
   except KeyboardInterrupt:
       print("Keyboard interrupt exception Caught")
      


if '__main__' == __name__:
    parser = argparse.ArgumentParser(prog="Domain Life", formatter_class=argparse.RawDescriptionHelpFormatter, usage="python3 domainlife.py optionnumber" , description=textwrap.dedent('''
                                           DOMAIN LIFE
                    Domain life helps you to ping a subdomain or a domain in different ways...choose a number to get started
                        1  We can send light and heavy packet
                        2  By default ping wait for 1 sec to send next packet we can change this time
                        3  To only get the summary about the network
                        4  To stop pinging after sometime
                        5  To send packets as soon as possible. This is used to test network performance
                        6  It is current time of event recorded by a machine over a network. It works by using TS option of IP packet.
                           We have three option with it - tsonly (timestamp only), tsandaddr (timestamp and address)
                        7  Sets time to wait for a response
                        8  We can fill data in packet using this option. Like ff will fill packet with ones
                        9  It is maximum hop a packet can travel before getting discarded.A value 0 will restricts packet to same host
                        10 Exit
                        11 Original ping
                        '''))
    parser.add_argument('optionnumber',metavar='N', action='store',type=int, default=10, help='Type a number from 1 to 11 to specify the type of ping you want to perform and 10 is to exit')
    parser.add_argument('--file', action='store',type=argparse.FileType('r'), help='Enter the file that contains the list of subdomains to be pinged')
    parser.add_argument('--site', action='store',type=str, help='Enter the domain or subdomain to be pinged')
    args = parser.parse_args()
    parser.print_help()



    match args.optionnumber:
        case 1:
          try:
             num = input("Enter the size of packets to send: ")
             num1 = input("Enter the number of packets to send: ")
             name = input("Enter the name of text file to save output: ")
             if (args.site == None):
                data = args.file.readlines()
                for line in data:
                   sub = line.rstrip()
                   controlling_the_size_of_packet(sub, num, num1, name)
             else:
                sub = args.site
                controlling_the_size_of_packet(sub, num, num1, name)
          except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")

        case 2:
           try:
            num = input("Enter the time interval after which packets are sent: ")
            num1 = input("Enter the number of packets to send: ")
            name = input("Enter the name of text file to save output: ")
            if (args.site == None):
               data = args.file.readlines()
               for line in data:
                   sub = line.rstrip()
                   changing_the_time_interval(sub, num, num1, name)
            else:
               sub = args.site
               changing_the_time_interval(sub, num, num1, name)
           except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")

        case 3:
           try:
            num = input("Enter the number of packets to send: ")
            name = input("Enter the name of text file to save output: ")
            if (args.site == None):
               data = args.file.readlines()
               for line in data:
                   sub = line.rstrip()
                   summary(sub, num, name)
            else:
               sub = args.site
               summary(sub, num, name)
           except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")

        case 4:
           try:
             num = input("Enter the time for timeout: ")
             name = input("Enter the name of text file to save output: ")

             if (args.site == None):
                data = args.file.readlines()
                for line in data:
                   sub = line.rstrip()
                   timeout(sub, num, name)
             else:
               sub = args.site
               timeout(sub, num, name)

           except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")

        case 5:
          try:
           name = input("Enter the name of text file to save output: ")
           if (args.site == None):
            data = args.file.readlines()
            for line in data:
                sub = line.rstrip()
                flooding(sub, name)
           else:
            sub = args.site
            flooding(sub, name)
          except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")


        case 6:
           try:
            typeoftimestamp = input("Enter the type of timestamp tsonly or tsandaddr: ")
            num = input("Enter the number of packets to send: ")
            name = input("Enter the name of text file to save output: ")
            if (args.site == None):
             data = args.file.readlines()
             for line in data:
                   sub = line.rstrip()
                   timestamp(sub, typeoftimestamp, num, name)

            else:
             sub = args.site
             timestamp(sub, typeoftimestamp, num, name)
           except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")


        case 7:
           try:
            num= input("Enter the number of packets to send: ")
            num1= input("Enter the time to wait: ")
            name = input("Enter the name of text file to save output: ")
            if (args.site == None):
              data = args.file.readlines()
              for line in data:
                   sub = line.rstrip()
                   time_to_wait_for_response(sub, num, num1, name)
            else:
             sub = args.site
             time_to_wait_for_response(sub, num, num1, name)
           except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")


        case 8:
           try:
            num = input("Enter the number of packets to send: ")
            fill = input("Enter the binary number to fill packets: ")
            name = input("Enter the name of text file to save output: ")
            if (args.site == None):
             data = args.file.readlines()
             for line in data:
                   sub = line.rstrip()
                   fill_packet_with_data(sub, num, fill, name)
            else:
             sub = args.site
             fill_packet_with_data(sub, num, fill, name)
           except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")


        case 9:
           try:
            num= input("Enter the number of packets to send: ")
            num1= input("Enter the time to live: ")
            name = input("Enter the name of text file to save output: ")
            if (args.site == None):
             data = args.file.readlines()
             for line in data:
                   sub = line.rstrip()
                   specify_TTL(sub, num, num1, name)
            else:
             sub = args.site
             specify_TTL(sub, num, num1, name)
           except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")


        case 10:
           try:
            num = input("Enter the number of packets: ")
            name = input("Enter the name of text file to save output: ")
            if (args.site == None):
             data = args.file.readlines()
             for line in data:
                sub = line.rstrip()
                controlling_the_number_of_packets(sub, num, name)
            else:
             sub = args.site
             controlling_the_number_of_packets(sub, num, name)
           except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")


        case 11:
            sys.exit(0)


        case default:
           try:
            name = input("Enter the name of text file to save output: ")
            if (args.site == None):
             data = args.file.readlines()
             for line in data:
                sub = line.rstrip()
                pingoriginal(sub, name)
            else:
             sub = args.site
             pingoriginal(sub, name)
           except KeyboardInterrupt:
            print("Keyboard interrupt exception Caught")






