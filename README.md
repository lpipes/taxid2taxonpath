# taxid2taxonpath
converts EMBL, NCBI (GenBank), DDBJ taxon ids to full taxonomic paths
modified from https://github.com/bakerccm/entrez_qiime and updated for python3
uses the cogent3 library

taxid2taxonpath.py 
-d* nodes.dmp
-m* names.dmp 
-e* merged.dmp 
-l* delnodes.dmp 
-i* input_file 
-o* output_file 
-c column_of_taxid 
-r column_of_readname

*positional arguments

the default column of taxid is 3 and the default column of readname is 2 (for kraken2 output)

outputs the following ranks:
'superkingdom','phylum','class','order','family','genus','species'


.dmp files can be downloaded from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
