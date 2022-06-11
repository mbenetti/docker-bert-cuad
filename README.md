# Streamlit Web App on of Bert transformer for Clause extraction on commercial contracts 
### Bert implementation for contract analysis and clause extraction.

![contracts](https://user-images.githubusercontent.com/27162948/171717588-4cf26c0a-874e-45ac-b080-a00f39664177.jpg)


This is a Docker implementation of the Bert Base model trained on the CUAD dataset. The front end is a streamlit web app that allows to upload any contract and extract one, or all of the 41 aspects of a commercial contract. This repo contains instructions to run the CPU and the GPU implementations. 

The gentel introduction can be found on my previous repo: 

```
https://github.com/mbenetti/bert-cuad.git
```

Additional information about the project:
Contract Understanding Atticus Dataset (CUAD) v1 is a corpus of 13,000+ labels in 510 commercial legal contracts that have been manually labeled under the supervision of experienced lawyers to identify 41 types of legal clauses that are considered important in contact review in connection with a corporate transaction, including mergers & acquisitions, etc.

** **
Prerequisites are Docker installed on your system. Then run:

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

**Screenshots**


![Bert-contract01](https://user-images.githubusercontent.com/27162948/173197297-2bb27090-3623-4a53-9a09-334ebd8c8f23.png)

![Bert-contract02](https://user-images.githubusercontent.com/27162948/173197300-4b981563-bf67-411d-ac11-3eb2230fe0bb.png)

![Bert-contract03](https://user-images.githubusercontent.com/27162948/173197303-8f12e0ff-f1f6-4369-8bcc-69cda864cc7e.png)

![Bert-contract04](https://user-images.githubusercontent.com/27162948/173197306-3ae71697-25a3-489d-8e78-1ffb7645eee1.png)

![Bert-contract05](https://user-images.githubusercontent.com/27162948/173197308-dbf91f59-bf8d-47b5-afd7-035625a0f3c3.png)

**Benetti Mauro 05.2022**

https://www.maurobenetti.ml

**License: CC BY 4.0** 

###### https://creativecommons.org/licenses/by/4.0/

** **

**Project that create the dataset:** 

https://www.atticusprojectai.org/cuad

**Git Hub of the project:** 

https://github.com/TheAtticusProject/cuad

**CUAD Dataset:** 

https://huggingface.co/datasets/cuad

*Bert models are under Apache License 2.0*

