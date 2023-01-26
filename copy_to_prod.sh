#!/bin/bash

# source directory
src_dir="/home/saknesar/dundlabumi.lv/dainis_git_action"

# destination directory
dst_dir="/email/"

# array of files and directories to copy
files_to_copy=("manage.py" "passenger_wsgi.py" "email_tracking" "tracking_app")

# loop through the array and copy each file/folder
for item in "${files_to_copy[@]}"; do
  cp -r "$src_dir/$item" "$dst_dir"
done