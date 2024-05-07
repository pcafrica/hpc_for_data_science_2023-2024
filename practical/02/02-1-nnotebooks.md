# Neural Networks and Notebooks

## Access to GPUs

- Option(s) 1: the easy way.
  - Your laptop or office workstation may already have a GPU (in this case, make sure you've installed the necessary [Nvidia drivers](https://www.nvidia.com/download/index.aspx)).
  - Your boss may already have money to buy you one.
  - Your department may already have [*shared* remote workstations](#workstations). These differ from a compute cluster by the looser access rules, i.e. the absence of a queuing system, which is expected to be replaced by considerate usage patterns and polite communication.

  A setup like this will be adequate for development and testing and hopefully for some light production work.

> [!IMPORTANT]
> <a name="workstations"></a>TSDS members are requested to familiarise themselves with the available resources and the accompanying usage policy! described in [the dedicated wiki](https://git-scm.sissa.it/sissa-tsds/hpc-wiki/-/wikis/servers) (login required).

- Option 2: [Google Colab](https://colab.research.google.com) used to be really great; nowadays, it's cool at best, but it still provides free intermittent access to a GPU, about 50 GB of scratch storage, and a decent software stack out of the box. If I didn't have option 1, or I wanted to easily set up a Notebook environment for interactive development/testing, or share some quick code snippets that only make use of publically installable libraries, I can see myself using Colab. For serious research, though, you'll probably need to pay.

- Option 3: the big boys (HPC clusters). SISSA people have access to two tiers of compute clusters
  - [Ulysses](https://www.itcs.sissa.it/services/computing/hpc) (see also the great ~~fanfic~~ [unofficial docs](https://ulysses.readthedocs.io/); and by "see" I mean, "you are requested to see") is SISSA's on-premises cluster.[^exhausts] It is *decent*. It is managed by slurm but has no budget limits. Its networking is disastrous:[^network] sometimes, it takes two minutes to `import torch` because the user's home directories are on a non-local partition...
  - [Cineca](https://www.hpc.cineca.it/user-support/documentation/) (talk to your supervisor for access) is a collection of supercomputers. Specifically relevant is [Leonardo](https://wiki.u-gov.it/confluence/display/SCAIUS/UG3.2%3A+LEONARDO+UserGuide) with its ~3500 nodes with 4x A100-64GB GPUs each.[^madness]

- Bonus option: commercial compute providers (aka compute clouds) are as abundant as silicon. See [e.g. this blog post](https://www.paperspace.com/gpu-cloud-comparison) for a comparison and links. They, as long as services like [Huggingface](https://huggingface.co/) may be good options for sharing your results interactively or letting others use your trained models.

[^exhausts]: Who's in for a field trip to the giant heat exhausts/evaporators beyond the garden?

[^network]: Stay in SISSA long enough, and you'll get accustomed to the gentle background hum of "Ulysses network problem" emails...

[^madness]: I've seen users occupy *thousands* of GPUs at the same time...

Once you've got your hands on the hardware, you can verify it is accessible via
```shell
nvidia-smi
```
which will list the available GPU(s), their parameters (chiefly memory) and utilisation (allocated/free memory and power usage, which is proportiotal to how much computation you're squeezing out of the GPU). It is a good habit to check `nvidia-smi` while your code is running to verify the GPU is being used and how much memory/compute you're using.[^system]

[^system]: [Modern tools](#weights-and-biases) can log system information automatically behind the scenes.


## PyTorch Lightning

It's the 2020s, and you don't need to write your own training loop and/or zero your own gradients[^loop]. [(PyTorch) Lightning](https://lightning.ai/docs/pytorch/stable/) can do this for you.

[^loop]: unless you are *developing*/*studying* the dark magic of deep learning instead of simply practicing it

`pytorch_lightning` is a utilitiies library that automates the tedious (software) engineering tasks that previously represented a high barrier to entry of scientists into high-performance deep learning. I'm talking zero to multi-node multi-GPU training in two exercise sessions.

Lightning automates the following procedure: you provide it with a model and a data loader and it
- puts your model on the "best" device on your system (it detects GPUs automatically)
- starts your training loop:
  - calls `.train()` on your model
  - iterates your [training data loader](#train-dataloader)
    - zeros gradients
    - gets a new batch and puts it on the model device
    - calls `model.training_step(batch)` (you fill this in, see [below](#training-step)) to calculate the loss
    - calculates gradients from the loss
    - runs an optimizer step
- from time to time (e.g. every epoch), runs a validation loop
  - calls `.eval()` on your model
  - iterates your [validation data loader](#val-dataloader)
    - gets a new batch and puts it on the model device
    - calls `model.validation_step(batch)` (you fill this in, see [below](#validation-step)) to calculate the loss

Lightning has two major components that you should get right from the start, in order to enjoy all its benefits.

### [Lightning Module](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html)

Your neural network module should be a subclass of `LightningModule`. You then need the following methods
- `__init__(self, ...)`: put whatever *hyperparameters* determine the structure of your network—e.g. number of layers, sizes of layers, type of non-linearity—as parameters to `__init__`. These will then be logged ([see here](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#save-hyperparameters)), so you can keep track of what configurations work best. Inside `__init__`, you should initialise your network components as usual.
- [`configure_optimizers(self)`](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#configure-optimizers): create the optimisers and pass them the parameters of the module. This is usually as simple as
  ```python
  def configure_optimizers(self):
      return Adam(self.parameters(), lr=self.lr)
  ```
  (note that the learning rate has to be passed e.g. through `__init__`: it is, indeed, a hyperparameter). However, one can also return a more complicated `{'optimizer': optim, 'lr_scheduler': sched}` dictionary to enable [learning rate scheduling](https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate)[^sched].

[^sched]: I've heard this makes or breaks transformer training.

> [!TIP]
> For advanced—or simply adventurous—users, Lightning has a [`Tuner`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.tuner.tuning.Tuner.html) class that can automatically find a good learning rate: see [here](https://lightning.ai/docs/pytorch/stable/advanced/training_tricks.html#learning-rate-finder) for usage.

- <a name="training-step"></a>[`training_step(self, batch, ...)`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.training_step): run your network or do whatever else it takes to compute the loss value for a *batch* of inputs. Usually, the `batch` is a tuple `(inputs, targets)` (targets can be the labels for classification or response variables for regression), but you're fully in control through the [data loader](#lightning-data).
  
  The forward pass is usually implemented in a `forward(self, inputs)` method. Its contents depend on the NN architecture. Instead, in the simplest case, your `training_step` will look like 
  ```python
  def training_step(self, batch, *args, **kwargs):
      inputs, targets = batch
      outputs = self.forward(inputs)
      return self.loss(outputs, targets)
  ```
- <a name="validation-step"></a>[`validation_step(self, batch, ...)`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.validation_step) is not *required* but you *should* have one to implement validation checks on held-out data. In the simplest scenario, this can be exactly the same as the [`training_step`](#training-step); in this case, you can just do
  ```python
  validation_step = training_step
  ```

### [Lightning Data](https://lightning.ai/docs/pytorch/stable/data/datamodule.html)

While Lightning can work with ~any data loader[^torch-data], it's a good idea to structure your data in a [`LightningDataModule`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningDataModule.html#lightning.pytorch.core.LightningDataModule): this will be of great help when moving your training to different machines or scaling it to multiple accelerators. A Lightning Data Module encapsulates:
- data download: e.g. if your compute nodes don't have access to shared filesystems or you want to move stuff to faster memory;
- data preparation: e.g. constructing a [transform / augmentation pipeline](https://pytorch.org/vision/stable/transforms.html);
- splitting data into training and validation;
- creating the actual loaders: these should be iterables that return batches of example inputs (and corresponding targets for supervised learning):
  - <a name="train-dataloader"></a>[`train_dataloader(self)`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.train_dataloader): implement this to return a torch [`DataLoader`]() that will be iterated and its batches fed directly (after being [transferred to the relvant device](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.transfer_batch_to_device)) into [`training_step`](#training-step);
  - <a name="val-dataloader"></a>[`val_dataloader(self)`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.val_dataloader): the same as [`train_dataloader`](#train-dataloader) but for validation batches to be fed to [`validation_step`](#validation-step).

[^torch-data]: The reader is strongly advised to familiarise themselves with the PyTorch documentation on data loading ([`torch.utils.data`](https://pytorch.org/docs/stable/data.html)). Curious/Advanced users should also consider the extension [`torchdata`](https://pytorch.org/data/beta/index.html).

#### Data loading (for distributed training)

> [!TIP]
> Following best practices for distributed training will also improve your single-device experience!

You will soon transition to distributed training for the fun and high performance of it. The most crucial aspect of setting that up is actually the data loading: since you need to ensure you are loading data on the appropriate machines and exactly partitioning your training and validation sets among the devices/processes (without repetitions or missing examples).

The recommended (by me) strategy is to use [map-style data sets](https://pytorch.org/docs/stable/data.html#map-style-datasets), from which individual examples are accessible by `dataset[i]`, and simply wrap them in a [`DataLoader`](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader). This will be enough for PyTorch+Lightning to automatically
- shuffle examples (differently every epoch),
- compile examples into batches,
- partition batches among the different processes/devices.

Note that usually *all* the data should be loaded in each process, allowing Lightning to just swap in a custom [`Distributed`](https://pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler)[`Sampler`](https://pytorch.org/docs/stable/data.html#torch.utils.data.Sampler) that iterates through disjoint subsets in each process. In this context, it is important to understand the difference between:
- [`prepare_data(self)`](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#prepare-data): runs only *once* in distributed training (or once *per node* if [`prepare_data_per_node`](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#prepare-data-per-node) is set). This is meant for downloading data.
- [`setup(self)`](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#setup): runs in every process. The majority of things you do to your data should probably be defined here.

> [!IMPORTANT]
> Always set `prepare_data_per_node`, even if it's false, otherwise distributed initialisation may fail.

### [Lightning Trainer](https://lightning.ai/docs/pytorch/stable/common/trainer.html)

A Lightning Trainer... um... trains... and much more! your model. It's the component that implements most of Lightning's automations. To train a [Lightning Module](#lightning-module) on some [Lightning Data](#lightning-data):
```python
trainer = Trainer(...)
trainer.fit(model, datamod)
```
Now sit back and enjoy the show.

#### Trainer flags

The [`...`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#trainer-flags) above can be useful (and/or essential) configuration like
- nothing, lol, Lighting will pick sensible defaults for everything;
- [`accelerator`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#accelerator), [`devices`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#devices): e.g. `'gpu'` and `1`; but Lightning will usually automatically recognise the number and type of devices you have; note that for >1 device you'll probably need some further setup/thought, so it might be a good idea to explicitly set `devices=1`; along this line of thought
  - [`num_nodes`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#num-nodes): multi-node training will be discussed later;
- [`max_epochs`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#max-epochs), [`max_steps`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#max-steps): how long to train; note that a "step" is of the optimiser, not simply one forward pass (relevant for [`accumulate_grad_batches`](#accumulate-grad-batches));
  - [`max_time`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#max-time) if you like absolute terms;
- <a name="accumulate-grad-batches"></a>[`accumulate_grad_batches`](https://lightning.ai/docs/pytorch/stable/advanced/training_tricks.html#accumulate-gradients): sometimes, a single batch[^oom] does not fit in GPU memory. In that case, you should reduce the batch size produced by your loaders and accumulate gradients from a few of these smaller batches. This is basically replaces parallel evaluation with a sequential for loop;
- [`logger`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#logger): see [below](#logging-tensorboard-and-wb). Note that Lightning will automatically set up a [`TensorboardLogger`](https://lightning.ai/docs/pytorch/stable/extensions/generated/lightning.pytorch.loggers.TensorBoardLogger.html), which you can disable by `logger=False`;
- [`callbacks`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#callbacks): see [below](#callbacks). Note that Lightning will automatically include some callbacks by default, which you may want to disable in some cases through
  - [`enable_checkpointing`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#enable-checkpointing) (yes, by default); [customise checkpointing](https://lightning.ai/docs/pytorch/stable/common/checkpointing_intermediate.html) by providing an explicit [`ModelCheckpoint`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint) callback (see [below](#checkpointing));
  - [`enable_progress_bar`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#enable-progress-bar) (yes, by default); [customise progress-barring](https://lightning.ai/docs/pytorch/stable/common/progress_bar.html) by providing an explicit [`ProgressBar`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ProgressBar.html#lightning.pytorch.callbacks.ProgressBar)-derived callback;
- how often to run the validation loop:
  - [`val_check_interval`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#val-check-interval):
    - a float ∈ [0, 1]: fraction of the training epoch, or
    - an integer: number of training batches;
  - [`check_val_every_n_epoch`](https://lightning.ai/docs/pytorch/stable/common/trainer.html#check-val-every-n-epoch);
  
  The most sensible (and default) setting is simply `check_val_every_n_epoch=1`, unless you're doing something funky. Note that it can be a useful strategy to define various callbacks (e.g. checkpointing!) to run [`on_validation_end`](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#on-validation-end) so that you can control them collectively from the settings here;
- and [more](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer).

[^oom]: Usually, the batch itself is small, but evaluating a big network on it is what takes up the lot of memory.

### [Callbacks](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html)

Lightning boasts giving the user the ability to patch into training at any point through an extensive [list of *hooks*](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#hooks) that can be defined[^self] on a [`Callback`] subclass, instances of which can be given in a list to the [Trainer](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html)'s [`callbacks` flag](https://lightning.ai/docs/pytorch/stable/common/trainer.html#callbacks).

Here are some important/useful hooks:
- [`on_fit_start(trainer, model)`](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#on-fit-start),
  [`on_fit_end(trainer, model)`](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#on-fit-end): 
  called when you call `Trainer.fit` and before it returns; useful for registering various components needed in callbacks;
- [`on_train_batch_start(trainer, model, batch, ...)`](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#on-train-batch-start),
  [`on_train_batch_end(trainer, model, outputs, batch, ...)`](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#on-train-batch-end):
  called before and after [`training_step`](#training-step) (the outputs are the calculated loss and anything else returned by `training_step`, possibly [accumulated over batches](#accumulate-grad-batches));
- [`on_validation_batch_start(trainer, model, batch, ...)`](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#on-validation-batch-start),
  [`on_validation_batch_end(trainer, model, outputs, batch, ...)`](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#on-validation-batch-end):
  same but for validation batches; you can use this to store all validation outputs if you want to aggregate / display them in some custom way;
- [`on_validation_start(trainer, model)`](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#on-validation-start),
  [`on_validation_end(trainer, model)`](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#on-validation-end):
  I suggest the latter for running custom progress visualisations, e.g. using the saved validation outputs.

[^self]: Signatures shown below are how the methods will be called. When defining them in a [Callback](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.Callback.html#lightning.pytorch.callbacks.Callback), remember the `self` argument as well.

Lightning also comes with a range of [builtin callbacks](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html#built-in-callbacks), some of which we will discuss in more detail below; a random selection from the rest is:
- [`EarlyStopping`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.EarlyStopping.html#lightning.pytorch.callbacks.EarlyStopping): for not wasting time once the validation loss stops improving;
- [`LearningRateMonitor`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.LearningRateMonitor.html#lightning.pytorch.callbacks.LearningRateMonitor): for monitoring a learning-rate schedule.

#### [Checkpointing](https://lightning.ai/docs/pytorch/stable/common/checkpointing.html)

You should periodically save your progress while training in order to ensure:
- you can resume in case something bad happens (e.g. you run out of computing time or your network hits its head and forgets everything it had learned...) or in case you eventually want to train more than you initially thought;
- you can retrieve the best performing (generalising) version of your network in case you overfit it.

By default, Lightning sets up checkpointing at the end of every epoch and keeps only *the last one*. This can be modified in terms of:
- frequency:
[`every_n_train_steps`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint.params.every_n_train_steps),
[`every_n_epochs`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint.params.every_n_epochs),
or [`train_time_interval`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint.params.train_time_interval);
- retention:
  - [`save_top_k`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint.params.save_top_k): can be set to a specific number or -1 to keep all checkpoints,
  - [`monitor`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint.params.monitor) a specific [logged](#logging) value and keep checkpoints based on performance ("top") with respect to it; you can also change the monitoring
    - [`mode`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint.params.mode): one of `'min'` or `'max'`;[^top]
  - convenience: [`save_last`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint.params.monitor) to save a *last* checkpoint regardless; useful for [resuming training](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.fit.params.ckpt_path), but maybe you want to restart from the *best* checkpoint instead...

To [load a network from a checkpoint](https://lightning.ai/docs/pytorch/stable/common/checkpointing_basic.html#lightningmodule-from-checkpoint), you should be able to use the [`MyLightningModel.load_from_checkpoint(ckpt_path)`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.load_from_checkpoint) *class*method, but you can also simply [`torch.load(ckpt_path)`](https://pytorch.org/docs/stable/generated/torch.load.html), inspect the checkpoint's contents, and do whatever you want with them.
If you're wondering *which* checkpoint to load, after training, you can use the `ModelCheckpoint`'s `.best_model_path` or `.best_k_models` properties.

[^top]: Fun story, by default, `mode` is `'min'`, so "top" is actually "bottom".

#### [Logging](https://lightning.ai/docs/pytorch/stable/extensions/logging.html#logging)

It's the 2020s, and you don't need to print out the progress of your training yourself!

For starters, Lightning automatically shows you a [`tqdm`](https://github.com/tqdm/tqdm) [progress bar](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.TQDMProgressBar.html) displaying the current step and epoch (and the progress within the epoch) and the loss value, alongside any other scalar/numerical values you may have logged through 
- [`LightningModule.log(name, value, *args, **kwargs)`](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#log) or [`LightningModule.log_dict(dictionary, *args, **kwargs)`](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#log_dict):
  
  you can call this from within [`training_step`](#training-step) or [`validation_step`](#validation-step) or any callback/model hook. Lightning will then determine what is sensible to do via [some complicate logic that you should read about](https://lightning.ai/docs/pytorch/stable/extensions/logging.html#automatic-logging). Possibilities include reporting values on the progress bar and/or logger(s), or saving and reporting/logging them only at the end of an epoch.

The simplest usage pattern (that already gets you pretty far in terms of logging) is to
```python
self.log('train loss', loss)
```
from within [`training_step`](#training-step) and
```python
self.log('val loss', loss)
```
from within [`validation_step`](#validation-step).

From within callbacks, you can also "log" (save) non-numerical values like images, figures, weights and biases histograms, tables of network predictions, etc. by making use of custom loggers. The most famous one is

##### [Tensorboard](https://www.tensorflow.org/tensorboard/)

[Tensorboard](https://pypi.org/project/tensorboard/) is a package that provides a web application for monitoring machine learning experiments. After installing it (e.g. via Pip), you can start a server via
```shell
tensorboard --logdir LOGDIR
```
(folders within `LOGDIR` will then represent different *experiment versions*). You can now open a browser, point it to [` http://localhost:6006/`](http://localhost:6006/), and explore. But your exploration will probably be quite short before you've logged some data.

Tensorboard was originally developed by PyTorch's rival, TensorFlow, but its `SummaryWriter` has been [ported](https://pytorch.org/docs/stable/tensorboard.html#torch.utils.tensorboard.writer.SummaryWriter) to—and included by default with—PyTorch. Moreover, Lightning *automatically* installs a [`TensorboardLogger`](https://lightning.ai/docs/pytorch/stable/extensions/generated/lightning.pytorch.loggers.TensorBoardLogger.html#lightning.pytorch.loggers.TensorBoardLogger) if one is not provided to the trainer (or logging disabled through `logger=False`), so it literally takes *near-zero effort* on the user's part to have training / validation losses logged to Tensorboard.

If you want to ["manually log scalar artifacts"](https://lightning.ai/docs/pytorch/stable/extensions/logging.html#manual-logging-non-scalar-artifacts) from callbacks, you can access the raw [`SummaryWriter`](https://pytorch.org/docs/stable/tensorboard.html#torch.utils.tensorboard.writer.SummaryWriter) through a model/trainer's [`.logger`](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#logger)[`.experiment`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.loggers.logger.html#lightning.pytorch.loggers.logger.DummyLogger.experiment) property and then use the relevant `.add_*` methods, as described in the documentation.

##### [Weights and Biases](https://wandb.ai/)

Tensorboard is cool, but it has to be run locally. Wouldn't it be cooler, if you could monitor the progress of your machine learning experiment on your phone *from Barcola*!?

Weights and Biases is a service that can host your Tensorboard-and-beyond logs online and display them in a web[^web] browser in beautiful and customisable ways. The first step to enabling it is registering for an account on [wandb.ai](https://wandb.ai/). Then you need to install the [Python package](https://pypi.org/project/wandb/). Finally, add *two lines of code* before your Lightning-powered network training code:
```python
import wandb

wandb.init(project=..., name=..., sync_tensorboard=True, ...)
```
(See [`wandb.init`'s docs](https://docs.wandb.ai/ref/python/init) for what you can put instead of the `...`.)
Once you've finished training, don't forget to call [`wandb.finish()`](https://docs.wandb.ai/ref/python/finish): otherwise, your computer will get full of `wandb-service` zombie processes!

See if this works for you: it should get you pretty far. Of course, there's a world of customisation options: for example, you can directly use a [`WandbLogger`](https://lightning.ai/docs/pytorch/stable/extensions/generated/lightning.pytorch.loggers.WandbLogger.html#lightning.pytorch.loggers.WandbLogger) (see [here](https://docs.wandb.ai/guides/integrations/lightning) for a tutorial), bypassing TensorBoard.

[^web]: for real this time
