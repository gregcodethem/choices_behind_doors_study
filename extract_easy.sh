
# Download data
cd ~/code/game_project/data
git reset --hard HEAD
git pull

# update main file if necesary
cd ~/code/game_project
source env/bin/activate
git checkout master
git reset --hard HEAD
git pull
pip install -r requirements.txt

python extract_all.py

