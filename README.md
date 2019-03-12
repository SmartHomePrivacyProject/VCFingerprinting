# Voice Command Fingerprinting Attack

This repository contains the source code and data for the Voice Command Fingerprinting Attack.  The attack is a privacy leakage attack that allows a passive adversary to infer the activity of a smart speaker user by eavesdropping encrypted traffic between the smart speaker and the smart speaker's cloud services.

**The dataset and code are for research purposes only**. The results of this study are published in the following paper: 

Sean Kennedy, Haipeng Li, Chenggang Wang, Hao Liu, Boyang Wang, Wenhai Sun, *“I Can Here Your Alex: Voice Command Fingerprinting Attacks on Smart Home Speakers,”* IEEE Conference on Communications and Network Security (**IEEE CNS 2019**), June 10-12, Washington D.C., 2019. (The first three authors contribute equally in this paper) 

## Content

### Data

The ```data``` folder contains the following:

```amazon_echo_query_list_100.xlsx``` - An excel spreadsheet of one hundred smart assistant queries.  We captured the network traffic data generated when performing these queries to build our dataset.

```capture_files``` - A folder containing two folders of pcap network capture files, each with one hundred pcap files captured by two different people. 

 ```trace_csv```- A folder that contains 1000 network trace files in csv format.  The trace files are extracted from the pcap files in capture_files using the ```pcap2csv``` code.  The attributes of the csv files are:

-  ```time``` - The timestamp of the packet relative to the first packet in the tracefile
- ```size``` - The size of the packet in bytes
- ```direction``` - A value indicating whether the smart speaker is the source of the packet or the destination.  A value of 1 indicates the speaker is the source and a value of -1 indicates the speaker is the destination 

### BuFLO_defense

This folder contains the implementation of the website fingerprinting countermeasure BuFLO (Buffered  Fixed-Length  Obfuscation).  This is used to assess the performance of the attack when website fingerprinting defenses are in place.

### doc2vec_model

This folder contains the training and inference code for the doc2vec model, a machine learning model that represents sequences of text as fixed length vectors.  Using these vectors allows for calculating the similarity between two queries, which can be used as an evaluation of the performance of the attack, i.e., if an adversary does not predict the exact query, we can use the distance between the vectorized prediction and the vectorized query as a performance metric for the attack.

### pcap2csv

This folder contains the code used to convert pcap network capture files into csv network trace files, that can be used to train the models that are utilized in the voice command fingerprinting attack.

### vcfp_attack

This folder contains four traffic analysis algorithms used in the attack.

## Usage

See the REAME files in each folder for instructions on usage.

