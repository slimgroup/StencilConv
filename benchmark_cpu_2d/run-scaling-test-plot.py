import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

sfmt = matplotlib.ticker.ScalarFormatter(useMathText=True)
sfmt.set_powerlimits((0, 0))
font = {'family': 'serif', 'size': 6}
matplotlib.rc('font', **font)


def img_size(n):
    return [2**(5 + j) for j in range(n)]


def input_data(filenames):

    info = {}
    for file in filenames:

        info[file] = {"nch": set(), "k": set(), "n": set()}

        with open(os.path.join('logs/', file)) as f:
            for content in f.readlines():
                line = content.rstrip().split(' ')

                if len(line) == 6:
                    op_build_time = float(line[3])
                    op_run_time = float(line[4])

                elif len(line) == 5:
                    nch = 2**int(line[0])
                    k = int(line[1])
                    n = 2**int(line[2])
                    run_time = float(line[3])
                    memory = float(line[4])

                    if not (run_time, memory) == (-1.0, -1.0):

                        info[file]["nch"].add(nch)
                        info[file]["k"].add(k)
                        info[file]["n"].add(n)

                        info[file][nch, k, n]  = (run_time, memory/(1024**2),
                                                  op_build_time, op_run_time)

        info[file]["nch"] = np.sort(list(info[file]["nch"]))
        info[file]["k"] = np.sort(list(info[file]["k"]))
        info[file]["n"] = np.sort(list(info[file]["n"]))

    return info


