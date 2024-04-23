# Preparing Python Projects for Packaging and Public Propagation

> [!TIP]
> The [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) tutorial and [Building and Publishing](https://packaging.python.org/en/latest/guides/section-build-and-publish/) guide are your friends. [PEP 621](https://peps.python.org/pep-0621/) is your law. As always, the following is mostly a condensed summary of those superior resources.

## Terminology

- "package": a *directory* containing an `__init__.py` file[^complicated]
    - "subpackage": a package contained within another package
    - "module": a `.py` file within a (sub)package

  Modules and (sub)packages (their `__init__.py`) are the targets of Python `import`s.
- "project": extends a package (or a collection of many packages!) with metadata like name, author, build/install instructions and dependencies (for building/installing and/or running packages), documentation, tests, etc.

> [!NOTE]
> Packages are found *within* the project root: either "on the surface" (`PROJECT_ROOT/PKG_NAME`) or in a source directory (`PROJECT_ROOT/src/PKG_NAME`).

> [!IMPORTANT]
> No `.py` files directly in the project root ever! All the `.py` files containing code you'd like to distribute and/or `import` should be within a (sub)package.

- "script": a Python file outside a package. Shouldn't exist. If you want to distribute *behaviour* (i.e. *scripts*) instead of *modules* of classes and functions, see [Entry points → Console Scripts](https://setuptools.pypa.io/en/latest/userguide/entry_point.html#console-scripts).

[^complicated]: Of course, it's [more](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/). [complicated](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/).


## [`pyproject.toml`](https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-toml-spec)

> [!IMPORTANT]
> There are many ways to prepare a Python project for publication. It's good to recognise "`setup.py`" and "`setup.cfg`" as alternative/old Python packaging configurations, just for general culture[^culture], but in this course, we'll cover only the modern approach using "`pyproject.toml`" that tightly integrates with Pip.

[^culture]: Historically, the way to install *packages* for use with Python was through the built-in [distutils](https://docs.python.org/3.11/library/distutils.html) module. This was extended to *projects* via [setuptools](https://setuptools.pypa.io/en/latest/). While the former is now deprecated (and [removed from Python 3.12](https://docs.python.org/3.12/whatsnew/3.12.html#distutils)), setuptools is still the primary *build* tool for Python projects (used under the hood by Pip). However, a growing number of similar tools have recently emerged and challenged the Pip/setuptools duumvirate: e.g. <a name="alts"></a>[Poetry](https://python-poetry.org), [Flit](https://flit.pypa.io/), [PDM](https://pdm-project.org/), [Hatch](https://hatch.pypa.io/). Note that they *all* use more or less the same "`pyproject.toml`"-based configuration! However, I personally haven't found any significant advantages over Pip/setuptools. ¯\\\_(ツ)\_/¯

`pyproject.toml` is a [TOML](https://toml.io/) file that you include in the root of your Python *project* to describe it. It contains multiple *tables* of metadata:

### [`[build-system]`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#declaring-the-build-backend)
tells Pip[^installer] what tool to use to *build* the project. As such, the packages listed here are not required for *running* your software, so they may not be installed if the package manager finds a suitable pre-built [*wheel*](#wheels).[^reinvent] In this guide, we'll focus on setuptools:
```toml
[build-system]
  requires = ["setuptools"]
  build-backend = "setuptools.build_meta"
```

### [`[project]`](https://packaging.python.org/en/latest/specifications/pyproject-toml/#declaring-project-metadata-the-project-table)
Project metadata:
- basic stuff:
  ```toml
  [project]
  name = "BetaFold"
  description = "Cures cancer"
  authors = [
    {name = "YOU!", email = "you@hotmail.com"},
    {name = "ChatGPT"}
  ]
  ```
- [`version = "..."`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#version) but see [Versioning](#versioning);
- <a name="legal"></a>legal stuff:
    - [`readme = ...`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#readme);
    - [`license = ...`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license);
- [`requires-python = ">=..."`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#requires-python): are you cutting-edge?
- dependencies: a list of names of packages with optional [version specifiers](https://packaging.python.org/en/latest/specifications/dependency-specifiers).
    - ```toml
      [project]
      dependencies = [
        "numpy", "scipy", "pytorch >= 2",
        "magic[black]"
      ]
      ```
      lists the *required* dependencies of your project: a package manager installing your software *will* install these as well—if they are not already available—else fail.
    - ```toml
      [project.optional-dependencies]
      EXTRA_NAME = [...]
      # ...
      ```
      The package manager will install these only if requested through "`PACKAGE[EXTRA_NAME]`": for example, "`magic[black]`" (supposing there's a perfectly usable package of non-black `magic`).

[^installer]: or whatever other package manager you're using...

[^reinvern]: Do not re-invent them! (unless you really enjoy coding)

#### Versioning

There are numerous (exactly 7: see [here](https://packaging.python.org/en/latest/guides/single-sourcing-package-version/)) ways to set a *version* for your package globally so that it's reused across source files, project metadata, and documentation. I recommend [`setuptools_scm`](https://setuptools-scm.readthedocs.io/), which extracts/generates a version from the Git history (see [here](https://setuptools-scm.readthedocs.io/en/latest/usage/#default-versioning-scheme) for the default scheme). To enable it, you need to
1. list `setuptools_scm` as a build requirement:
   ```toml
   [build-system]
   requires = [..., "setuptools_scm"]
   ```
2. list "`version`" as [dynamic](https://packaging.python.org/en/latest/specifications/pyproject-toml/#dynamic) for the benefit of the builder:
   ```toml
   [project]
   dynamic = ["version"]
   ```
3. <a name="scm_table"></a>enable `setuptools_scm` via a [dedicated table](#tooltoolname-tables) `[tool.setuptools_scm]`. Here you can include optional configuration like
    - `version_file = "package/root/_version.py"` (relative to the *project* root): `setuptools_scm` will write something like
      ```python
      # file generated by setuptools_scm
      # don't change, don't track in version control
      __version__ = version = '4.2'
      __version_tuple__ = version_tuple = (4, 2)
      ```
      From within your package (or elsewhere, e.g. in the documentation), you can then import that file and read in the real package version from the `__version__`, etc. variables.
    - [`version_scheme = "..."`](https://setuptools-scm.readthedocs.io/en/latest/extending/#version-number-construction): specifies how the version is "calculated" from the Git history. See the link for available options.

If you have set up your Git repository and possibly tagged a commit with a version-like string (e.g. `v4.2`), you're good to go.

### `[tool.TOOLNAME]` tables

Each "tool" can define its own settings within a dedicated table. We've already [seen this](#scm_table) for `setuptools_scm`, but what about [setuptools themselves](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html#setuptools-specific-configuration)?

> [!WARNING]
> This section will quickly get very technical and maybe confusing. I'll try to simplify it as much as I can, but seeing as it's entirely setuptools' fault, maybe some of [these alternatives](#alts) might actually be worth looking into.

<a name="include"></a>
You'd probably want to specify [which files get packaged](https://setuptools.pypa.io/en/latest/userguide/miscellaneous.html#controlling-files-in-the-distribution); these may be
- [source files](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html). Setuptools have ["automatic package discovery"](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#automatic-discovery), but if this doesn't work (or you just want to be [in control](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#custom-discovery)):
  ```toml
  [tool.setuptools.packages.find]
  include = ["GLOB", ...]
  exclude = ["GLOB", ...]
  ```
  where the `GLOB` patterns indicate the packages (directories) to include/exclude, along with all modules (`.py` files) within them. If you use the "`src`" layout, include a `where = "src"` entry (by default, it's the *project* root, i.e. `"."`).
- or [data files](https://setuptools.pypa.io/en/latest/userguide/datafiles.html): e.g. containing saved arrays or [images of pasta](https://github.com/LR-inaf/pasta-marker/tree/main)[^pasta]. By default, *all* files within declared (or discovered) packages are included in the distribution, *if they're tracked by Git and `setuptools_scm` is used*... Again, for the control freaks:
  ```toml
  [tool.setuptools.package-data]
  PKG_NAME = ["GLOB", ...]
  # ...
  
  [tool.setuptools.exclude-package-data]
  PKG_NAME = ["GLOB", ...]
  ```

[^pasta]: bad example: in that project, the pasta outlines are defined inline in [a source file](https://github.com/LR-inaf/pasta-marker/blob/main/pastamarkers/markers.py)...

#### [What's in the paaackage?](https://www.youtube.com/watch?v=lHpHxLZReiI)

It can be hard to convince yourself you're doing exactly what you want through `packages.find` and `package_data`. How can you verify you've selected the correct set of files? One way is to actually build a source distribution as if you're [preparing to publish](#build) your project:
```shell
python -m build --sdist
```
You can then inspect the source distribution and see [what's in there](https://www.youtube.com/watch?v=UxgZnVTyWRk&t=78s)!

> [!CAUTION]
> Are you using `setuptools_scm`? Tough luck, everything (that's tracked in Git) is included in your source distribution. It's an... [ undocumented feature?!?](https://github.com/pypa/setuptools_scm/issues/190)... that the `setuptools_scm` developers refuse to fix.
>
> In that case, you can still `python -m build --wheel` and inspect that.

## Building extensions

If you want to build (C++, CUDA, ...) extensions that interface with Python code, you're probably more advanced than the level this guide is aimed at.  Let's, then, pretend that this section is

> [!WARNING]
> UNDER CONSTRUCTION

and in the meantime consult [PyPA → Packaging binary extensions](https://packaging.python.org/en/latest/guides/packaging-binary-extensions/), [Setuptools → Building Extension Modules](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html), and e.g. [PyTorch → Custom C++ and CUDA Extensions](https://pytorch.org/tutorials/advanced/cpp_extension.html).

## Publishing on PyPI

Okay, only a few steps remain before you're a published author (of a Python package[^terminology]).[^flesh]

[^terminology]: project

[^flesh]: Before proceeding, remember to flesh out any readme or license you promised [above](#legal).

### [Build](https://en.wikipedia.org/wiki/Bob_the_Builder_(character))

Install the tiny Python module[^terminology] [`build`](https://pypi.org/project/build/). Then, from your *project root*, run
```shell
python -m build
```

This will create two artefacts inside `PROJECT_ROOT/dist`:
- a [source distribution (`sdist`)](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist): a collection of the Python sources (and some supporting files);
- a [wheel](https://en.wikipedia.org/wiki/Wheel): a "built distribution" that is *directly installable*. If your project/package is pure Python (i.e. no compiled extensions), the wheel is mostly the same as a source distribution, but *(c)leaner*. Otherwise, wheels can be built for each combination of [architecture * operating system * Python version](https://packaging.python.org/en/latest/guides/packaging-binary-extensions/#building-extensions-for-multiple-platforms) you[^wheelbuilders] wish to support.

[^wheels]: You've heard[^maybe] of Ruby on Rails, now prepare for Python in [Wheels](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#wheels)[^eggs].

[^maybe]: maybe

[^eggs]: [Wheels are the new eggs](https://packaging.python.org/en/latest/discussions/package-formats/#what-about-eggs)... Poor name choice, @[Hatch](https://github.com/pypa/hatch).

[^wheelbuilders]: *Others*, e.g. *conda-forge*, might wish to build wheels for your package independently (starting from your source distribution), if your package is famous enough.

### [twine](https://en.wikipedia.org/wiki/Twine)

Good, now you just need to
- Register on ([Test.](https://test.pypi.org/))[PyPI.org](https://pypi.org/) (follow instructions [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives)).
    - They are entirely separate: you cannot transfer projects from test to "production".
    - Once a project name is registered on either package index, *that name is taken forever*!
- Install [twine](https://pypi.org/project/twine/) and run (continuing to follow [those](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives) instructions)
  ```shell
  python -m twine upload [--repository testpypi] dist/*
  ```

Congratulations, you're a published author![^peer-review] [You deserve cake!](https://packaging.python.org/en/latest/tutorials/packaging-projects/#next-steps)

[^peer-review]: This is not a refereed publication. To make you module/package/project [journal](https://joss.theoj.org/)-worthy, you'll need to work a bit harder, but that's very soon to come.

### Publish hook on GitHub

See [this guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/) and [this GitHub action](https://github.com/marketplace/actions/pypi-publish). Maybe one day I'll elaborate.
