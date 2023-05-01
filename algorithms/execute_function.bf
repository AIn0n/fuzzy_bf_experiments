### first block is always true
# next 3 blocks are function exec flag
# if founded they jump into code block which is another function
+     # always true 
>>+<< # second is function to jump
[
  > # start of function stack if first mem element
    # iterate as long as you found 1
  [] # first func
  >
  # second func
  [
    >> # I have to go two steps to be on stack
    +++++ > # put on stack five
    +++ # put on stack three
    # function exit turn off exec flag and turn next func
    <<< -
    > + < next function will be executed
  ] 
  >
  [
    >> # go to the end of the stack
    [-<->]
  ] # third func
]