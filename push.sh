#!/bin/bash

git status
git add .
git commit -m "update"
git push -u origin main
git status

git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/devnamdev2003/task_management_system.git
git push -u origin main