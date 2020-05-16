**Master thesis**
-
**Requirements**

- [Jupyter notebook](https://jupyter.org/install.html)
* `requirements.txt` 

    * contains used packages
    * for installation activate the virtual enviroment ([venv](https://docs.python.org/3/library/venv.html)) and then run: `pip install -r requirements.txt`


**Project structure**

* folder `crf_extraction` contains:
    * subfolders with scripts for each CRF model
        * in every subfolder is `trained.joblib` which is a trained model before hyper-parameter tuning
        * `*_model_features.py` - word features for each CRF model
        
    * utility folder `utils` with helper functions
    
* folder `rnn_extraction` contains:
    * subfolders with scripts for LSTM and BiLSTM models
    
* folder `data_preprocessor` contains:

    * `medic.csv` part of provided data used for experimental dataset
    * `preprocessor.py` script for preprocessing of provided data
    * `data_preparation.ipynb` for creating of experimental dataset and dividing it into three parts - train, validation, test 

* folder `datasets` contains:

    * `train_dataset.csv`
    * `validation_dataset.csv`
    * `test_dataset.csv`
    
* folder `utils` contains helper classes and functions

**Important:** Provided `medic.csv` file and generated train, validation and test datasets from this file form only a small part of 
all used data and serve only for demonstration purposes.