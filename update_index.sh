#!/bin/bash
BASE_DIRECTORY = ~/
cd ./src/webscraper
python scraper.py 
cd ./../Search
python BuildSchema.py
cd ~/