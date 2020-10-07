import numpy as np
from devito import *
import time
configuration['log-level'] = 'WARNING'


def conv(nx, ny, nch, n, m, n_runs):

    start_time = time.time()

    # Image size
    dt = np.float32
    x, y, c = SpaceDimension("x"), SpaceDimension("y"), Dimension("c")
    grid = Grid((nch, nx, ny), dtype=dt, dimensions=(c, x, y))

    stride = 2

    # Image
    im_in = Function(name="imi", grid=grid, space_order=1)
    input_data = np.linspace(-1, 1, nx*ny*nch).reshape(nch, nx, ny)
    im_in.data[:] = input_data.astype(np.float32)

    # Output
    im_out = Function(name="imo", grid=grid, space_order=1)
    im_out.data

    # Weights
    i, j = Dimension("i"), Dimension("j")
    W = Function(name="W", dimensions=(c, i, j), shape=(nch, n, m), grid=grid)
    # popuate weights with deterministic values
    for i in range(nch):
        W.data[i, :, :] = np.linspace(i, i+(n*m), n*m).reshape(n, m)

    # Convlution
    conv = sum([W[c, i2, i1]*im_in[c, x+i1-n//2, y+i2-m//2]
                for i1 in range(n) for i2 in range(m)])

    op = Operator(Eq(im_out, conv))
    for j in range(n_runs):
        op()

    return time.time() - start_time


if __name__ == '__main__':
    nch = 2
    n, m = 3, 3

    nx_list = [2**j for j in range(5, 15)]
    run_times = []
    for nx in nx_list:
        run_times.append(conv(nx, nx, nch, n, m, 200))

    with open('scaling-devito-conv-run-times.txt', 'w') as f:
        for item in run_times:
            f.write("%s\n" % item)