import numpy as np
import matplotlib
import matplotlib.pyplot as plt

sfmt = matplotlib.ticker.ScalarFormatter(useMathText=True)
sfmt.set_powerlimits((0, 0))
font = {'family': 'serif',
        'size': 8}
matplotlib.rc('font', **font)

filenames = ['scaling-devito-conv-run-times.txt',
             'scaling-torch-conv-run-times.txt',
             'scaling-torch-gpu-conv-run-times.txt']

run_times = []
for file in filenames:
    with open(file) as f:
        content = f.readlines()
    content = [float(x.strip()) for x in content]
    run_times.append(content)

def img_size(n_points):
    return [2**(5 + j) for j in range(n_points)]

fig = plt.figure("Scaling", dpi=200, figsize=(7, 2.5))
plt.plot(img_size(len(run_times[0])), run_times[0],
         color='#be22d6', linewidth=1.0, label='devito on cpu')
plt.scatter(img_size(len(run_times[0])), run_times[0],
            color='#be22d6', s=1.5)

plt.plot(img_size(len(run_times[1])), run_times[1],
         color='#22c1d6', linewidth=1.0, label='torch on cpu')
plt.scatter(img_size(len(run_times[1])), run_times[1],
            color='#22c1d6', s=1.5)

plt.plot(img_size(len(run_times[2])), run_times[2],
         color='#aab304', linewidth=1.0, label='torch on gpu (4 GB)')
plt.scatter(img_size(len(run_times[2])), run_times[2],
            color='#aab304', s=1.5)

plt.legend(fontsize=8)
plt.title("200 calls to conv for image w/ size " + r"$n_x \times n_x$")
plt.ylabel("wall-clock time (s)")
plt.xlabel(r"$n_x$")
plt.xscale('log')
plt.yscale('log')
plt.grid()
plt.savefig('scaling.png' ,format='png', bbox_inches='tight',
            dpi=200, pad_inches=.05)
plt.close(fig)