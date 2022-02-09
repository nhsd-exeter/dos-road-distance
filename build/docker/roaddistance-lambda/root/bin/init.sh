#!/bin/bash

cd /var/task/application
for f in *.py
do
  rm ../$f
  ln -s application/$f ../$f
done
