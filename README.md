# taxid2taxonpath
converts taxids to taxonpaths
modified from https://github.com/bakerccm/entrez_qiime and updated for python3
uses the cogent3 library

taxid2taxonpath.py 
-d <nodes.dmp> 
-m <names.dmp> 
-e <merged.dmp> 
-l <deleted.dmp> 
-i <input_file> 
-o <output_file> 
-c <column of taxid> 
-r <column of readname>
the default column of taxid is 3 and the default column of readname is 2 (for kraken2 output)
.dmp files can be downloaded from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
