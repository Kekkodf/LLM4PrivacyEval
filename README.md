# SIGIR-SP-PrivacyEvalLLMs
Repository for the SIGIR Short Paper (SP) on Assessing Privacy of Obfuscation Mechanisms using LLMs.



## Structure

The repository is structured as follows:

- `appendix/`: Contains the appendix of the paper.  
- `config/`: Contains the configuration files for the experiments.  
  (To run them, you need to generate a conda environment from the `env.yml` file and a cloud key from the  
  [Groq Cloud Platform](https://console.groq.com/playground).)  
- `data/`: Contains the data used in the experiments.  
  (Query_ID, Original_text, Obfuscated_text, LLM_Score, LLM_Justification, LLM.)  
- `results/`: Contains the results of the experiments.  
- `src/` and `demo.py`: Contain the code to run the experiments.  

![LLM](./plots/niceImage.png)


## Running the code

To run the code, you need to install the dependencies in the `env.yml` file. You can do this by running the following command:

```bash
conda env create -f env.yml
```
Then, you need to activate the environment:

```bash
conda activate sigir-sp-privacy-eval-llms
```

Finally, you can run the code by running the following command:

```bash
python demo.py
```

Remark: Put the Groq cloud key in the `config/key.txt` file.

## Findings

Prompt Used

  ![Prompts](./plots/textPrompts.png)


### Distributions of LLM Scores

  ![Legend](./plots/legend_prompts.png)

  **DeepLearning19**  
  ![MSMarcoDL19](./plots/distributions_msmarco-dl19.png)

  **Medline04**  
  ![MEDLINE04](./plots/distributions_medline-2004.png)


