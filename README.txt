First-Time Setup Summary

git clone https://github.com/alonkr13/communications-LTD-CTF-SECURE.git
cd communications-LTD-CTF
cd backend
python -m venv venv

PowerShell:

.\venv\Scripts\Activate.ps1

Git Bash:

source venv/Scripts/activate

Install dependencies:

pip install -r requirements.txt

Run the server:

python -m uvicorn main:app --reload   /  python main.py

------------------------------------------

Important Notes

Do not commit:

venv/
__pycache__/
.db files
.vscode/

These are already ignored by .gitignore.
