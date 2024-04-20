# Software ecosystems

In the world of open source, software packages form an entangled ~~mess~~ ecosystem of interdependencies. Making use of it—or worse, developing in it—requires a package manager that can solve and preserve numerous *requirements*[^jax_v_torch], while attending to the available hardware. Here, we will focus on the Python ecosystem (and ajacents), for which the most popular package/environment managers are PIP and Conda.

[^jax_v_torch]: And some competing requirements may be *incompatible*: in that case, the manager should let you know, and you'll have to pick a side.

> [!TIP]
> TL;WR: I recommend [`conda`](https://conda.io/projects/conda/en/latest/user-guide/index.html) from [Miniforge](https://github.com/conda-forge/miniforge) with the [`conda-libmamba-solver`](https://conda.github.io/conda-libmamba-solver/user-guide/). Use it also for Python packages and only resort to PIP (after checking with `--dry-run` what dependencies you could install with `conda`) for the odd one that's missing on [`conda-forge`](https://conda-forge.org/packages/) and for your own (editable) packages.

## Managing Python environments with PIP

> [!TIP]
> See also the pretty good [Python Packaging User Guide](https://packaging.python.org/en/latest/).

[PIP](https://pip.pypa.io/en/stable/) is the Package Installer for Python that usually comes bundled with the interpreter. By default, it taps into the [Python Package Index (PyPI)](https://pypi.org/)—a repository to which *anyone* can submit a package: in fact, *you* will be asked to do this very soon!—but can also be used to install local packages (and their dependencies).

The basic usage is
- `pip install PACKAGE` and its dependencies.
    - `--dry-run` will preemptively show you which packages will be installed.
    - `--user`: if you're using a global Python[^global] (e.g. on a shared machine), this option (which is usually auto-applied if it's needed) directs installations to a writable user directory, thus acting as a primitive "environment" (see below).

  `PACKAGE` can be
    - a simple name like "`numpy`" (or a multiple names separated by spaces: "`numpy scipy matplotlib`").

      Optional features can be requested by specifying *extras*:
        - `PACKAGE[EXTRA, ...]` (these are arbitrarily defined by the `PACKAGE`).

      Importantly, each name can include a [*version specifier*](https://pip.pypa.io/en/stable/reference/requirement-specifiers/), e.g.
        - `PACKAGE == VERSION`: you want an exact version for some reason;
        - `PACKAGE ~= VERSION`: a "compatible" version, whatever that means[^versions];
        - `PACKAGE < VERSION`: they messed it up at `VERSION`, so you want one from before that; as a safeguard, you might put a `VERSION` from the future! For example, if `torch` is (was) currently at `1.13`, you might put `<2` since you expect them to break some stuff with a new major release[^spoiler];
        - `PACKAGE >= VERSION`: they added at `VERSION` a feature that you want.

      Remember to use "quotes" on the command line since `<`, `>` have meanings in Shell.

    - or maybe the URL of a Git repository: `git+REPO_URL@BRANCH`, if you want to install a specific unpublished (usually in-development or altogether unreleased) version (`@BRANCH` can be omitted, defaults to the tip of the default branch).

If you wish to install your own package[^release]—or at any rate, a package that you have locally *and wish to continue developing / edit* without reinstalling—you want an editable installation:
- `pip install -e DIR` ("`DIR`" is usually the current `.`). You can still ask for extras like `DIR[EXTRA, ...]`. Installing a package has several advantages over barbaric [path modification](https://docs.python.org/3/library/sys_path_init.html):
    - It takes care of dependencies! Granted, you'll run an editable installation once and forget about it, adding new dependencies manually, but the real power behind this is that it's
    - reproducible: you can easily clone your sources to a new machine (remote, continuous integration, documentation builder, ...) and install your code, ensuring its requirements are met.

For completeness, to uninstall a package, simply ask:
- `pip uninstall PACKAGE` by name.

[^global]: Bad idea: shared / global Pythons are usually old and come with an undefined ~~mess~~ environment of already installed packages, some of which may be vital to the overall operation of the system... Better to install your own from scratch using e.g. Conda or [`pyenv`](https://github.com/pyenv/pyenv). I'd like to warn you though that choosing a Python version is a wedding: in that if you want a newer spouse, e.g. to enjoy some newer features, you'll need to reinstall everything from scratch (and will probably lose half your stuff in the process). None of the package managers discussed below can help you with that. The only one I've seen pull it off is [Arch Linux's Pacman](https://wiki.archlinux.org/title/python#Installation). On the other hand, Conda, `pyenv`, and `virtualenv` do support *multiple Python versions at the same time* (in different environments), but that's [cheating](https://en.wikipedia.org/wiki/Thou_shalt_not_commit_adultery).

[^versions]: I refer the curious (and bored) to [Version Specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/).

[^spoiler]: Spoiler: they didn't! But a bunch of packages that were requiring "`torch<2`" still managed to have [issues](https://github.com/pyro-ppl/pyro/issues/3162) with that.

[^release]: For that, you'll need to first *make* your package installable: this is your second warning for the exercise session.

### Virtual environments

Often[^often] one might ~~experience congnitive dissonance~~ face conflicting requirements: where new features of a package are required for one project, but the changes introduced in new versions break some old code that one insists on blindly using for another project.[^blind] In that case, the *builtin* module [`venv`](https://docs.python.org/3/library/venv.html)[^venv] can help you create two (or more, some people go crazy) *separate* environments that you can switch between at will. The guide in the documentation does a pretty good job[^source] at explaining how to create and manage virtual environments, so I'll just briefly summarise it, noting that popular IDEs have first-class (point-and-click) support for venvs:
- `python -m venv VENV_PATH` (`VENV_PATH` is usually "`.venv`" within your current directory) creates a virtual environment. I'd strongly recommend `--system-site-packages` to include any packages lying around in the global (+ user) Python installation already. These can then be overridden just as `--user` overrides global packages.
- `source VENV_PATH/bin/activate` (or similar) to "activate" the environment for the current Shell session (the command line prompt will be modified to indicate that). Now any Pythons you run will "see" this particular environment's packages.
- Modify the environment (once activated) with PIP as usual. Note that any installations won't be visible when the venv is deactivated.

Beware that venvs contain local copies of all their private packages: so if you end up installing NumPy, PyTorch, etc. over and over again, you might consider installing them in a more global and shared place, to save space.

[^often]: Well, here is some data: I have been developing in Python for, let's say, 6 years, and I've never used virtual environments: I think they're for [REDACTED] who can't keep up with the relentless passage of time. --KK

[^blind]: Okay, less harshly now: sometimes you want to develop on top of some new feature but are also using someone else's old codebase that you can't really modify, and that person has left academia.

[^venv]: There is also the third-party module [`virtualenv`](https://virtualenv.pypa.io/en/stable/index.html) with some additional features (supposedly).

[^source]: and is my only source of knowledge about venvs anyway...

## Beyond Python: Conda

Conda is like PIP+`venv` but for software *beyond* Python, although it can be used to install and manage Python packages as well—and is actually pretty good at it, once you smooth out some quirks. So before we demonstrate usage, let's discuss the quirks:
- Conda is an idea, which can be instantiated in many ways[^conda-idea]: [Anaconda](https://www.anaconda.com/download), [Miniconda](https://docs.anaconda.com/free/miniconda/), [Mamba](https://mamba.readthedocs.io/en/latest/index.html), [Miniforge](https://github.com/conda-forge/miniforge). What unites them is the way they perceive the software ~~mess~~ ecosystem: through the lens of
- channels. A Conda "channel" is a repository of Conda packages: metadata and build/install instructions and/or pre-built distributions for various software. A channel contains many versions of each software, further specialised to different operating systems, Python versions, hardware, etc...

  Conda itself requires some software to run, so it provides the
    - *default* channels. However, they are sometimes outdated ([and probably bad for your environment](https://mamba.readthedocs.io/en/latest/user_guide/troubleshooting.html#mixing-the-defaults-and-conda-forge-channels)), so people[^I] use
    - [`conda-forge`](https://conda-forge.org/).
    - Nvidia software is not open source, so they run [their own channel](https://anaconda.org/nvidia). Confusingly, some of their packages are available from other channels as well.
    - PyTorch also maintain [a Conda channel](https://anaconda.org/pytorch). Confusingly, `torch` is also perfectly available from `conda-forge`.

  It is important to realise that packages from the different channels are equivalent, and so the package manager is ["free"](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html) to choose the best-fitting version from any of the configured channels *at any point*: including when an already installed package is required by a new addition to the environment.

  All this makes solving requirements ~~unnecessarily~~ very complicated in Conda, especially if an environment starts off with some default packages / channels and moves on to others. But hey, computers are fast and good at algorithmic processing, right? Right?
- Mamba: do yourself a favour and use Mamba or at least [their solver as a plugin to Conda](https://conda.github.io/conda-libmamba-solver/user-guide/). It solves environments \*much\* faster than the builtin solver (i.e. within the age of the Universe).

[^conda-idea]: Read: "there are a number of installers that provide `conda` (or similar)".

[^I]: I


### Using Conda

> [!TIP]
> Take a look at the [User Guide](https://conda.io/projects/conda/en/latest/user-guide/index.html). What follows is a biased summary.

#### Install

Did you think it's more complicated than
- `conda install PACKAGE [PACKAGE ...]`? You can specify
    - `-c CHANNEL` to consider (with priority) a channel outside of those [configured globally](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html);
    - `-h` to see what else is available (nothing crucial).

#### Environments

Of course, it is more complicated than that. Conda treats [*environments*](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) as first-class citizens and needs one to be explicitly activated[^conda-env]. Most Conda installers will set up [automatic activation of the `base` environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#conda-init) upon login: if this is not desired (but why wouldn't it?!),
- `conda config --set auto_activate_base false`.

An environment can be
- [`conda create -n NAME`](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands),
- [`conda remove -n NAME --all`](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#removing-an-environment),
- [`conda activate [--stack] NAME`](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) or [`conda deactivate`](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#deactivating-an-environment),
- [rolled back](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#restoring-an-environment),
- and conveniently [exported as a minimal list of requirements](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#building-identical-conda-environments) that can reproduce it!

> [!WARNING]
> Conda environments do not inherit (I think), i.e. each is independent, hence, bulky. Use them sparingly. Note also that [Mamba obligates you to not use `base`](https://mamba.readthedocs.io/en/latest/user_guide/troubleshooting.html#no-other-packages-should-be-installed-to-base) (the the Mamba solver doesn't have this restriction).

[^conda-env]: The active environent is indicated with an `(ENV)` prefix to the command-line prompt.

#### Closing remarks on Conda
- A particular advantage of Conda over more manual / less integrated approaches to installing a ML stack is that it can handle GPU-related software like Nvidia's CUDA (toolkit), which is e.g. required by PyTorch: if installing it by PIP, you'll need to satisfy this requirement in some other way.
- You *can* still use [PIP within a Conda environment](https://www.anaconda.com/blog/using-pip-in-a-conda-environment) (but only do this for packages that are not otherwise available)!
- [`conda list`](https://conda.io/projects/conda/en/latest/commands/list.html) will [show you what you've got](https://www.youtube.com/watch?v=Ga8zpMMCD98).
- [`conda search PATTERN`](https://conda.io/projects/conda/en/latest/commands/search.html) will search for `PATTERN` (see the examples in the link), returning all available versions from all configured channels. Or you could use [the internet](https://anaconda.org/).