# NT2vec
Produce vectors from network traffic capture files.

**Usage**  
The pcap_2_csv script takes a pcap file and IP address as the first and second arguments.  The script runs a function to 
detect the traffic bursts in the pcap file.  These burst ranges are then passed to another function that chops the pcap
file into separate CSV files, with one trace per file (one trace = one burst).  

To run the script cd into the project directory and run ...
```
python3 pcap_2_csv.py <filename.pcap> <device ipv4 address>
```
The resulting CSV files will be saved in the 'csv/' directory with the name \<filename_n.csv> for n number of traces.

*NOTE*: Currently the burst detection function only works with shorter traffic bursts. At this point we should make sure
we do cursory checks of the burst ranges and compare them to trace files to make sure burst detection is working as intended.

**Dependencies**  
Python 3.6  
See requirements.txt file for list of necessary libraries.  

