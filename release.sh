#! /usr/bin/env sh

git co master
git merge devel
./create_plugin.sh
git co devel
