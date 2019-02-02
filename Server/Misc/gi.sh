#!/usr/bin/env bash

git init
git add .
git commit -m "init"
git status
git log
git remote add origin https://github.com/Jacko1394/new.git
git remote -v
git push --set-upstream origin master
