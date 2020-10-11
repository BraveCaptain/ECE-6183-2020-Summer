%% wave_filter_matlab.m

%% Load wave file

[x, Fs] = audioread('author.wav');

N = length(x);
n = 1:N;
t = n/Fs;

a = zeros(1, 801);
a(1) = 1.0;
a(801) = -1.5;
b = zeros(1, 801);
b(1) = 1.0;


%% Frequency response

[H, om] = freqz(b, a);
f = om*Fs/(2*pi);
figure(1)
clf
plot(f, abs(H))
xlabel('Frequency (Hz)')
title('Frequency response')
zoom xon

%% Impulse response
% discrete-time plot

L = 150;
imp = [1 zeros(1, L)];
h = filter(b, a, imp);

figure(2)
clf
stem(0:L, h)
xlabel('Discrete time (n)')
title('Impulse response')

%% Impulse response
% continuous-time plot

figure(3)
clf
plot((0:L)/Fs, h)
xlabel('Time (sec)')
title('Impulse response')

%% Apply filter to speech signal

y = filter(b, a, x);   % implement difference equation

%% Write output signal to wave file

audiowrite('output_matlab.wav', y, Fs);

sound(y, Fs)
