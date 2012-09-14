#! /usr/bin/env sh

git co master
git merge devel
./create_plugin.sh
git co devel
markdown README.md >static/plugin_web2admin/about.html
