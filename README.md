# Overview

This repository is a collection of raw MetaSUB metadata with annotation and scripts to produce cleaned metadata.

To build a clean metadata table run the following commands

`python setup.py develop` to install

`metasub-generator best-effort --sample-names <list of names> > metadata.csv`
to generate a metadata table.

`--sample-names` may be omitted to use a default list of sample names `spreadsheets/sample_names.txt`

## Spreadsheets

`city_names.csv` Canonical city names and countries. 

`metadata.MetaSUB_UK2017.xlsx` Clean metadata from the UK Tigress (Channel 4) sampling project. Includes IDs that match FASTQ files.

`ha_to_msub_name_conversion_for_project_haib17CEM4890.xlsx` Table that maps H.A. names (`4890-CEM-[0-9]{4}`) to MetaSUB names for 576 samples from OLY and CSD16. Also includes info about DNA conc.

`Control_Plate_Final.xlsx` Table that maps H.A. names (`4959-DB[0-9]{4}`) to barcodes, information about control plates. Also includes metadata from 'Hospital' samples. Control information includes the following keys:
 - CTRL cities
 - Dry tube
 - Dry tube & swab
 - Tube & RNA/DNA out
 - Tube & RNA/DNA out & swab 

`UK_Tube_Plates_Updated021117.xlsx` Table mapping plate positions to metadata from London gCSD17. Does NOT include IDs that will be useful for mapping fastqs.

`gCSD2017_metadata_joint-1.txt` A rough metadata table for gCSD17 produced by Alina F. from Kobo toolbox. This table identifies samples exclusively by barcode.

`cleaned_simplified_metadata.csv` A cleaned version of `gCSD2017_metadata_joint-1.txt` produced using the script `clean_parse_alina_mdata_tbl.py`.

`HA Submissions-Grid view.csv` Exported from an airtable. This table maps H.A. IDs to plate positions.

`CSD2017_DAVID.csv` This table maps plate positions to barcodes for CSD17 samples.

`filenames_HCY5HCCXY.tsv` maps SL names to H.A. IDs for 191 samples.

`Conversion Tables-Table 1.csv` This table maps IDs used by London in gCSD17 to H.A. names of fastq files.

`Metadata-Table 1.csv` This table includes metadata from London gCSD17 and appears to be roughly analagous to `UK_Tube_Plates_Updated021117.xlsx`

`sample_metadata.csv` Metadata for 1301 samples/fastqs produced using the `map_collate` package. Many fields are incomplete for many samples.

`collated_metadata_csd16.csv` Metadata for many csd16 samples made by row binding sheets from GIS cloud and canonicalizing city names.

`upload_metadata_csd16.csv` Metadata for csd16 samples with fields that would be problematic for MGS removed. Based on `collated_metadata_csd16.csv`

`sample_names.txt` Fastq names currently on cluster

`sample_names_types.tsv` Sample names with types.

`airsamples_ha_id_to_msub_name.csv` H.A. sample submission mapping H.A. IDs to MetaSUB names.

## Unpackaged Scripts

`clean_parse_alina_mdata_tbl.py` Alina F. generated a metadata table by dumping the output of Kobo toolbox into a file named `gCSD2017_metadata_joint-1.txt`. That table has several issues: city names are non canonical, na tokens are non canonical, barcodes were recorded as numbers so lost a leading zero, and fields 'wandered' between columns. This script produces a cleaned version of that table.

`map_collate` (`mappers.py`, `sample_wise.py`, `sample.py`) a miniature package that defined a best-effort approach to matching metadata with variosu forms of identification. The key insight is that this package is intended to deal with many layers of indirection that may originate in many different places. Relies on a large number of metadata files many of which were themselves edited and cleaned.

## Known Unknowns

 - Metadata for NYC Winter
 - Metadata for PathoMAP
 - Metadata for Pilot
 - Metadata for many gCSD16 samples
 - Metadata for Olympiome

## What are the MetaSUB sample collection projects?
 - CSD-2016
 - CSD-2017
 - Tigress
 - Pilot (Early 2016)
 - NYC Winter
 - Olympiome 2016
 
## Known Irregularities

London did not use the Kobo Toolbox app in gCSD17

## What are the MetaSUB sample extraction and sequencing batches?

N.B. these were largely informal and are ongoing

 - ~5k samples extracted at qiagen, then shipped to hudsonalpha (we have an inventory?)
 - Some samples were sent to Hong Kong for extraction, library prep and sequencing (Hong Kong and Shanghai)
 -  Some samples have been kept in Moscow for extraction, library prep and sequencing
 -  London has shipped barcoded tubes from csd2017 to Shanghai. Then Shanghai has sent WCM the samples
 -  UK sent samples to Zymo. Zymo does not have barcode reader so they're labeling by position (this is resolved)
 -  Stockholm extracted samples from Stockholm and other cities and sent the extracted samples to hudsonalpha
 -  We have <a number> of samples in our freezers


