# MetaSUB Reproducible Metadata

This repository is a collection of raw MetaSUB metadata with annotation and scripts to produce cleaned metadata. It is reproducible in the sense that it generates metadata directly from documentary files without relying on a person to collate files.

A metadata table can be generated with this command: `metasub-generator best-effort > metadata.csv`

[This file](https://github.com/MetaSUB/MetaSUB-metadata/blob/ba04acb5bf6df79d2a9cdd30178f80386b6475c0/complete_metadata.csv) is the most recent, complete, and stable version of the metadata (v1.0.1).

## Installation

```
git clone git@github.com:MetaSUB/MetaSUB-metadata.git
cd MetaSUB-metadata
python setup.py develop
```

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

`samples_oly_meta_all_information_e.xlsx` Metadata for OLY16 samples from Brazil team.

`CSD Sample IDs -2.xlsx` 3 letter codes for all metasub cities

`PathoMap-3.xlsx` PathoMap metadata from Ebrahim

`Winter2014_metadata-3.xlsx` Winter PathoMap metadata from Ebrahim

## Unpackaged Scripts

`clean_parse_alina_mdata_tbl.py` Alina F. generated a metadata table by dumping the output of Kobo toolbox into a file named `gCSD2017_metadata_joint-1.txt`. That table has several issues: city names are non canonical, na tokens are non canonical, barcodes were recorded as numbers so lost a leading zero, and fields 'wandered' between columns. This script produces a cleaned version of that table.

`map_collate` (`mappers.py`, `sample_wise.py`, `sample.py`) a miniature package that defined a best-effort approach to matching metadata with variosu forms of identification. The key insight is that this package is intended to deal with many layers of indirection that may originate in many different places. Relies on a large number of metadata files many of which were themselves edited and cleaned.



