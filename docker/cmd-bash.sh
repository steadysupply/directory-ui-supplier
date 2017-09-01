#!/bin/bash -xe

apt update -q
apt install -yq vim
pip install -r requirements_test.txt --src /usr/local/src
pip install ipdb
make bash
