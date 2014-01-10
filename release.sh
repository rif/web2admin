#! /usr/bin/env sh

git co master
git merge devel
git co devel
git push
