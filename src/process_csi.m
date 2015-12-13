#!/usr/bin/octave -qf

addpath('/home/adrian/csi/linux-80211n-csitool-supplementary/matlab');
graphics_toolkit gnuplot;

% Assume SignalType = 'voltage'
db = @(X) 10 * log10(abs(X).^2)

csi_trace = read_bf_file(argv(){1});
csi_entry = csi_trace{1};
csi = get_scaled_csi(csi_entry);
figure("visible", "off");
plot(db(abs(squeeze(csi).')), 'LineWidth', 4);
axis([0 30 5 30]);
legend('RX Antenna A', 'RX Antenna B', 'RX Antenna C', 'Location', 'SouthEast' );
xlabel('Subcarrier index');
ylabel('SNR [dB]');
print -r0 -dpng img/plot.png;
