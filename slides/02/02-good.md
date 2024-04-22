<!--
title: Lecture 02
paginate: true

_class: titlepage
-->

# Lecture 02
<br>

## A hitchhiker's guide to coding
<br>

#### High Performance Computing for Data Science - SISSA, UniTS, 2023-2024

###### Pasquale Claudio Africa, Konstantin Karchev

###### 23 Apr 2024

---

# Outline

1. The role of Python in modern scientific computing
2. Dependency management
3. GitHub
4. Unit testing
5. Documentation

---

<!--
_class: titlepage
-->

# The role of Python in modern scientific computing

---

# The role of Python in modern scientific computing

Python has emerged as a pivotal language in scientific computing, distinguished by:

- Intuitive and readable syntax, making coding accessible to scientists from various fields.
- A vast array of libraries and tools tailored for scientific applications.

Python's versatility extends across numerous scientific domains:

- In physics, it's used for simulations and theoretical calculations.
- In biology and chemistry, Python aids in molecular modeling and genomic data analysis.
- Its application in astronomy includes data processing from telescopes and space missions.
- In environmental science, it's pivotal in climate modeling and biodiversity studies.

---

# Python's library ecosystem for scientific computing

The power of Python in scientific computing is amplified by its extensive library ecosystem:

- NumPy and SciPy are fundamental for numerical computations.
- pandas enhances data manipulation and analysis capabilities.
- Matplotlib and Seaborn excel in creating scientific visualizations.
- TensorFlow and PyTorch are at the forefront of machine learning research and applications.

Python's role in democratizing scientific research is underscored by its open-source nature, fostering collaboration and innovation.

---

# Real-world applications of Python in scientific research

Python's impact in scientific research is evident through numerous real-world applications:

- In physics, it has been used to analyze data from the Large Hadron Collider.
- In biology, Python is integral in genome sequencing projects like the Human Genome Project.
- Environmental scientists utilize Python in modeling the effects of climate change on different ecosystems.
- In astronomy, it played a key role in processing the first image of a black hole.

These applications underscore Python's versatility and effectiveness in advancing scientific knowledge.

---

# How to get your system ready

Most Python libraries can be installed with `pip`, with [`Conda`](https://conda.io), with a package manager on Linux and macOS, or from source.

- Using `pip`:

    ```bash
    pip install numpy scipy matplotlib seaborn pandas
    ```

- Using `Conda`:

    ```bash
    conda create -n sci-env
    conda activate sci-env
    conda install numpy scipy matplotlib seaborn pandas
    ```

Best practices in setting up a scientific computing environment include creating isolated environments and maintaining updated library versions.

---

# PyPy and Numba overview

- [**PyPy**](https://www.pypy.org/)
  - Alternative Python implementation focusing on speed.
  - JIT Compiler for runtime compilation.
  - Less memory usage, compatible with CPython.
  - Faster for long-running processes.
  - **Limitations**: Library support, JIT warm-up time.
- [**Numba**](https://numba.pydata.org/)
  - JIT compiler for Python and NumPy code.
  - Easy to use, significant performance improvements.
  - Integrates with Python scientific stack.
  - Supports CUDA GPU programming.
  - **Limitations**: Focused on numerical computing, learning curve for parallel programming, debugging challenges.

---

