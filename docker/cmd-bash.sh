#!/bin/bash -xe

pip install -r requirements_test.txt --src /usr/local/src
pip install ipdb
make bash
