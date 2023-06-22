import sys, re
from rbtree import RedBlackTree
from minheap import minHeap

# initialize Red Black Tree and Min Heap
r = RedBlackTree()
m = minHeap()

# get the filename from command line argument
fileName = sys.argv[1]

# open input and output files
with open(fileName, 'r') as file, open('output_file.txt', 'w') as openFile:

  # read each line in input file
  for line in file:
    
    # extract the arguments from the line
    args = re.findall('\((.*?)\)', line)

    # if the operation is an Insert
    if "Insert" in line:
      # extract the ride number, ride cost, and time duration from the arguments
      rn, rc, td = tuple(int(arg) if arg.isdigit() else arg for arg in args[0].split(','))
      output = f"({rn},{rc},{td})"
      
      # insert the ride into the Min Heap if it's the earliest ride
      if m.insert(rn, rc, td):
        print(m.insert(rn, rc, td)) # debug print statement
        openFile.write(m.insert(rn, rc, td))
        sys.exit(0)
      # insert the ride into the Red Black Tree if it's not the earliest ride
      elif r.insert(rn, rc, td):
        print(r.insert(rn, rc, td)) # debug print statement
        openFile.write(r.insert(rn, rc, td))
        sys.exit(0)

    # if the operation is a GetNextRide
    elif "GetNextRide" in line:
      # get the next ride from the Min Heap
      next_ride = m.GetNextRide()

      if next_ride:
        # if there is a ride, remove it from the Min Heap and print its details
        ride_id, ride_from, ride_to = next_ride
        r.delete(ride_id)
        ride_info = (ride_id, ride_from, ride_to)
        ride_str = f"({ride_id}, {ride_from}, {ride_to})"
        print(ride_str)
        openFile.write(f"{ride_str}\n")
      else:
        # if there are no active ride requests, print a message
        print("No active ride requests")
        openFile.write("No active ride requests\n")

    # if the operation is an UpdateTrip
    elif "UpdateTrip" in line:
      # extract the ride number and new time duration from the arguments
      rn_str, newtd_str = args[0].split(',')
      try:
        rn = int(rn_str)
      except ValueError:
        rn = rn_str
      try:
        newtd = int(newtd_str)
      except ValueError:
        newtd = newtd_str
      # update the ride in both the Min Heap and Red Black Tree
      m.update_trip(rn, newtd)
      r.UpdateTrip(rn, newtd)

    # if the operation is a CancelRide
    elif "CancelRide" in line:
      try:
        rn = int(args[0])
      except ValueError:
        # if the ride number is not a valid integer, print an error message
        print("Invalid ride number, please enter an integer")
        openFile.write("Invalid ride number, please enter an integer\n")
      # cancel the ride in both the Min Heap and Red Black Tree
      m._cancel_ride(rn)
      r.delete(rn)

    # if the operation is a Print
    elif "Print" in line:
      printargs_str = args[0].split(',')
      printargs = [int(arg) if arg.isdigit() else arg for arg in printargs_str]
      #  If there is only one argument, search the Red-Black Tree for a node with the corresponding ride number
      if len(printargs) == 1:
        node = r.search(printargs[0])
        if node == r.NIL:
          printargs = (0, 0, 0)
        else:
          printargs = (node.rn, node.rc, node.td)
      #   If there are two arguments, print all nodes in the Red-Black Tree with ride numbers between the two arguments
      else:
        nodes = r.Print(printargs[0], printargs[1])
        if len(nodes) == 0:
          printargs = (0, 0, 0)
        else:
          printargs = nodes
      print(printargs)
      openFile.write(str(printargs) + '\n')