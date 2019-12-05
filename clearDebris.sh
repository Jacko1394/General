#!/usr/bin/env bash

cd /Users/jd/GIT/MAGIQ\ Mobile/src/Magiq.Mobile.iOS
find . -type f -name '*.png' -exec xattr -c {} \;
