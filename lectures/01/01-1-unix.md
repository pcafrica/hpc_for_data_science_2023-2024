# Unix and the command line

Unix is an operating system that is commonly operated from a "command line": that is, by sending textual commands[^1] (but in fact, the commands themselves are executable programs[^2]). Here is a useful one:

[^1]: Life is easiest if you are using a graphical user interface (or "desktop environment"). You probably have one on your laptop Linux: it allows you to do all of the below by pointing and clicking. Sometimes, but not always, you might have this luxury on powerful remote machines or clusters: in that case, consider yourself truly blessed and free to skip this section.

[^2]: In fact, the "command line" is just an interpreter of a variant of the [shell script](https://en.wikipedia.org/wiki/Shell_script) programming language. The default "shell" is usually [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)). Shell commands can also be read and executed from a (shell script) file, usually with extension `.sh`. One can write *any* program, e.g. a neural network, in the shell: just ask ChatGPT (and skip through the initial complaints about how stupid this request is). But real programming is better left to a nicer language.

* `man COMMAND`: user "manual" for `COMMAND`. Type this to get help on the usage of `COMMAND` and the arguments it accepts. Alternatively
    * `COMMAND -h/--help` *might*—but is not guaranteed to—produce similar (usually more condensed) results.
  
  At this point it might be time to note that "switches" to commands are usually indicated by a single dash followed by a single letter (`-h`) or two dashes and a longer/full name (`--help`). The former can be combined without repeating the `-`: see `ls -al` below. Some switches might take arguments; some arguments might be given without switches; the only way to learn is by example, so read on. Oh, and capitalised words in examples/manuals are usually intended to be *replaced* by specific instances.

The first thing you'd want to do when you log in to a Unix shell is find where you are
* `pwd`: print working directory (the folder "we're currently in")

and maybe go somewhere else:
* `cd PATH`: change directory.

In a `PATH`:
* a single `.` indicates "this" directory; so `.` is the working directory, but `some/other/./directory` is the same as `some/other/directory`;
* a double `..` is the "parent" directory: `..` is the parent of the workdir, but `some/other/../directory` is the same as `some/directory` (the `..` is the parent of `some/other`);
* a path starting with `/` is relative to the "root" of the filesystem; instead, a path not starting with `/` is relative to the working directory;

The shell also supports a number of *expansion* / *glob* patterns[^glob] in paths:
* `~` expands to the user's home directory;
* `*` expands to a sequence of any number of any characters in a file/folder name, except an initial `.`;
* `?`: likewise but for a single character;
* `**` can be used to represent any number of nested directories.

[^glob]: To use them in Python, see [os.path.expanduser()](https://docs.python.org/3/library/os.path.html#os.path.expanduser) and [glob](https://docs.python.org/3/library/glob.html).

What is there in a directory?
* `ls PATH`: list (directories and files within `PATH` (`.` by default));
    * `ls -l`: list with more info,
    * `ls -a`: list all entries (by default, those starting with `.` (including, but not limited to `.` and `..` (yes, `.` and `..`, technically, are special entries within every directory)) are ignored).
* `mkdir NAME`: make directory named `NAME`. If you give the `-p` switch, `NAME` can contain a sequence of parents like `some/other/name`.
* `mv SOURCE DEST`: move, aka *rename*, `SOURCE` as `DEST` (including, obviously, everything whinin it if it's a directory).
* `cp SOURCE DEST`: copy `SOURCE` to `DEST`. Now, if `DEST` exists, it'd better be a directory, in which `SOURCE` (just the last part if it's `a/hierarchy/of/names`) will be placed. If it doesn't exist, it will be the name/path of the new copy.
* `ln [-s] SOURCE DEST`: link: a powerful Unix-specific-ish tool like Windows' "shortcut". Its most useful form, `ln -s` creates a "symbolic" link: a file/folder that just points to another by name. Note that the `DEST` is relative to the `SOURCE`('s directory), so better use absolute paths, or `cd` into the `SOURCE`'s directory first.
    * useful example: your working directory (with all your code) is on a small shared and backed-up drive accessible from many machines. However, you want to save/load vast amounts of meaningful data, which you store on a big local scratch drive, say in `/scratch/USER/data`. You can `ln -s /scratch/USER/data .` to make a shortcut within your working directory: no copies are made, and you need to try hard to realise that `./data` is on an entirely different drive (`ls -l` will tell you if some entries are symbolic links and where they point to).

Speaking of large amounts of data,
* `df [-h] PATH`: disk free: how much free space is there on the filesystem of `PATH`; the `-h` makes it "human-readable", i.e. in kilo/mega/giga bytes instead of... something arbitrary (usually just bytes).
* `du [-a] [-h] [-dN] PATH`: disk usage: list size of folders (and files if `-a` is switched) within `PATH`. Again, `-h` makes the output "human-readable". The `-d` switch, which takes an argument (no space) N=depth, limits the recursive printing to a depth of N; results are still aggregated, though!
    * `du -ahd1 | sort -h` will list entries in the working dir sorted by their size!
    * `du` might take a while, since it walks and aggregates the directory tree in any case.

If you want to track/hunt down running programs:
* `top [-u USER]`: something like an interactive comman-line task manager (well, just viewer). `-u USER` to display processes by a specific user. Usually, the `%CPU` displayed is in per cent of one core—so can be >100. Press `e` to cycle through units of memory (RAM: look at the `RES` column) or `q` to quit. For a simpler non-interactive output
* `ps -u USER` will give you a static list of `USER`'s running programs. You can then use the listed `PID`s to
* `kill PID` an unresponsive (or just naughty) program. If this doesn't work, try [`kill -9 PID`](https://unix.stackexchange.com/questions/317492/list-of-kill-signals#comment558131_317496). You can also kill by name with
* `killall NAME`. I don't think you can kill another user's programs, though.

Speaking of computing resources:
* `sbatch`, `salloc`, `srun`, `scancel`, `squeue`, `sinfo`: commands to interact with the [SLURM](https://futurama.fandom.com/wiki/Slurm) [cluster workload manager](https://slurm.schedmd.com/documentation.html), which will be described later.

Here are a few other tips and tricks:
- `cat FILE [FILE2 ...]` to just display one or many files;
- `tail -f FILE` to monitor a file that is being continuously updated (e.g. the redirected output of a script);
- `history` will show you your previous commands. In a command, `!N` is replaced by the `N`th command from history, so you can easily re-run it; `!!` is replaced by the last command;
- `grep PATTERN FILE` can be used to filter `FILE` for lines [containing `PATTERN`](https://phoenixnap.com/kb/grep-regex)—or the output of other commands, if used with a [pipe](https://www.geeksforgeeks.org/piping-in-unix-or-linux/): `COMMAND | grep ...`;
- `nohup COMMAND ... > OUTPUT_FILE &` to run a process in the background (the `&` at the end is important) so that it isn't terminated when you [hang up](https://www.youtube.com/watch?v=EDwb9jOVRtU) (log out / exit the terminal). The output is redirected to `OUTPUT_FILE`. The enthusiasts are invited to explore [more complicated patterns](https://www.redhat.com/sysadmin/redirect-shell-command-script-output) to e.g. separate `stdout` and `stderr` into different files.
- to interrupt a running program: `Ctrl+c`;
- to end a Unix session: `exit`, `logout`, or `Ctrl+d` (`EOF`: end-of-file);
- to learn more, Google `unix WHAT_I_WANT_TO_DO`.

### Environment variables

Environment variables are a means for programs (or the user) to communicate with other programs. They store—usually small—pieces of textual information, which can be accessed with a `$` prefix: `$ENVVAR`. (Remember to *do* something with the value of `ENVVAR` thus recalled. I.e. `cd $HOME` or `echo $PATH`, otherwise, the shell will try to parse `ENVVAR`'s contents as a regular command (and probably—hopefully harmlessly—fail).) To set an environment variable,
* `export ENVVAR=VALUE`; the `export` part makes it available in other programs started in the current session. Want to "always" set some environment variable (e.g. where your code is stored)? Set it in `~/.bashrc`.

In Python, environment variables can be accessed and manipulated through [`os.environ`](https://docs.python.org/3/library/os.html#os.environ).

Here are some important environment variables:
- `HOME`: the "home/user" directory of the current user;
- `PATH`: the collection of folders where the shell searches for executables. This is relevant when you install packages and will usually be managed by a package manager;
- `PYTHONPATH`: the collection of folders where Python looks for importable packages (in addition to the current working directory and defaults);
- `SLURM_...`: [define](https://slurm.schedmd.com/sbatch.html#SECTION_INPUT-ENVIRONMENT-VARIABLES) / [describe](https://slurm.schedmd.com/sbatch.html#SECTION_OUTPUT-ENVIRONMENT-VARIABLES) the distributed computing environment of a SLURM job (will be discussed later).