if __name__ == '__main__':

    filenames = ['devito-conv-split.txt',
                 'torch-conv-split.txt']

    info = input_data(filenames)

    colors = [(0.0,0.0,0.0),
              (0.0,0.584,1.0),
              (1.0,0.0,0.286),
              (0.0,0.584,0.239),
              '#c2c22f',
              '#8a8a8a',
              '#a1c0ff',
              '#ff9191',
              '#91eda2',
              '#ffff61']

    if not os.path.exists('figs/'):
        os.mkdir('figs/')

    # Plot wall-clock time
    figs = []
    axs = []
    for j, file in enumerate(info.keys()):
        for r, nch in enumerate(info[file]["nch"]):

            if j == 0:
                fig, ax = plt.subplots(figsize=(8, 3))
                figs.append(fig)
                axs.append(ax)

            for i, k in enumerate(info[file]["k"]):

                run_times = []
                n_list = []

                for n in info[file]["n"]:
                    if (nch, k, n) in info[file].keys():

                        if j == 1:
                            marker = 'v'
                        else:
                            marker = 'o'

                        run_times.append(info[file][nch, k, n][0])
                        n_list.append(n)
                        axs[r].scatter(n, info[file][nch, k, n][0],
                                       s=2, color=colors[5*j + i],
                                       marker=marker)

                if j == 1:
                    linestyle = '--'
                else:
                    linestyle = '-'
                axs[r].plot(n_list, run_times, color=colors[5*j + i],
                            linewidth=0.4, linestyle=linestyle,
                            label=(file[:file.find('-')] + " - "
                                   + r"$k={{{}}}$".format(k)))

            axs[r].legend(fontsize=6, ncol=2, loc='upper left')
            axs[r].set_ylabel("wall-clock time (s)", fontsize=8)
            axs[r].set_xlabel(r"$n$", fontsize=10)
            axs[r].set_title("OP build and 50 calls to a "
                             + r"$k \times k \ conv$"
                             + " - image size: "
                             + r"$n \times n \times {{{}}}$".format(nch))
            axs[r].set_xscale('log')
            axs[r].set_yscale('log')
            axs[r].set_xlim([2e1, 2e4])
            axs[r].set_ylim([3e-1, 6e3])
            ax.grid(True, which="both", ls="-", alpha=.2)

    for j, fig in enumerate(figs):
        fig.savefig(os.path.join('figs/', ('runtime_nch%d' % j) + '.png'),
                    format='png', bbox_inches='tight',
                    dpi=400, pad_inches=.05)
        plt.close(fig)

    # Plot OP build time
    figs = []
    axs = []
    for j, file in enumerate(info.keys()):
        for r, nch in enumerate(info[file]["nch"]):

            if j == 0:
                fig, ax = plt.subplots(figsize=(8, 3))
                figs.append(fig)
                axs.append(ax)

            for i, k in enumerate(info[file]["k"]):

                run_times = []
                n_list = []

                for n in info[file]["n"]:
                    if (nch, k, n) in info[file].keys():

                        if j == 1:
                            marker = 'v'
                        else:
                            marker = 'o'

                        run_times.append(info[file][nch, k, n][2])
                        n_list.append(n)
                        axs[r].scatter(n, info[file][nch, k, n][2],
                                       s=2, color=colors[5*j + i],
                                       marker=marker)

                if j == 1:
                    linestyle = '--'
                else:
                    linestyle = '-'
                axs[r].plot(n_list, run_times, color=colors[5*j + i],
                            linewidth=0.4, linestyle=linestyle,
                            label=(file[:file.find('-')] + " - "
                                   + r"$k={{{}}}$".format(k)))

            axs[r].legend(fontsize=6, ncol=2, loc='upper left')
            axs[r].set_ylabel("OP build time (s)", fontsize=8)
            axs[r].set_xlabel(r"$n$", fontsize=10)
            axs[r].set_title("OP build time for a "
                             + r"$k \times k \ conv$"
                             + " - image size: "
                             + r"$n \times n \times {{{}}}$".format(nch))
            axs[r].set_xscale('log')
            axs[r].set_yscale('log')
            axs[r].set_xlim([2e1, 2e4])
            axs[r].set_ylim([1e-3, 6e2])
            ax.grid(True, which="both", ls="-", alpha=.2)

    for j, fig in enumerate(figs):
        fig.savefig(os.path.join('figs/', ('op_build_runtime_nch%d' % j)
                                 + '.png'),
                    format='png', bbox_inches='tight',
                    dpi=400, pad_inches=.05)
        plt.close(fig)

    # Plot pure OP run-time
    figs = []
    axs = []
    for j, file in enumerate(info.keys()):
        for r, nch in enumerate(info[file]["nch"]):

            if j == 0:
                fig, ax = plt.subplots(figsize=(8, 3))
                figs.append(fig)
                axs.append(ax)

            for i, k in enumerate(info[file]["k"]):

                run_times = []
                n_list = []

                for n in info[file]["n"]:
                    if (nch, k, n) in info[file].keys():

                        if j == 1:
                            marker = 'v'
                        else:
                            marker = 'o'

                        run_times.append(info[file][nch, k, n][3])
                        n_list.append(n)
                        axs[r].scatter(n, info[file][nch, k, n][3],
                                       s=2, color=colors[5*j + i],
                                       marker=marker)

                if j == 1:
                    linestyle = '--'
                else:
                    linestyle = '-'
                axs[r].plot(n_list, run_times, color=colors[5*j + i],
                            linewidth=0.4, linestyle=linestyle,
                            label=(file[:file.find('-')] + " - "
                                   + r"$k={{{}}}$".format(k)))

            axs[r].legend(fontsize=6, ncol=2, loc='upper left')
            axs[r].set_ylabel("OP run-time (s)", fontsize=8)
            axs[r].set_xlabel(r"$n$", fontsize=10)
            axs[r].set_title("Only 50 calls to a "
                             + r"$k \times k \ conv$"
                             + " - image size: "
                             + r"$n \times n \times {{{}}}$".format(nch))
            axs[r].set_xscale('log')
            axs[r].set_yscale('log')
            axs[r].set_xlim([2e1, 2e4])
            axs[r].set_ylim([4e-3, 6e3])
            ax.grid(True, which="both", ls="-", alpha=.2)

    for j, fig in enumerate(figs):
        fig.savefig(os.path.join('figs/', ('op_runtime_nch%d' % j)
                                 + '.png'),
                    format='png', bbox_inches='tight',
                    dpi=400, pad_inches=.05)
        plt.close(fig)

    # Plot peak memory usage
    figs = []
    axs = []
    for j, file in enumerate(info.keys()):
        for r, nch in enumerate(info[file]["nch"]):

            if j == 0:
                fig, ax = plt.subplots(figsize=(8, 3))
                figs.append(fig)
                axs.append(ax)

            for i, k in enumerate(info[file]["k"]):

                memory = []
                n_list = []
                bckend = file[:file.find('-')]
                for n in info[file]["n"]:
                    if (nch, k, n) in info[file].keys():

                        if j == 1:
                            marker = 'v'
                        else:
                            marker = 'o'

                        memory.append(info[file][nch, k, n][1])
                        n_list.append(n)
                        axs[r].scatter(n, info[file][nch, k, n][1] - (.060468 if 'devito' in bckend else .139660),
                                       s=2, color=colors[j], marker=marker)

                if k == 3:
                    label = (bckend + r", $k=3, 5, 7, 9, 11$")
                else:
                    label = '_no_label_'
                if j == 1:
                    linestyle = '--'
                else:
                    linestyle = '-'
                if 'devito' in bckend or 'torch' in bckend:
                    const_m =.060468 if 'devito' in bckend else .139660
                    memory = [m-const_m for m in memory]
                axs[r].plot(n_list, memory, color=colors[j],
                            linestyle=linestyle,
                            linewidth=0.3, label=label, alpha=0.7)
            axs[r].legend(fontsize=6, ncol=2, loc='upper left')
            axs[r].set_ylabel("Memory (GB)", fontsize=8)
            axs[r].set_xlabel(r"$n$", fontsize=10)
            axs[r].set_title("50 calls to a " + r"$k \times k \ conv$"
                             + " - image size: "
                             + r"$n \times n \times {}$".format(int(nch)))
            axs[r].set_xscale('log', basex=2)
            axs[r].set_yscale('log', basey=2)
            axs[r].set_xlim([2e1, 2e4])
            axs[r].set_ylim([1e-2, 1e2])
            ax.grid(True, which="both", ls="-", alpha=.2)

    for j, fig in enumerate(figs):
        fig.savefig(os.path.join('figs/', ('memory_nch%d' % j) + '.png'),
                    format='png', bbox_inches='tight',
                    dpi=400, pad_inches=.05)
        plt.close(fig)
