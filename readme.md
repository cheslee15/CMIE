# Data and Code for "CMIE: Combining MLLM Insights with External Evidence for Explainable Out-of-Context Misinformation Detection" (ACL'25 Findings)

This repo contains the data and code for the following paper:

Fanxiao Li, Jiaying Wu, Canyuan He, Wei Zhou. CMIE: Combining MLLM Insights with External Evidence for Explainable Out-of-Context Misinformation Detection, Findings of the Association for Computational Linguistics: ACL 2025.


## Abstract
Multimodal large language models (MLLMs) have demonstrated impressive capabilities in visual reasoning and text generation. While previous studies have explored the application of MLLM for detecting out-of-context (OOC) misinformation, our empirical analysis reveals two persisting challenges of this paradigm. Evaluating the representative GPT-4o model on direct reasoning and evidence augmented reasoning, results indicate that MLLM struggle to capture the deeper relationships—specifically, cases in which the image and text are not directly connected but are associated through underlying semantic links. Moreover, noise in the evidence further impairs detection accuracy.
To address these challenges, we propose CMIE, a novel OOC misinformation detection framework that incorporates a Coexistence Relationship Generation (CRG) strategy and an Association Scoring (AS) mechanism. CMIE identifies the underlying coexistence relationships between images and text, and selectively utilizes relevant evidence to enhance misinformation detection. Experimental results demonstrate that our approach outperforms existing methods. 

## Get Started
### Install Dependency
```bash
pip install -r requirements.txt
```

### Data Preparation
Download the NewsCLIPpings dataset and the corresponsing evidences. Sample data used in our paper is available in the `./dataset/ directory.

### OpenAI API Key
Please register for an API Key on https://platform.openai.com/api-keys. Then set up the API Key in `/utils.py`

### Evaluation
Running this will reproduce the results reported in our paper.
```bash
python evaluate.py 
```

### Run CMIE
After preparing your own data in the same format as the provided demo, you can run the following command to execute the CMIE pipeline.
```bash
python main.py 
```
