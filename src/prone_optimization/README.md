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


