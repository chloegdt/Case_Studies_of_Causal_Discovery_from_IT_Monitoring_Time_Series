# Case studies of causal discovery for IT monitoring time series
____________________________________________________________________

*Temporary version.*

This is work based on the code available here :  https://github.com/ckassaad/Case_Studies_of_Causal_Discovery_from_IT_Monitoring_Time_Series

## Installation
Python version used : 3.9.19

To install all the libraries used: 
``` pip install -r requirements.txt```

## Utilisation

The following Python files  : 
- test_Mom.py
- test_Storm.py
- test_Web_processed.py
- test_Antivirus_processed.py

can be executed using this command line in the terminal : 
```python3 run_tests.py [OPTIONS] {MOM|INGESTION|WEB|ANTIVIRUS} {CBNB_W|CBNB_E|NBCB_W|NBCB_E|GCMVL|PCMCI|PCGCE|VARLINGAM|TIMINO|DYNOTEARS}```

The currently available options (more are in progress) are:
- ```--tau INTEGER``` : lag (the default value depends on the dataset)
- ```--sig FLOAT```  :  significance threshold (default 0.05)
- ```--dataset INTEGER```  1 or 2 for MOM, WEB and ANTIVIRUS
- ```--save STR``` : save the graph with the given filename
- ```--show``` : show the graph
- ```--help```   show the usage and available options

> Note: if a dataset is provided for Ingestion, it will be ignored

____________________________________________
## Data

All data are available at: https://easyvista2015-my.sharepoint.com/:f:/g/personal/aait-bachir_easyvista_com/ElLiNpfCkO1JgglQcrBPP9IBxBXzaINrM5f0ILz6wbgoEQ?e=OBTsUY


## Methods

* Dynotears: https://github.com/quantumblacklabs/causalnex

* PCMCI+: https://github.com/jakobrunge/tigramite

* PCGCE: https://github.com/ckassaad/PCGCE

* VarLiNGAM: https://github.com/cdt15/lingam

* TiMINo: http://web.math.ku.dk/~peters/code.html

* NBCB: https://github.com/ckassaad/Hybrids_of_CB_and_NB_for_Time_Series

* CBNB: https://github.com/ckassaad/Hybrids_of_CB_and_NB_for_Time_Series
