#!/bin/bash

ssh -N -f -R 8887:localhost:8888 login12
source jsalt_startup.sh
jupyter-lab  --port 8888

#On laptop, forward: ssh -L 8000:localhost:8887 abeb4417@login12.rc.colorado.edu || curc