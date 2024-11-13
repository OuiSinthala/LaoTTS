# Welcome to Lao Text To Speech project

* **We aim to create a functional tts engine for lao language**


---
## Instruction for start testing the tts 

> **Requirements**:
>* You must have docker installed in your machine. [Download docker desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)  
> * Clone the project with "git clone"

--- 

1. Go into the cloned folder and go into the **build_tts_engine_container** folder


2. Run this docker command for creating a docker container: 
* here all the required libraries will be installed
```bash
docker compose up --build -d
```

3. After you created the docker container then go to this url or link:
> URL: http://localhost:8501/

>**Remark**: the website will be slow at the first time the container is running because the container has to go download models from the internet.

4. If your testing is done, run this docker command to destroy the running container.
* You must in the **build_tts_engine_container** folder 
```bash
docker compose down
```














