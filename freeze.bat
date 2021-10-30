pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm --windowed --icon "./DATA/icons/favicon.v3.ico" --name "WhirlEdit" --add-data "./data.py;." --add-data "./widgets.py;." --add-data "./tkcode;tkcode/"  "main.py"
