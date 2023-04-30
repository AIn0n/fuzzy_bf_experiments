## move by pointer number to some place and go back
#
# useful to build some sort of memory allocator
# first address is stop number, 0 minus 1 value needed to stop us during comeback.
# second address (plus 2) is used as iterator
#

### BLOCK TO MOVE LEFT BY POINTER
-       # initialize stop sign
>>      # move to next
+++++   # number 5 its iterator
[
  [
    ->>+<<  # move number one address further
  ]
  # remove one to make it working till
  # iterator is different than zero 
  >>- 
]
### BLOCK TO COMEBACK RIGHT TILL STOP SIGN
+[-<<+]