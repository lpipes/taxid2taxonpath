#!/usr/bin/python

import os, argparse
import sys, getopt
from textwrap import dedent
from time import strftime
from time import localtime
from sys import exit

from cogent3.parse.ncbi_taxonomy import NcbiTaxonomyFromFiles
from cogent3.parse.ncbi_taxonomy import NcbiTaxonNode
from cogent3.core.tree import TreeNode

def main(argv):
    nodes_file = ''
    names_file = ''
    outputfile = ''
    inputfile = ''
    mergednodes = ''
    deletednodes = ''
    output_ranks = ['superkingdom','phylum','class','order','family','genus','species']
    col=3
    read=2
    try:
        opts, args = getopt.getopt(argv,"hd:m:o:i:e:l:c:r:",["nodes=","names=","out=","input=","merged=","deleted=","column=","read="])
    except getopt.GetoptError:
        print('taxid2TaxonPath.py -d <nodes.dmp> -m <names.dmp> -i <kraken2> -o <txt> -e <merged.dmp> -l <deleted.dmp> -c <column of taxid> -r <column of readname>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('taxid2TaxonPath.py -d <nodes.dmp> -m <names.dmp> -e <merged.dmp> -l <deleted.dmp> -i <kraken2> -o <txt> -c <column of taxid> -r <column of readname>')
            print ('the default column of taxid is 3 and the default column of readname is 2 (for kraken2 output)')
            print ('.dmp files can be downloaded from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz')
            sys.exit()
        elif opt in ("-d","--nodes"):
            nodes_file=arg
        elif opt in ("-m","--names"):
            names_file=arg
        elif opt in ("-i","--input"):
            inputfile=arg
        elif opt in ("-o","--out"):
            outputfile=arg
        elif opt in ("-e","--merged"):
            mergednodes=arg
        elif opt in ("-l","--deleted"):
            deletednodes=arg
        elif opt in ("-c","--column"):
            col=int(arg)
        elif opt in ("-r","--read"):
            read=int(arg)
    ncbi_full_taxonomy = NcbiTaxonomyFromFiles(open(nodes_file),open(names_file))
    merged = {}
    mergeddmp = open(mergednodes,'r')
    for curr_line in mergeddmp:
        curr_line_old_taxid = curr_line.split('|')[0].strip()
        curr_line_new_taxid = curr_line.split('|')[1].strip()
        merged[curr_line_old_taxid] = curr_line_new_taxid
    mergeddmp.close()
    deleted_taxids = {}
    delnodesdmp = open(deletednodes,'r')
    for curr_line in delnodesdmp:
        curr_line_old_taxid = curr_line.split('|')[0].strip()
        deleted_taxids[curr_line_old_taxid] = True
    delnodesdmp.close()
    included_nodes = []
    node_numbers = {}
    taxid = {}
    failed_taxids = {}
    results = open(inputfile,'r')
    for curr_line in results:
        curr_reads = curr_line.rstrip().split('\t')[read-1]
        curr_taxid = curr_line.rstrip().split('\t')[col-1]
        if not curr_taxid in node_numbers:
            try:
                included_nodes.append(ncbi_full_taxonomy[curr_taxid])
            except KeyError:
                if curr_taxid in merged:
                    old_taxid = curr_taxid
                    curr_taxid = merged[curr_taxid]
                    print('The following TaxonID was changed with taxid=' + str(old_taxid) + \
                            ' --> changed to taxid=' + str(curr_taxid) + '.\n')
                elif curr_taxid in deleted_taxids:
                    old_taxid = curr_taxid
                    curr_taxid = 1 # assigns to root
                    print('This is a deleted TaxonID:\n'
                            + str(old_taxid) + \
                            ' --> changed to taxid=' + str(curr_taxid) + '.\n')
            finally:
                node_numbers[curr_taxid] = True
                try:
                    included_nodes.append(ncbi_full_taxonomy[curr_taxid])
                except KeyError:
                    failed_taxids[curr_taxid] = True
                    print('The following taxid could not be added to included_nodes: taxid=' + str(curr_taxid) + '.\n')
        taxid[curr_reads] = curr_taxid
    results.close()
    taxid_taxonomy = {}
    ranks_taxonomy = {}
    ranks_lookup = dict([(r,idx) for idx,r in enumerate(output_ranks)])
    for node in included_nodes:
        lineage = ['NA'] * len(ranks_lookup)
        curr = node
        #if curr.Rank in ranks_lookup:
        #    lineage = ['NA'] * (ranks_lookup[curr.Rank]+1)
        #else:
        #    lineage = ['NA'] * len(ranks_lookup)
        lineage_complete = False
        if curr.Rank=="no rank":
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="subspecies":
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="species group":
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="superfamily":
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="infraorder":
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
            print(curr.TaxonId)
        elif curr.Rank=="suborder":
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="cohort":
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="tribe":
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="infraclass":
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="biotype":
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="serogroup":
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="superorder":
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="subclass":
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="subfamily":
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="parvorder":
            print("help\n")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['order']
        elif curr.Rank=="kingdom":
            print("superkingdom")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['superkingdom']
        elif curr.Rank=="subgenus":
            print("subgenus")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['genus']
        elif curr.Rank=="subtribe":
            print("subtribe")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="species subgroup":
            print("species subgroup")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="varietas":
            print("varietas")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="strain":
            print("strain")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="forma":
            print("forma")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="forma specialis":
            print("forma specialis")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="clade":
            print("clade")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        elif curr.Rank=="isolate":
            print("isolate")
            print(curr.TaxonId)
            ranks_taxonomy[curr.TaxonId]=ranks_lookup['species']
        else:
            ranks_taxonomy[curr.TaxonId]=ranks_lookup[curr.Rank]
        while lineage_complete is False:
            if curr.Rank in ranks_lookup:
                lineage[ranks_lookup[curr.Rank]] = curr.Name
            curr = curr.parent
            if curr is None:
                lineage_complete = True
            elif curr.TaxonId in taxid_taxonomy:
                #import pdb; pdb.set_trace()
                for level in range(0,len(lineage)):
                    if (taxid_taxonomy[curr.TaxonId][level] != 'NA') and (lineage[level] == 'NA'):
                        lineage[level] = taxid_taxonomy[curr.TaxonId][level]
                lineage_complete = True
        taxid_taxonomy[node.TaxonId] = lineage
    missing_taxonomy = ['NA'] * len(ranks_lookup)
    o = open(outputfile,'w')
    for curr_read in taxid:
        #import pdb; pdb.set_trace()
        if int(taxid[curr_read]) == 0:
                lineage = 'unassigned'
        else:
            path = taxid_taxonomy[int(taxid[curr_read])]
            lowest_rank = ranks_taxonomy[int(taxid[curr_read])]+1
            lineage = ';'.join(path[0:lowest_rank])
        #for i in enumerate(taxid_taxonomy[int(taxid[curr_read]):
        #    lineage = ';'.join(taxid_taxonomy[
        #lineage = ';'.join(taxid_taxonomy[int(taxid[curr_read])])
        o.write(curr_read+"\t"+lineage+"\n")
    o.close()
if __name__ == "__main__":
    main(sys.argv[1:])
