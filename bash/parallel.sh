
ls -1 .. | parallel echo {}

parallel -j 1 echo {1}_{2} ::: A B C D E ::: 1 2 3 4 5 6 7

seq 2007 2019 > years.txt && seq 1 12 > months.txt
parallel -j 1 --eta --progress --verbose echo {1} {2} :::: years.txt :::: months.txt
rm -f years.txt months.txt

seq 100 | parallel --jobs 0 --eta --progress --bar 'sleep 0.1'
