# !/usr/bin/python3
import argparse
import random
import sys

def main():
  parser = argparse.ArgumentParser(prog='SHUF',\
                                  usage='shuf [OPTION]... [FILE]\n  or:  shuf -e [OPTION]... [ARG]...\n  or:  shuf -i LO-HI [OPTION]...',\
                                  description='Write a random permutation of the input lines to standard output.',\
                                  epilog='Made by Soyeon Kim. UCLA 2024 Winter CS35L by Eggert')
  parser.add_argument('-e', '--echo', metavar='', nargs='*', \
                      help='treat each arg as an input line')
  parser.add_argument('-i', '--input-range', metavar='LO-HI', type=str, \
                      help='treat each number LO through HI as an input line')
  parser.add_argument('-n', '--head-count', metavar='COUNT', type=int, \
                      help='output at most COUNT lines')
  parser.add_argument('-r', '--repeat', action='store_true', \
                      help='each output line is randomly chosen from all the inputs')

  args, extra_args = parser.parse_known_args()

  # print(args, ', ', extra_args)
  count = -1 # store head-count number
  lines = [] # store values to print
  extra_arg_len = len(extra_args)

  try:
    if (args.echo is not None and args.input_range):
      raise SyntaxError("cannot combine -e and -i options")
    if (extra_args and args.input_range):
      raise SyntaxError(f"extra operand: '{extra_args[0]}'")

    # -e(echo) option
    if (args.echo is not None): # args.echo can be an empty list
      lines = args.echo
      if (extra_arg_len > 0): # -e treats everything but the option (and their values) as the input line
        lines += extra_args

    # -i(input-range) option
    elif (args.input_range):
      try:
        low, high = args.input_range.split('-')
        lo, hi = int(low), int(high)

        if (lo > hi): raise ValueError

        lines = list(range(lo, hi+1))

      except: raise ValueError(f"invalid input range: '{args.input_range}'")

    # check extra_args
    else:
      if (extra_arg_len == 0) or (extra_arg_len == 1 and extra_args[0] == '-'): # no input
        inputs = sys.stdin.readlines()
        sys.stdin.close()
        lines = [line.strip() for line in inputs]

      elif (extra_arg_len == 1): # argument input
        input_arg = extra_args[0]

        if (input_arg.startswith('-')): # no need to consider combined opt like -er
          raise SyntaxError(f"invalid option '{input_arg}'")

        with open(input_arg, 'r') as file:
          lines = [line.strip() for line in file]

      elif (extra_arg_len == 2 and extra_args[0] == '-'): # '-' input
        with open(extra_args[1], 'r') as file:
          lines = [line.strip() for line in file]
          
      else:
        raise SyntaxError(f"extra operand: '{extra_args[1] if extra_args[0] != '-' else extra_args[2]}'")


    # -n(head-count) option: store head_count value to count
    if (args.head_count):
      count = args.head_count
      if (count < 0): parser.error(f"invalid line count: '{count}'")

    # -r(repeat) option
    if (args.repeat):
      if (not lines): parser.error("no lines to repeat")

      while (not args.head_count or count > 0):
        print(lines[random.randrange(len(lines))])
        count -= 1
    else:
      random.shuffle(lines)
      repeat = min(count, len(lines)) if count != -1 else len(lines)
      for i in range(repeat):
        print(lines[i])

  except FileNotFoundError as err:
    parser.error(f"{err.args[1]}: '{extra_args[0] if extra_args[0] != '-' else extra_args[1]}'")
  except KeyboardInterrupt:
    parser.error("Keyboard interrupt")
  except Exception as err: # catch all
    parser.error(err)

if __name__ == "__main__":
    main()
