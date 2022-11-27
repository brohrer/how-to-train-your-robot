mkdir -p archive
if [ -f *.log ]; then 
  mv *.log archive
fi

if [ -f *.png ]; then
  mv *.png archive
fi

flake8 *.py
black --line-length 80 *.py
