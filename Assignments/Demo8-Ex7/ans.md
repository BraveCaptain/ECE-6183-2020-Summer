# how this affects the sound of the output?
The output will be recursive. It will become a feedback system

# With this change, what is the difference equation, transfer function, and impulse response of the system?
- difference equation: y(n) = x(n) + 0.8* y(n-800)
- transfer function: Y(z)/X(z) = 1 / (1 - 0.8 * z^(-800))
- impulse response: please refer to attached files im_res_con.jpg & im_res_dis.jpg

# What happens when the gain for the delayed value is greater than 1?
- For difference equation: y(n) = x(n) + 0.8* y(n-800), please refer to file output_matlab.wav
- For difference equation: y(n) = x(n) + 0.8* x(n-800), the output sound will increase