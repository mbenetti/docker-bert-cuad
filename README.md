# Streamlit Web App on of Bert transformer for Clause extraction on commercial contracts 
### Streamlit and a Bert implementation for contract analysis and clause extraction.

![contracts](https://user-images.githubusercontent.com/27162948/171717588-4cf26c0a-874e-45ac-b080-a00f39664177.jpg)


This is a Docker implementation of the Bert Base model trained on the CUAD dataset. The front end is a streamlit web app that allows to upload any contract and extract one, or all of the 41 aspects of a commercial contract. This repo contains instructions to run the CPU and the GPU implementations. 

Additional information about the project:
Contract Understanding Atticus Dataset (CUAD) v1 is a corpus of 13,000+ labels in 510 commercial legal contracts that have been manually labeled under the supervision of experienced lawyers to identify 41 types of legal clauses that are considered important in contact review in connection with a corporate transaction, including mergers & acquisitions, etc.

Prerequisites are Docker installed on your system:

Then run:

```cmd
sudo docker run -p 8501:8501 25987908/cuad-cpu-bbase:latest
```
Remove the sudo statement if you are in Win2 of course, and open:

```
http://localhost:8501
```

**GPU version with Nvidia support**

The full version with 3 models; Bert Base, Bert Large and Xlarge with GPU support can be run with the following command:

```
sudo docker run -p 8501:8501 --gpus all 25987908/cuad-gpu-bxlarge 
```

and open:

```
http://localhost:8501
```

**To build from source, only cpu version**

```git
https://github.com/mbenetti/docker-bert-cuad.git  
```

```cmd
cd docker-bert-cuad
```

Download the Base model from 

```
https://zenodo.org/record/4599830/files/roberta-base.zip?download=1
```

Copy the model folder inside the "cuad-models" folder. Build the container run the following command on the 


```
docker build -t docker-bert-cuad:latest .
```

**Screenshoots**

![docker deployment 3](https://user-images.githubusercontent.com/27162948/172209631-0eed4a47-04d0-4063-ac70-2b4bbbda2672.png)
![docker deployment 4](https://user-images.githubusercontent.com/27162948/172210219-b9863aec-d32f-4727-93f0-e5865d7e7e13.png)

![docker deployment 2](https://user-images.githubusercontent.com/27162948/172209609-27efff13-415b-4d09-95e6-09cdf5f8c8b3.png)
![docker deployment](https://user-images.githubusercontent.com/27162948/172209676-87a62bcb-22d3-4ddd-8a7e-082f315e3b1c.png)


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
