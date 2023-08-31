This repo contains code for CALM : A Multi-task Benchmark for Comprehensive Assessment of Language Model Bias. [arXiv](https://arxiv.org/abs/2308.12539)

Dataset can be found on huggingface at : [https://huggingface.co/datasets/vipulgupta/CALM](https://huggingface.co/datasets/vipulgupta/CALM)

Ground truths for CALM dataset can be found in `evaluation/gt` folder.

Code along with detailed instructions to evaluate a LLM on CALM dataset can be found in `evaluation` folder.

Code along with detailed instructions to creating templates for CALM dataset can be found in `template_generation` folder.

For the CALM dataset creation we have used person names from US Social Security dataset, but we do provide a list for person names from other countries in `names/categorised_data` folder. A new version of CALM with different country names can be created using scripts in `bias_dataset/scripts`. Script to add more countries data can be found in `names` folder.


