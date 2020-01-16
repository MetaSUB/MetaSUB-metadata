.DEFAULT_GOAL: help

help:
	@echo "complete - build the metasub metadata table"

complete:
	metasub-generator best-effort > temp_complete_metadata.csv 
	mv temp_complete_metadata.csv complete_metadata.csv

columns:
	head -1 complete_metadata.csv | tr ',' '\n'

cities:
	cat complete_metadata.csv | cut -d ',' -f5 | sort | uniq -c