#!/bin/sh

# This program downloads the latest data from the server,
# then runs the extract file on it locally.

# access the server
cd code/game_project
ssh study1@study.medialucida.co.uk
# enter password


cd study.medialucida.co.uk/data
git add .
git commit -m "latest update"
git push
# enter password

exit

./extract_easy.sh






