#!/bin/bash
git config --global user.name 'Zoaker'
git config --global user.email "Zoaker@163.com"
ssh-keygen -t ras -C "Zoaker@163.com"
cd ~/.ssh
cat id_ras.pub
