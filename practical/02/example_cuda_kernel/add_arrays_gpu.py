# -*- coding: utf-8 -*-
"""add_arrays_gpu

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KQui0t4Hqp2PJcgBI2Gf1IvAqBhozk5-
"""

import cupy as cp
import numpy as np
import time

# Define a CUDA kernel as a raw string.
cuda_kernel = """
extern "C" __global__
void add_arrays(const float * x, const float * y, float * z, int size)
{
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid < size)
      {
        z[tid] = x[tid] + y[tid];
      }
}
"""

# Compile the CUDA kernel.
add_kernel = cp.RawKernel(cuda_kernel, 'add_arrays')
add_kernel.compile()

# Define array size.
size = int(1e8)

# Create random arrays.
np.random.seed(0)
x = np.random.rand(size).astype(np.float32)
y = np.random.rand(size).astype(np.float32)

# Copy arrays to device.
x_gpu = cp.asarray(x)
y_gpu = cp.asarray(y)
z_gpu = cp.zeros_like(x)

# Grid and block sizes.
block_size = 256
grid_size = (size + block_size - 1) // block_size

# Launch the kernel.
start_gpu = time.time()
add_kernel((grid_size,), (block_size,), (x_gpu, y_gpu, z_gpu, size))  # grid, block and arguments
end_gpu = time.time()
time_gpu = end_gpu - start_gpu

# Check the result (for example, by printing some of the output).
print(z_gpu[:10])
print(f"Elapsed time: {time_gpu}ms")

def add_arrays(x, y):
    return x + y

# Perform the addition.
start_cpu = time.time()
z = add_arrays(x, y)
end_cpu = time.time()
time_cpu = end_cpu - start_cpu

# Check the result (for example, by printing some of the output).
print(z[:10])
print(f"Elapsed time: {time_cpu}ms")

print(f"Speedup: {(time_cpu) / (time_gpu)}")