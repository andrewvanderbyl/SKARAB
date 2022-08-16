import numpy as np
import matplotlib.pyplot as plt
from IPython import embed


def _compute_sfdr(db_total):
    ignore_zone = 3 
    peak = np.max(db_total)
    peak_channel = np.argmax(db_total)

    # Compute next dominant spike(tone).
    next_peak_value = max(np.max(db_total[:peak_channel-ignore_zone]), np.max(db_total[peak_channel + 1 + ignore_zone:]))
    next_peak_channel = np.where(db_total == next_peak_value)[0][0]
    return (next_peak_value - peak, peak_channel, next_peak_channel)

def db(x):
    # np.maximum just to prevent errors about log(0)
    return 20 * np.log10(np.maximum(1e-3, x))

def plot_vacc_data(data):
	plt.figure(1)
	plt.plot(data)
	# embed()
	# plt.figure(1)
	# plt.plot(10*np.log10(np.maximum(data,1e-8)/np.max(data)))
	plt.show()

def plot_spectral_data(data):
	data = np.abs(np.square(data))
	# plt.figure(1)
	# plt.plot(np.abs(data))
	plt.figure(2)
	plt.plot(10*np.log10(np.maximum(data,1e-4)/np.max(data)))
	# plt.show()

def plot_results_separate(data, name):
    sfdr = _compute_sfdr(db(np.abs(data)))
    db_text_y_pos = -12
    plt.style.use("ggplot")
    markers = [sfdr[1], sfdr[2]]
    plt.title(name)
    plt.ylabel("dB")
    plt.xlabel("Channel")
    plt.plot(db(np.abs(data)), label='FFT', marker="D", markevery=markers, markerfacecolor='green', markersize=9)

    plt.show()

    # if savefigs:
    #     if pfb:
    #         pfb = "pfb"
    #         filename = f"{name}_{pfb}{taps}_{batches}.png"
    #     else:
    #         filename = f"{name}_{batches}.png"
    #     plt.savefig(filename, bbox_inches='tight')
    # if savefigs==False:
    #     plt.show()