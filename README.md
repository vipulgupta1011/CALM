# CALM

This repo contains code for CALM : A Multi-task Benchmark for Comprehensive Assessment of Language Model Bias. [arXiv](https://arxiv.org/abs/2308.12539)

Dataset can be found on huggingface at : [https://huggingface.co/datasets/vipulgupta/CALM](https://huggingface.co/datasets/vipulgupta/CALM)

## Installation
1. Clone this repo : `git clone https://github.com/vipulgupta1011/CALM.git`
2. Install the dependencies : `pip install -r requirements.txt`
We have used ```python version 3.9.12``` for our experiments.

For installing flash attention, please refer to the original github repo of [flash attention](https://github.com/Dao-AILab/flash-attention). Some of the latest LLMs uses flash attention and it might be worth the time to install it. Some models do not require flash attention and you can skip installing it for now.

## Generating Results

To produce our results and test for more models, please refer to the code along with detailed instructions in [evaluation](https://github.com/vipulgupta1011/CALM/tree/main/evaluation) folder.

To reproduce the results on bloom (it does not use flash attention), run the following command:
1. `cd evaluation`
2. `python evaluate_models/evaluation_bloom.py`


## Generating Dataset

Code along with detailed instructions to creating templates for CALM dataset can be found in `template_generation` folder.

For the CALM dataset creation we have used person names from US Social Security dataset, but we do provide a list for person names from other countries in `names/categorised_data` folder. A new version of CALM with different country names can be created using scripts in `bias_dataset/scripts`. Script to add more countries data can be found in `names` folder.


## Citation
If you find this repo useful, consider cite our work:
```
@article{gupta2023calm,
  title={CALM: A Multi-task Benchmark for Comprehensive Assessment of Language Model Bias},
  author={Gupta, Vipul and Venkit, Pranav Narayanan and Lauren{\c{c}}on, Hugo and Wilson, Shomir and Passonneau, Rebecca J},
  journal={arXiv preprint arXiv:2308.12539},
  year={2023}
}
```
