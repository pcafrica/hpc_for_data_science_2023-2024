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

[^system]: [Modern tools](#tensorboard-and-wb) can log system information automatically behind the scenes.


## PyTorch Lightning

It's the 2020s, and you don't need to write your own training loop and/or zero your own gradients[^loop]. [(PyTorch) Lightning](https://lightning.ai/docs/pytorch/stable/) can do this for you.

[^loop]: unless you are *developing*/*studying* the dark magic of deep learning instead of simply practicing it

`pytorch_lightning` is a utilitiies library that automates the tedious (software) engineering tasks that previously represented a high barrier to entry of scientists into high-performance deep learning. I'm talking zero to multi-node multi-GPU training in two exercise sessions.

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

- [`training_step(self, batch, ...)`](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#training-step): run your network or do whatever else it takes to compute the loss value for a *batch* of inputs. Usually, the `batch` is a tuple `(inputs, targets)` (targets can be the labels for classification or response variables for regression), but you're fully in control through the [data loader](#lightning-data-loader-module).
  
  The forward pass is usually implemented in a `forward(self, inputs)` method. Inside `training_step`, you'd call `output = self.forward(inputs)`, then compare it with the `targets` through a loss function

### Lightning Data Loader (Module)


## Tensorboard and W&B

It's the 2020s, and you don't need to print out the progress of your training yourself.
