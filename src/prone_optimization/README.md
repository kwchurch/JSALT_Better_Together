# Prone Optimzation
<h1>Cython Code Creation</h1>
<ol>
<li><a href="https://cython.readthedocs.io/en/latest/src/quickstart/build.html">Baseline Link</a></li>
<li><a href="https://www.peterbaumgartner.com/blog/intro-to-just-enough-cython-to-be-useful">Quick Example</a></li>
</ol>
Cython is a manner of compiling any Python code into its C equivalent.
It optimizes variables and other memory calls to run faster in C.
When used for Prone (ran 10 times taking the average), we were able to get several runs on average 10 seconds speedup (on a small fraction of the graph -- 10%).
The original TSVD code from Sci-Py that uses Python takes about 90 seconds on the Northeastern "short" queue CPU boxes, when using Cython-compiled Prone.py it runs in about 80 seconds (10% speed up).
<h2>Logic</h2>
In order to run Cython, you will need to:

```sh
pip install cython
python setup.py build_ext --inplace
```

This assumes that you have updated the setup.py file with your filename, please see the setup.py file for help.
In this directory there is a file called "prone.pyx" which is used to create the binary below.
That will create a binary C object (a .so file like prone.cpython-39-x86_64-linux-gnu.so) that can then be used similar to the Python code by importing the name of your library.
For example, in this directory there is a "prone" library that can be imported.

<h2>Execution</h2>
With the c code and binary object you are then able to use an import prone as is done in the dict_to_embedding.cython.py
The cython file is identical to the original dict_to_embedding.py file with the exception of the call to the "new" prone call.
You only have to ensure that the .so library file and the .c file are in the path.

<h1>DASK use for tiling and GPU/CPU runs</h1>
<ol>
<li><a href="https://blog.dask.org/2020/05/13/large-svds">Link from Hui</a></li>
</ol>
The Dask library is done with pip.
The code is found in prone_dax_added.py from lines 170 - 190.
The most important paramter is the tile setting and can be configured according to the architecture.
Currently, on 10 runs using 100,100 tiles (this was found over several runs but may need to be optimized) the time to run went from 20k secs on a single cpu to 250 secs on average for a single GPU.
Ideally, we could create a ticket on the NE clusters to get multiple GPUs and there may be a speed up to surpass the current TSVD from scipy which on average is about 90 seconds on the short queue boxes cpus.


<h1>Memory and Time Profiling</h1>
For memory and time profiling, the _opt files take advantage of the python memory profiler and the Kernprof line profiler. They can be installed using the following commands:

```sh
pip install memory-profiler
pip install line_profiler
```

Here is an example memory profile run for the memory profiler on the chebyshev step, and the 0th partition of the semantic scholar graph: 

```sh
python -m memory_profiler prone_chebyshev_opt.py -G /work/k.church/JSALT-2023/semantic_scholar/j.ortega/cumgraphs.V2/000.sym.shrunk.G2.npz -U /scratch/k.church/JSALT-2023/semantic_scholar/j.ortega/cumgraphs.V2/000.sym.shrunk.G2.U.K280.npy --iteration 0 --temp_file_prefix /scratch/irving.b/JSALT/cheby/000
```

Run on the Northeastern cluster, this should produce the following output:

```sh
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    24  164.816 MiB  164.816 MiB           1   @profile
    25                                         def first_iter(i, temp_file_prefix, theta):
    26  164.816 MiB    0.000 MiB           1       if (i == 0):
    27  164.816 MiB    0.000 MiB           1           print(str(time.time() - t0) + ' about to load U: %s' % (str(args.U)), file=sys.stderr)
    28  164.816 MiB    0.000 MiB           1           sys.stderr.flush() 
    29  726.199 MiB  561.383 MiB           1           U = np.load(args.U).astype(np.float32)
    30  726.199 MiB    0.000 MiB           1           N = U.shape[0]
    31  726.199 MiB    0.000 MiB           1           K = U.shape[1]
    32  726.199 MiB    0.000 MiB           1           sys.stderr.flush()
    33  726.199 MiB    0.000 MiB           1           print('%0.2f sec: loaded U with shape: %s' % (time.time() - t0, str(U.shape)), file=sys.stderr)
    34  726.199 MiB    0.000 MiB           1           t = time.time()
    35  726.199 MiB    0.000 MiB           1           Lx0 = U
    36  726.199 MiB    0.000 MiB           1           del U
    37  789.949 MiB   63.750 MiB           1           M = load_m(temp_file_prefix, K, N)
    38 1350.461 MiB  560.512 MiB           1           Lx1 = M @ Lx0
    39 1350.617 MiB    0.156 MiB           1           Lx1 = 0.5 * M @ Lx1 - Lx0
    40 1286.320 MiB  -64.297 MiB           1           del M
    41 1846.820 MiB  560.500 MiB           1           conv = special.iv(0, theta) * Lx0
    42 1846.848 MiB    0.027 MiB           1           conv -= 2 * special.iv(1, theta) * Lx1
    43 1846.848 MiB    0.000 MiB           1           print('First iteration computation: ', time.time() - t)
    44 1846.848 MiB    0.000 MiB           1           return Lx0, Lx1, conv
```

For time profiling, we use the Kernprof library. An example run would look like this: 

```sh
kernprof -l -v prone_chebyshev_opt.py -G /work/k.church/JSALT-2023/semantic_scholar/j.ortega/cumgraphs.V2/000.sym.shrunk.G2.npz -U /scratch/k.church/JSALT-2023/semantic_scholar/j.ortega/cumgraphs.V2/000.sym.shrunk.G2.U.K280.npy --iteration 0 --temp_file_prefix /scratch/irving.b/JSALT/cheby/000
```

This should produce the following output:

```sh
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    24                                           @profile
    25                                           def first_iter(i, temp_file_prefix, theta):
    26         1          3.3      3.3      0.0      if (i == 0):
    27         1        100.4    100.4      0.0          print(str(time.time() - t0) + ' about to load U: %s' % (str(args.U)), file=sys.stderr)
    28         1          2.5      2.5      0.0          sys.stderr.flush() 
    29         1     902957.4 902957.4     23.7          U = np.load(args.U).astype(np.float32)
    30         1          8.5      8.5      0.0          N = U.shape[0]
    31         1          0.9      0.9      0.0          K = U.shape[1]
    32         1         18.5     18.5      0.0          sys.stderr.flush()
    33         1        212.5    212.5      0.0          print('%0.2f sec: loaded U with shape: %s' % (time.time() - t0, str(U.shape)), file=sys.stderr)
    34         1          1.7      1.7      0.0          t = time.time()
    35         1          0.5      0.5      0.0          Lx0 = U
    36         1     176188.3 176188.3      4.6          M = load_m(temp_file_prefix, K, N)
    37         1     969393.3 969393.3     25.5          Lx1 = M @ Lx0
    38         1    1063170.8 1063170.8     27.9          Lx1 = 0.5 * M @ Lx1 - Lx0
    39         1        955.7    955.7      0.0          del M
    40         1     282886.0 282886.0      7.4          conv = special.iv(0, theta) * Lx0
    41         1     409202.7 409202.7     10.8          conv -= 2 * special.iv(1, theta) * Lx1
    42         1        195.6    195.6      0.0          print('First iteration computation: ', time.time() - t)
    43         1          1.9      1.9      0.0          return Lx0, Lx1, conv
```

