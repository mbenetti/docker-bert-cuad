# docker-bert-cuad
### Streamlit container with Bert trained on CUAD dataset for contract analysis and clause extraction.

This is a Docker implementation of the Bert Base model trained on the CUAD dataset. The front end is a streamlit web app that allows to upload any contract and extract one or all the 41 aspects of a commercial contract. This is a CPU and Bert Base version, for the full GPU version and the Base, Large and X-Large models please check my next repo.

Additional information about the project:
Contract Understanding Atticus Dataset (CUAD) v1 is a corpus of 13,000+ labels in 510 commercial legal contracts that have been manually labeled under the supervision of experienced lawyers to identify 41 types of legal clauses that are considered important in contact review in connection with a corporate transaction, including mergers & acquisitions, etc.

Run:

```cmd
sudo docker run -p 8501:8501 25987908/cuad-cpu-bbase:latest
```
and open http://localhost:8501

To build from source

```git
git clone  mbenetti/docker-bert-cuad
```

```cmd
cd folder....
docker build -t streamlitappgpu:latest .
```

**Original Project:** 

https://www.atticusprojectai.org/cuad

**Git Hub: Bert model and training scripts** 

https://github.com/TheAtticusProject/cuad

**CUAD Dataset: created by the Atticus Project** 

https://huggingface.co/datasets/cuad

All Bert models have Apache License 2.0

*Implementation by Benetti Mauro 05.2022*

mauro.benetti@gmail.com

*License: CC BY 4.0* 
#### https://creativecommons.org/licenses/by/4.0/
