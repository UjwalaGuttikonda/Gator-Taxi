class minHeap:
    def __init__(self) -> None:
        self.size = 0
        self.heap = []  # initialize empty heap

    def insert(self, rn, rc, td):
        """
        Inserts a new trip into the heap.

        Args:
            rn: Ride Number
            rc: Ride Cost
            td: Trip Duration
        Returns:
            None if the insertion is successful, else returns error message.
        """
        err = "Duplicate RideNumber"
        ind = self._get_index(rn)
        if ind != -1:  # check if ride number already exists
            return err
        self.heap.append([rn, rc, td])  # append new trip to the heap
        i = len(self.heap) - 1
        self.upHeapify(i)  # heapify from bottom up
        return None

    def _get_index(self, rn):
        """
        Returns the index of a given ride number.

        Args:
            rn: Ride Number
        Returns:
            Index of the ride number if found, else returns -1.
        """
        for ind, trip in enumerate(self.heap):
            if rn == trip[0]:
                return ind
        return -1

    def update_trip(self, rn, newtd):
        """
        Updates the trip duration of a given ride number.

        Args:
            rn: Ride Number
            newtd: New Trip Duration
        """
        ind = self._get_index(rn)
        if newtd <= self.heap[ind][2]:
            # if new duration is less than or equal to the old duration, update duration and heapify
            self.heap[ind][2] = newtd
            self.upHeapify(ind)
            newind = self._get_index(rn)
            self.downHeapify(newind)
        elif self.heap[ind][2] < newtd <= 2 * self.heap[ind][2]:
            # if new duration is between old duration and twice the old duration, update cost and duration, then heapify
            temprn, temprc, _ = self.heap[ind]
            self.heap[ind][1] += 10
            self.heap[ind][2] = newtd
            self.upHeapify(ind)
            newind = self._get_index(rn)
            self.downHeapify(newind)
        elif newtd > 2 * self.heap[ind][2]:
            # if new duration is more than twice the old duration, cancel the ride
            self._cancel_ride(rn)

    def _cancel_ride(self, rn):
        """
        Cancels the ride with the given ride number.

        Args:
            rn: Ride Number
        """
        ind = self._get_index(rn)
        if ind != -1:
            if ind == len(self.heap) - 1:
                self.heap.pop()
            else:
                self.heap[ind] = self.heap.pop()
                self.downHeapify(ind)
  # function to heapify the element at position i
    def upHeapify(self, i):
      # check if i is greater than 0 and the parent element's distance and time are greater than the current element's distance and time
      if i > 0 and (self.heap[i][1] < self.heap[(i - 1) // 2][1] or
                    (self.heap[i][1] == self.heap[(i - 1) // 2][1]
                    and self.heap[i][2] < self.heap[(i - 1) // 2][2])):
        # swap the elements at positions i and (i-1)/2
        self.heap[i], self.heap[(i - 1) // 2] = self.heap[(i - 1) // 2], self.heap[i]
        # recursively call upHeapify on the parent of the current element
        self.upHeapify((i - 1) // 2)

  # function to get the next ride with minimum distance and time
    def GetNextRide(self):
      # if the heap is empty, return None
      if not self.heap:
        return None
      # if there is only one element in the heap, pop and return it
      if len(self.heap) == 1:
        ans = self.heap.pop()
      # if there are multiple elements in the heap
      else:
        # set ans to the root of the heap
        ans = self.heap[0]
        # replace the root with the last element in the heap
        self.heap[0] = self.heap.pop()
        # recursively call downHeapify on the root
        self.downHeapify(0)
      # return the minimum element
      return ans

  # function to heapify the element at position i
    def downHeapify(self, i):
    # calculate the left and right children of the element at position i
      l = 2 * i + 1
      r = 2 * i + 2
      # set the largest element to i
      largest = i
      # if the left child's distance and time are less than the largest element's distance and time
      if l < len(self.heap) and ((self.heap[l][1] < self.heap[largest][1]) or
                                (self.heap[l][1] == self.heap[largest][1]
                                  and self.heap[l][2] < self.heap[largest][2])):
        # set the largest element to the left child
        largest = l
      # if the right child's distance and time are less than the largest element's distance and time
      if r < len(self.heap) and ((self.heap[r][1] < self.heap[largest][1]) or
                                (self.heap[r][1] == self.heap[largest][1]
                                  and self.heap[r][2] < self.heap[largest][2])):
        # set the largest element to the right child
        largest = r
      # if the largest element is not i
      if largest != i:
        # swap the elements at positions i and largest
        self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
        # recursively call downHeapify on the largest element
        self.downHeapify(largest)
      return
