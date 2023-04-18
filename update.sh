conda update --all -y
run_nbs
nb_py
pip list --format=freeze > requirements.txt
black *.ipynb
black *.py
gitcombo
