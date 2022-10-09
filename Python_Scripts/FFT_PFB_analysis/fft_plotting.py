from re import I
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from IPython import embed


def _compute_sfdr(db_total):
    ignore_zone = 75 
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

# def plot_results_separate(data):
    # sfdr = _compute_sfdr(db(np.abs(data)))
    # db_text_y_pos = -12
    # plt.style.use("ggplot")
    # markers = [sfdr[1], sfdr[2]]
    # plt.title(name)
    # plt.ylabel("dB")
    # plt.xlabel("Channel")
    # plt.plot(db(np.abs(data)), label='FFT', marker="D", markevery=markers, markerfacecolor='green', markersize=9)

    # plt.show()

def plot_results_separate(data, args, taps=4, savefigs=False):
    plt.style.use("ggplot")
    for i, (spectrum, name) in enumerate(data):
        fig, axs = plt.subplots(1, 1, sharex=True, sharey=True)
        sfdr = _compute_sfdr(db(np.abs(spectrum)))
        markers = [sfdr[1], sfdr[2]]
        db_text_x_pos = 24e3
        db_text_y_pos = round(np.max(db(np.abs(spectrum))),2)-10
        axs.set_ylabel("dB")
        axs.set_xlabel("Channel")
        axs.plot(db(np.abs(spectrum)), label=name, marker="D", markevery=markers, markerfacecolor='green', markersize=7)
        axs.text(db_text_x_pos, db_text_y_pos, 'SFDR:'+ u"\u25C6" + str(round(sfdr[0],3))+'dB', color='green', style='italic')
        axs.legend(loc='upper right')

        if args.savefigs:
            filename = 'Spectrum_' + name + '.png'
            plt.savefig(filename, bbox_inches='tight', dpi = 100)

        # if savefigs:
        #     if pfb:
        #         pfb = "pfb"
        #         filename = f"{name}_{pfb}{taps}_{args.acc}.png"
        #     else:
        #         filename = f"{name}_{args.acc}.png"
        #     plt.savefig(filename, bbox_inches='tight')
    if args.savefigs==False:
        plt.show()

def plot_fft_analysis_results(data, savefigs=False):
    plt.style.use("ggplot")
    for cw_scale, wgn_scale, entry in data:
        shift = []
        overflow = [] 
        expected_input_output_ratio = []
        actual_input_output_ratio = []
        for item in entry:
            shift.append(item[1])
            overflow.append(item[2])
            expected_input_output_ratio.append(item[3])
            actual_input_output_ratio.append(int(item[4]))

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        
        ax1.plot(expected_input_output_ratio, expected_input_output_ratio, color='g', linestyle='dotted')
        ax1.scatter(expected_input_output_ratio, actual_input_output_ratio, color='b', marker="+")
        ax2.scatter(expected_input_output_ratio, overflow, color='r', marker="s")
        ax1.set_xlabel('Expected Shift (Value)')
        ax1.set_ylabel('Measured Shift (Value)', color='b')
        ax1.set_xticks(expected_input_output_ratio)
        ax1.set_yticks(expected_input_output_ratio)
        ax2.set_ylabel('FFT Oveflow', color='r')
        ax2.set_yticks([0,1])
        ax2.set_yticklabels(['False', 'True'])

        for i in range(len(expected_input_output_ratio)):
            ax1.annotate(str(shift[i]), xy=(expected_input_output_ratio[i],actual_input_output_ratio[i]))

        plt.title('FFT Shift - CW Scale:' + '' + str(cw_scale) + ' ' + 'WGN Scale:' + '' + str(wgn_scale))

        if savefigs:
            mng = plt.get_current_fig_manager()
            mng.resize(*mng.window.maxsize())
            
            figure = plt.gcf() # get current figure
            figure.set_size_inches(14, 12)

            filename = 'FFTShift_cw_' + str(cw_scale) + '_wgn_' + str(wgn_scale) + '.png'
            plt.savefig(filename, bbox_inches='tight', dpi = 100)
    if savefigs==False:
        plt.show()

    # plt.figure(1)
    # plt.scatter(expected_input_output_ratio, expected_input_output_ratio)
    # plt.scatter(expected_input_output_ratio, actual_input_output_ratio, marker ="+",)
    # plt.show()

    # fig=plt.figure()
    # ax=fig.add_axes([0,0,1,1])
    # ax.scatter(expected_input_output_ratio, expected_input_output_ratio, color='b', marker="+")
    # ax.scatter(expected_input_output_ratio, actual_input_output_ratio, color='r', marker="+")
    # ax.set_xlabel('FFT Shift')
    # ax.set_ylabel('')
    # ax.set_title('scatter plot')
    # plt.show()