#!/bin/bash

conda create -n rvc python=3.10 anaconda
conda actiate rvc
pip install -r requirements.txt
