# UI2code
UI2code is a tool to convert the UI design image into the skeleton code with deep learning methods.
For example, given an input of Android UI design image, it can generate the corresponding Android XML skeleton code to developers. And developers just need to fill in some detailed attributes such as color, text.
We believe that this tool can assist the front-end mobile developers to implement the UI design image from designers.
Some brief introduction can be seen in http://tagreorder.appspot.com/ui2code.html

# Paper
We have published this work in our ICSE'18 paper:

    From UI Design Image to GUI Skeleton: A Neural Machine Translator to Bootstrap Mobile GUI Implementation
    Chunyang Chen, Ting Su, Guozhu Meng, Zhenchang Xing, Yang Liu
    The 40th International Conference on Software Engineering, Gothenburg, Sweden.
    http://ccywch.github.io/chenchunyang.github.io/publication/ui2code.pdf


# Dataset
We adopt the UI testing to explore more than 5000 Android Apps crawled from the Google Play, and then take the screenshots as the UI design image and also collect the corresponding code.
There are totally 29,887 screenshots (We have resize it as 300 * 200 and rotate them 90 degree for training), and corresponding source code.
It can be downloaded in https://drive.google.com/open?id=17cRSdNPd7GoNuirE983S467kWbOLtiuw and decompressed it for using.

We use an automated GUI testing tool for android apps, named [Stoat](https://tingsu.github.io/files/stoat.html), to fully-automatically collect UI dataset. Stoat is easy and open to use. 

# Prerequsites
The project is written in [Torch](http://torch.ch), and the evaluation needs Python.

### Torch

#### Model

The following lua libraries are required for the main model.

* tds
* class 
* nn
* nngraph
* cunn
* cudnn
* cutorch

Note that currently it can only run in **GPU**

##### Perl

Perl is used for evaluating BLEU score.


# Usage

## Data

We have prepared the dataset for training, validation and testing.
so we need to specify a `data_base_dir` storing the images, a `label_path` storing all labels (e.g., code sequence). Besides, we need to specify a `data_path` for the training (or test) data samples. The format of `data_path` shall look like:

```
<img_name1> <label_idx1>
<img_name2> <label_idx2>
<img_name3> <label_idx3>
...
```
where `<label_idx>` denotes the line index of the label (starting from 0).
We have stored our trained model in https://drive.google.com/open?id=10vStYFIwA2ofXSzaUWA4JSw69XH6U3b6, training data as `train.lst`, validation data as `validate.lst`, testing data as `test_shuffle.lst`.
The raw image data is in `processedImage`, and all code data in `XMLsequence.txt` with the vocabulary as `xml_vocab.txt`.

## Train the Model

You can train the model with the following order:
```
th src/train.lua
-phase train -gpu_id 1
-model_dir model 
-input_feed -prealloc 
-data_base_dir data/processedImage/
-data_path data/train.lst
-val_data_path data/validate.lst
-label_path data/XMLsequence.lst
-vocab_file data/xml_vocab.txt
-max_num_tokens 100 -max_image_width 300 -max_image_height 200 
-batch_size 20 
-beam_size 5
-dropout 0.2
-num_epochs 10
```
In the default setting, the log file will be put to `log.txt`. The log file records the training and validation perplexities. `model_dir` speicifies where the models should be saved. Please fine-tune the parameter for your own purpose.

## Test the Model

After training, you can load a model and use it to test on test dataset. We provide a model trained on the our data which can be downloaded together with the dataset in xxx

Now you can load the model and test on test set. Note that in order to output the predictions, a flag `-visualize` must be set.
You can use the following order to test it:

```
th src/train.lua -phase test -gpu_id 1 
-load_model -model_dir model 
-log_path log_test.txt
-visualize
-data_base_dir data/processedImage/
-data_path data/test_shuffle.lst
-label_path data/XMLsequence.lst
-output_dir results 
-max_num_tokens 100 -max_image_width 300 -max_image_height 200 
-batch_size 30 -beam_size 5
```

## Evaluate
The test perplexity can be obtained after testing is finished. In order to evaluate the exact match and BLEU, the following command needs to be executed.

```
python evaluate/checkExeperiment.py
```
Note that if you change the directory of the results data, please change it accordingly in the file.


# Acknowledgments
This work heavily depends on the https://github.com/harvardnlp/im2markup, thanks for their work.
