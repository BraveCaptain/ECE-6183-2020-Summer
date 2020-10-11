# Describe how you would go about implementing the total system H(z) in real-time with block processing so that the initial states are correctly set so that no error artifacts arise.

Since the function is H(z) = H1(z)H2(z), I need to first calculate each block of H1 , after each block, use it to calculate H2. Just as before, we will need 2 states z1 and z2. We update z1 after calcualting each block of H1. After this is done, we use the output block and state z2 to calculate H2. We update each state after rach block of calculation.

# Do any problems arise? What kinds of issues do you need to be aware of?

Since there are two subsystems, we need to make sure each block of output is continious. So one state is not enough, two states are needed.
