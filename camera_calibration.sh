#!/bin/bash

mkdir ./tmp_calib_dir
python3 user_interface.py "$1"
rm -rf ./tmp_calib_dir
