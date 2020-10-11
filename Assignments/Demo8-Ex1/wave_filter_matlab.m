%% wave_filter_matlab.m

%% Load wave file

[x, Fs] = audioread('author.wav');

N = length(x);
n = 1:N;
t = n/Fs;

a = zeros(1, 801);
a(1) = 1.0;
b = zeros(1, 801);
b(1) = 1.0;
b(801) = 0.8;

%% Pole-zero diagram

figure(1)
clf
zplane(b, a)
title('Pole-zero diagram')

%% Frequency response

[H, om] = freqz(b, a);
f = om*Fs/(2*pi);
figure(2)
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

figure(3)
clf
stem(0:L, h)
xlabel('Discrete time (n)')
title('Impulse response')

%% Impulse response
% continuous-time plot

figure(4)
clf
plot((0:L)/Fs, h)
xlabel('Time (sec)')
title('Impulse response')

%% Transfer function


%% Apply filter to speech signal

y = filter(b, a, x);   % implement difference equation

%% Write output signal to wave file

audiowrite('output_matlab.wav', y, Fs);

sound(y, Fs)
