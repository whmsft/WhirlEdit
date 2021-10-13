pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon "./DATA/icons/favicon.v3.ico" --name "WhirlEdit" --add-data "./tkcode;tkcode/"  "main.py"