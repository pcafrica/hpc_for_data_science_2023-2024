# Documenting Python

You may have been advised previously to put comments in your code, to remind you what it's doing lest you forget—or worse, lest someone else tries to comprehend it. But commenting code is a chore concerned with details of the program's internal workings—that can be elucidated simply through the use of sensible variable names. In contrast, writing documentation is art: it aims to explain how to use a piece of software and put its various pieces in a larger context. Moreover, it is often meant to *define* aspects of the software: hence the term "[undocumented behaviour](https://en.wikipedia.org/wiki/Undocumented_feature)", i.e. a feature that the developer does not commit to preserving or caring for.

## Sphinx: the Python documentation tool

Again, documentation is art, and art is limitless, but I'll try to be brief and guide you through some basics. If you're serious about it, do read through the [Sphinx User Guide](https://www.sphinx-doc.org/en/master/usage/index.html): your future users will thank you.

`sphinx` is a Python package. Install it in your preferred way. Then make a `/docs` directory within your package and run
```shell
sphinx-quickstart
```
It will talk to you a bit and set up a Sphinx docs source directory, replete with
- an `index.rst` file for the landing page of the documentation (see [below](#what-goes-in-a-doc) for what to write in there);
- a [`conf.py` that configures the workings of Sphinx](https://www.sphinx-doc.org/en/master/usage/configuration.html). It'll be partially filled in based on your conversation with `sphinx-quickstart`. Here are some useful settings (all are put simply as variables in `conf.py`):
  - self-explanatory:
    - [`project`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-project),
    - [`author`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-author),
    - [`copyright`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-copyright): use e.g. [`datetime.datetime.now()`](https://docs.python.org/3/library/datetime.html#datetime.datetime.now),
    - [`version`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-version): import your project and use `package.__version__` (see also [setuptools_scm](https://setuptools-scm.readthedocs.io/en/stable/) for a way to set automatic versioning based on Git);
  - [`html_theme`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme): a very important and definitely not superficial aspect of your docs is their look. Choose a theme from e.g. [sphinx-themes.org](https://sphinx-themes.org/); along those lines, do you like web design?:
    - [`html_static_path`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_static_path), [`html_css_files`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_css_files), [`html_js_files`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_js_files)
  - [`highlight_language`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-highlight_language): the default programming language for highlighting code examples;
  - [`default_role`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-default_role): this is super useful! Set it to `'any'`. I'll explain [later](#what-goes-in-a-doc);
  - [`extensions`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-extensions) ([later](#extensions), but sooner than "`any`");
    - options particular to each loaded extension.
- a `Makefile` (please ask for it) that lets you build the documentation[^build] with
  ```shell
  make html
  ```

[^build]: You might want to survey the results of compiling ("building") your documentation locally before pushing it to an online service like [Read the Docs](#publishing-on-read-the-docs), which handles the build automatically (when [configured](#configuring-the-build) properly).

### Extensions

Extensions add functionality to Sphinx. They are simply Python modules listed in the [`extensions`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-extensions) configuration variable. Here are a few useful ones (we'll introduce a few more further below):
- [`sphinx.ext.mathjax`](https://www.sphinx-doc.org/en/master/usage/extensions/math.html#module-sphinx.ext.mathjax): use LaTeX (equations) in your docs;
- [`sphinx.ext.intersphinx`](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html): Remember how I said docs put your code in a larger context? This is it, Intersphinx is the larger context. It is an extension, bundled with Sphinx, that allows you to link to the documentation *of other projects*. I encourage you to overuse it: to the extent that every time you say "Tensor" in your documentation, it's actually `` `~torch.Tensor` `` (renders as [Tensor](https://pytorch.org/docs/stable/tensors.html#torch.Tensor), if you've set up `default_role = 'any'`);
- [`sphinx.ext.inheritance_diagram`](https://www.sphinx-doc.org/en/master/usage/extensions/inheritance.html) if you're into object-oriented programming and graphs!
- [`sphinx.ext.viewcode`](https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html), [`sphinx.ext.linkcode`](https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html): do what it says on the tin;
- [`sphinx-design`](https://sphinx-design.readthedocs.io/en/latest/): do you like fancy web design (and useful elements for your docs)?
- [`myst_parser`](https://myst-parser.readthedocs.io/en/latest/): if you don't like reStructuredText and prefer Markdown. It's a big thing lately.

### What goes in a Doc

You can put whatever you want in the [reStructuredText](https://docutils.sourceforge.io/rst.html) (check out the [Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) for its syntax: you'll use it one way or another (unless you really hate it and want to set up Markdown: in which case check out *its* [Cheat Sheet](https://www.markdownguide.org/basic-syntax/))) files of your documentation! Below, I'll tell you what you *should* put in them, but first, how:

> [!NOTE]
> I'll assume you went through the basic syntax of reST (or Markdown) linked above. What follows are some useful mostly Sphinx-cific features. (Here are the definite [usage guide](https://www.sphinx-doc.org/en/master/usage/index.html) and [reference](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html) if you don't like my presentation style.)

#### [Roles](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html)
In reST, text within `` ` ``and`` ` `` is "interpreted"[^uninterpreted] and can be assigned a *role*: `` :role:`interpreted` ``. The default role (i.e. what is assumed if you omit `:role:`) is set by [`default_role`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-default_role) in `conf.py`. Useful roles are
- [`:math:`](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-math): LaTeX;
- [`:code:`](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-code): short single-line snippet with syntax highlighting (see the link for how to set that up);
- [cross-referencing roles](https://www.sphinx-doc.org/en/master/usage/referencing.html):
  `` :target-type:`link text <target>` ``.
  - `link text` and the angle brackets can be omitted to display the target as the link text.
  - If the target is prefixed with `~`, the link text will be only its "last part", whatever that means. In Python, this means everything after the last dot: the `name` in `module.submodule.name`.
  - Here's a list of useful `target-type`s:
    - [`:any:`](https://www.sphinx-doc.org/en/master/usage/referencing.html#role-any): will automatically figure it out from the resolved target. Even if it's externally linked with Intersphinx. Do you now see why you should set it as the [`default_role`]((https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-default_role))? End of list.
    - For other target types (you miight end up using them in some edge cases), see [here](https://www.sphinx-doc.org/en/master/usage/referencing.html).

[^uninterpreted]: If you want to include some code-like text, i.e. in a "typewriter typestyle" font, use *double* backticks: ``` ``text`` ```.

#### [Directives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html)

Directives, which look like[^indents]
```rst
.. directive:: arguments...
   :option: value
   ...
   
   content
```
are *blocks* of content. Examples (check them out in the links) include
- "[admonitions](https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions)" ([note](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-note), [warning](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-warning), [etc](https://en.wikipedia.org/wiki/ETC).),
- [images](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#images), [figures](https://docutils.sourceforge.io/docs/ref/rst/directives.html#figure), or [tables](https://docutils.sourceforge.io/docs/ref/rst/directives.html#table),
- display [math](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-math),
- [code blocks](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block),
- directives included by "[domains](#domains)".

[^indents]: White space in reST is contested territory. Three- or four-space indents usually work. Maybe you can mix them? Empty lines before/after indents?... I don't know. Use a visual reST editor (Python IDEs have one built in). Or Markdown.

#### [Domains](https://www.sphinx-doc.org/en/master/usage/domains/index.html)

Domains are just collections of extra roles and directives. The most relevant one is the [Python domain](https://www.sphinx-doc.org/en/master/usage/domains/python.html), which contains
- directives for *declaring and documenting* Python entities like [(sub)modules](https://www.sphinx-doc.org/en/master/usage/domains/python.html#directive-py-module), [functions](https://www.sphinx-doc.org/en/master/usage/domains/python.html#directive-py-function), [classes](https://www.sphinx-doc.org/en/master/usage/domains/python.html#directive-py-class), [methods](https://www.sphinx-doc.org/en/master/usage/domains/python.html#directive-py-method), [attributes](https://www.sphinx-doc.org/en/master/usage/domains/python.html#directive-py-attribute), etc. You will rarely use those because of [docs as code](#docs-as-code);
- roles for *linking to* Python entities like [(sub)modules](https://www.sphinx-doc.org/en/master/usage/domains/python.html#role-py-mod), [functions](https://www.sphinx-doc.org/en/master/usage/domains/python.html#role-py-func), [classes](https://www.sphinx-doc.org/en/master/usage/domains/python.html#role-py-class), [methods](https://www.sphinx-doc.org/en/master/usage/domains/python.html#role-py-meth), [attributes](https://www.sphinx-doc.org/en/master/usage/domains/python.html#role-py-attr), etc. You will rarely use those because of [`default_role = 'any'`](https://www.sphinx-doc.org/en/master/usage/referencing.html#role-any);
- [roles](https://www.sphinx-doc.org/en/master/usage/domains/python.html#info-field-lists) for describing signatures. You will rarely use those because of [Napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html).

#### Tricks

- [`|Substitutions|`](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#substitutions) are used as "macros" for repeatedly inserting the same content (and for including markup (formatting) inside links—reST sucks). You can put your default "shortcuts" in [`rst_prolog`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-rst_prolog) in `conf.py`.
- [`[#Footnotes]_`](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#footnotes)[^footnotes]![^footpunct]

[^footnotes]: I love them!
[^footpunct]: BTW, do you put them before or after punctuation marks?

### Documentation content

There are two classes of "documents" you might wish to include in a documentation: API docs detailing drily all your (sub)modules, functions, classes, methods, attributes, etc.; and guides that show off the exciting features you've developed and entice potential users to install your package.

Now, you can go about including content in the usual way through separate files in the docs source. Or you can adhere to the design principle of

#### Docs as code

Put your documentation next to your code, in so-called "docstrings"! I strongly recommend [Napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html): a bundled extension to Sphinx that lets/makes you write docstrings in the human-readable [NumPy](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard) or [Google](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) styles, instead of cluttered reST. Choose one, then peruse and learn from the complete examples: [NumPy](https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html#example-numpy), [Google](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google). The one you chose represents an inseparable part of these lecture notes, and thus I consider I've taught you to write documentation as code.

> [!TIP]
> Good IDEs should *help* you write docstrings. For example, PyCharm will automatically expand a `"""` that starts a class/function docstring to contain a section for the parameters/attributes (and return type if applicable) with their names and types inspected from the definition of the class/function you're documenting.

What remains is to automatically pull the docstrings out of code files and put them in the generated documentation. Two extensions can help you with that:
- [Autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc) (bundled)
  - needs to import and execute your source files, hence:
    - they have to be importable, i.e. you either need to install your package before building documentation, or add the correct directory to [`sys.path`](https://docs.python.org/3/library/sys.html#sys.path);
    - they have to be executable without serious side effects; granted you're writing API documentation, I don't expect your actual analysis, etc. code to reside in the same files as your library of functions, etc., but if it does, (move it to separate files or notebooks, but if you still don't want to, then) protect it with `if __name__ == '__main__'`;
  - by default, doesn't do anything. That is, you still need to explicitly put [`.. automodule::`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-automodule), [`.. autofunction`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autofunction), [`.. autoclass::`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autoclass), [`.. automethod`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-automethod), [`.. autoattribute`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autoattribute), etc. directives to trigger the extraction of docstrings and place them in specific locations in your documentation pages.
- [AutoAPI](https://sphinx-autoapi.readthedocs.io/en/latest/) (requires separate install)
  - performs static analysis of your code, i.e. parses the source files as pure text. You still need to tell it [where they are](https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_dirs), though;
  - by default, automatically generates standalone API docs pages from all the docstrings it finds. This can be [fine tuned](https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#customisation-options) or [disabled](https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_generate_api_docs) entirely, reverting to [autodoc-style directives](https://sphinx-autoapi.readthedocs.io/en/latest/reference/directives.html#autodoc-style-directives).

> [!NOTE]
> For completeness:
> - [`apidoc`](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html) (not an extension but rather a tool based on Autodoc) generates standalone API docs pages from all the docstrings it finds.
> - [`sphinx-autodoc2`](https://sphinx-autodoc2.readthedocs.io/en/latest/index.html), of whose existence I just learned, is, apparently, a better Auto*API*.

#### Notebooks as docs

On the other hand, user guides are supposed to demonstrate complete applications of your code and the results it generates. For this, you can (re-)use (your already existing) Jupyter notebooks via [`nbsphinx`](https://nbsphinx.readthedocs.io/). You can pre-execute the notebooks to make sure their result is as you expect (or if they take a long time or require some data/dependencies you don't want to retrieve every time you build docs), or you can have `nbsphinx` [execute them automatically](https://nbsphinx.readthedocs.io/en/latest/executing-notebooks.html). Furthermore, you can actually put API-style documentation and/or do all the usual Sphinx stuff inside [raw reST Notebook cells](https://nbsphinx.readthedocs.io/en/latest/raw-cells.html#reST). If you just want pretty formatting and (tediously explicit) links, you can still use the default Markdown text cells in notebooks, as you'd normally do. Alternatively, you might use [*raw* Markdown cells](https://nbsphinx.readthedocs.io/en/latest/raw-cells.html#Markdown), which *may* be processed by your default Markdown processor (e.g. [MyST]((https://myst-parser.readthedocs.io/en/latest/))), which *may* offer better integration with Sphinx-cific features.

> [!TIP]
> Overall, using notebooks as docs can be an equally fulfilling and/or frustrating experience. You might consider other ways of including execut(ed/able) code in your documentation, like the [`.. ipython::` directive](https://ipython.readthedocs.io/en/stable/sphinxext.html#ipython-sphinx-directive).

## Publishing on Read the Docs

[Read the Docs](https://about.readthedocs.com/) is (something you should do before asking questions or raising issues, but also) a website[^rtfd] / service that can automatically build and then host your documentation online.

If you already have a simple documented project with a public online repo[^exercise], [getting it on RTD](https://docs.readthedocs.io/en/stable/intro/import-guide.html) is as simple[^simple] as registering for an account, linking your e.g. GitHub, importing the repo and waiting a bit.

[^rtfd]: sometimes abbreviated as [RTFD.io](https://rtfd.io)) ¯\_(ツ)_/¯
[^exercise]: Third warning for the exercise session.
[^simple]: [slightly more complicated](https://blog.readthedocs.com/migrate-configuration-v2/) since September 2023. You might want to import your project now or wait until you've read about [`readthedocs.yaml`](#configuring-the-build), which is now required.

### Configuring the build

Building documentation is straightforward since it usually only requires Python and Sphinx, which RTD, of course, already has. Still, you *must* include a  [`.readthedocs.yaml`](https://docs.readthedocs.io/en/stable/config-file/v2.html) YAML file (check out the simple [template](https://docs.readthedocs.io/en/stable/config-file/index.html#getting-started-with-a-template)) in your project that details the build process. It should specify, at least:
- [`sphinx.configuration`](https://docs.readthedocs.io/en/stable/config-file/v2.html#sphinx-configuration): the path to the Sphinx `conf.py` file;
- [`build.tools.os`](https://docs.readthedocs.io/en/stable/config-file/v2.html#build-os), [`build.tools.python`](https://docs.readthedocs.io/en/stable/config-file/v2.html#build-tools-python): the environment used for building the docs; the specifics are only relevant if you're installing/importing your package and it requires a certain Python version.

That should be enough for a simple project. But not yours! By that, I mean any project whose documentation somehow inspects the code (i.e. for fetching the version and/or extracting docstrings) or uses non-bundled Sphinx extensions; i.e. any modern software project. In that case, you'll need[^need] to install your package and its (docs-related and/or not) dependencies.
- [`python.install`](https://docs.readthedocs.io/en/stable/config-file/v2.html#python-install) in `.readthedocs.yaml` specifies how to do this. I strongly suggest
  ```yaml
  python:
    install:
      - method: pip
        path: .
        extra_requirements:
          - docs
  ```
  This will basically run `pip install .[docs]` in RTD's build environment, which will automatically install your project's dependencies, including the [optional dependencies](https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#optional-dependencies) grouped under "`docs`" (see the lecture on distributing Python packages): here you should put Sphinx and all the extensions you use.

Alternatively (or in addition), if you really know what you're doing,
- [`python.install.requirements`](https://docs.readthedocs.io/en/stable/config-file/v2.html#requirements-file) can be used to specify one or many [Pip requirements file(s)](https://pip.pypa.io/en/stable/reference/requirements-file-format/) containing dependencies. This can be used as a complement to `pip install`ing your own package as described above (maybe you can use [`--no-deps`](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-no-deps)) and/or list the documentation-specific dependencies in a docs-specific requirements file.

Or, if you need it for some reason:
- [`conda`](https://docs.readthedocs.io/en/stable/config-file/v2.html#conda).

> [!WARNING]
> Remember, in any case, that if you're using Autodoc, your sources will be executed—and that includes any global `import` statements, so you need to install all packages thus imported! This does not apply if you're using a static AutoAPI builder.

[^need]: you may be able to hack your way around this, but honestly, it's easier to set it up properly. This may also help you uncover bugs in the way you [include files in source distributions](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#package-discovery) (talking from experience here).

### Perks of RTD

Read the Docs has a handful of features advanced users might consider neat. For starters, [their theme](https://sphinx-rtd-theme.readthedocs.io/en/stable/) is pretty nice; but you're in no way obligated to use it (remember, though, to install it in the `.readthedocs.yaml` build environment...). They can also host separate versions of the documentation simultaneously, e.g. if you're working on new features alongside a stable released version, or simply for historical reasons. Their service is also free of charge, as long as you swear by open source.
