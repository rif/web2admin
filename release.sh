#! /usr/bin/env sh

git co master
git merge devel
tar czvf ~/Ubuntu\ One/web2py.plugin.web2admin.w2p --exclude='*.sh' *
git co devel
