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

1. The Python ecosystem
2. Dependency management
3. GitHub
4. Unit testing
5. Documentation

---

<!--
_class: titlepage
-->

# The Python ecosystem

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

# Setting up a Python environment

To work with Python, you need to set up a development environment.

Here are the basic steps:

- **Install Python:** Download and install Python (version $\geq 3$) from the official [Python website](https://www.python.org/). Advanced users may want to have a look at [PyPy](https://www.pypy.org/).
- **Integrated Development Environment (IDE):** Choose an IDE such as PyCharm, VSCode, or Jupyter Notebook for a more interactive development experience. You can even use online platforms like [Google Colab](https://colab.google/) and [JupyterLab](https://jupyter.org/try).
- **Package management:** Utilize tools like `pip` to install and manage third-party packages.
- (Advanced users) **Virtual environments:** Use virtual environments, such as [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) to isolate project dependencies and avoid conflicts between different projects.

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

