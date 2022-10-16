mkdir -p archive
mv *.log archive/
mv *.png archive/

python3 -m black *.py
python3 -m flake8 *.py
