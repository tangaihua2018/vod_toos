#!/bin/bash
nohup python3 ${HOME}/bin/day_upd.py > ${HOME}/logs/$(date +%Y-%m-%d)_day.log 2>&1 &