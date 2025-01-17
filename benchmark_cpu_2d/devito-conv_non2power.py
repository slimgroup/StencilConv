import sys
import numpy as np
from devito import (SpaceDimension, Dimension, Grid, Function, Operator, Eq,
                    configuration)
import time
configuration['log-level'] = 'ERROR'


def conv(nx, ny, nchi, ncho, n, m):

    # Image size
    dt = np.float32
    x, y, ci, co = (SpaceDimension("x"), SpaceDimension("y"), Dimension("ci"),
                    Dimension("co"))
    grid = Grid((nchi, ncho, nx, ny), dtype=dt, dimensions=(ci, co, x, y))

    # Image
    im_in = Function(name="imi", dimensions=(ci, x, y),
                     shape=(nchi, nx, ny), grid=grid, space_order=n//2)

    # Output
    im_out = Function(name="imo", dimensions=(co, x, y),
                      shape=(ncho, nx, ny), grid=grid, space_order=n//2)

    # Weights
    i, j = Dimension("i"), Dimension("j")
    W = Function(name="W", dimensions=(co, ci, i, j), shape=(ncho, nchi, n, m),
                 grid=grid)

    # Popuate weights with deterministic values
    for i in range(ncho):
        for j in range(nchi):
            W.data[i, j, :, :] = np.linspace(i+j, i+j+(n*m), n*m).reshape(n, m)

    # Convlution
    conv = [Eq(im_out, im_out
               + sum([W[co, ci, i2, i1] * im_in[ci, x+i1-n//2, y+i2-m//2]
                      for i1 in range(n) for i2 in range(m)]))]

    op = Operator(conv)
    op.cfunction

    # Initialize the input/output
    input_data = np.linspace(-1, 1, nx*ny*nchi).reshape(nchi, nx, ny)
    im_in.data[:] = input_data.astype(np.float32)
    im_out.data

    return op


if __name__ == '__main__':

    k = int(sys.argv[1])
    n = 2**int(sys.argv[2])
    nch = 2**int(sys.argv[3])

    t0 = time.time()
    op = conv(n + n//3, n + n//5, nch, nch, k, k)
    op_build_time = time.time() - t0

    t0 = time.time()
    tdv = 0
    for j in range(50):
        summary = op()
        tdv += sum([v for _, v in summary.timings.items()])
    op_run_time = time.time() - t0

    print(sys.argv[3], sys.argv[1], sys.argv[2], op_build_time,
          op_run_time, tdv)
