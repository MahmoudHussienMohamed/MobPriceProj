# MobPriceProj
Devices Price Classification System assessment for **Maids.cc**. System has **97.35% accuracy score** utilizing the power of **SupportVectorClassifier (*SVC*)** and non-blocking server with the use of **SpringBoot WebFlux** utilities.
## Project Structure
``` bash
├── API.py
├── BE
│   └── EndPoints
│       └── src
│           └── main
│               ├── java
│               │   └── com
│               │       └── MobPriceCls
│               │           └── EndPoints
│               │               ├── Controller
│               │               │   └── DeviceController.java
│               │               ├── DTO
│               │               │   └── DeviceDTO.java
│               │               ├── EndPointsApplication.java
│               │               ├── Entity
│               │               │   └── Device.java
│               │               ├── Repository
│               │               │   └── DeviceRepository.java
│               │               ├── Service
│               │               │   └── DeviceService.java
│               │               └── Utils
│               │                   └── AppUtils.java
│               └── resources
│                   ├── application.properties
│                   └── application.yml
├── ML
│   ├── Model-API.py
│   ├── Model.ipynb
│   ├── Model.pkl
│   ├── Pipeline.pkl
│   ├── test.csv
│   ├── train.csv
│   └── Transformers.py
├── README.md
└── springboot-init-configs.txt
```
### ML (Machine Learning) 
`ML` folder contains all the machine learning code, model, preparing pipeline, and API. ML model is ***SVC*** with **97.35% accuracy!**
* `Model-API.py`: Python module contains a single endpoint responsible for handling remote model invocations (*i.e. SpringBoot requests*).
* `Model.ipynb`: Jupyter Notebook contains all data pereparation, data pereparation, model design and evaluation, and hyperparameters fine-tuning
* `Model.pkl`: The SVC pretrained classification model with **97.35% accuracy!** 
* `Pipeline.pkl`: Preparing pipeline that transforms data for the model. (*designed in `Model.ipynb`*)
* `test.csv`: Test data set. 
* `train.csv`: Training data set.
* `Transformers.py`: The custom transformers I created for data preparation. (*designed in `Model.ipynb` as well*)

### BE (Back-End)
`BE` folder contains all the back-end code (*written in **Java SpringBoot** and using **non-blocking** techinques using **WebFlux***) and configurations for data base (*which is **MongoDB***).

### Remaining important files
* `API.py`: Python module acts as client side and call requests and endpoints of back-end.
* `springboot-init-configs.txt`: contains link of **SpringBoot Initializer** with configured values.
