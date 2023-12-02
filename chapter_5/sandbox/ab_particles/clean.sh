pkill python3 

mkdir -p archive
mv *.log archive 2> /dev/null
mv *.png archive 2> /dev/null

black --line-length 80 *.py
