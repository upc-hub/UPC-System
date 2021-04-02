#!/bin/sh

/app/src/wimnetsim 2020 0.0 /app/data/field-ex1.dat /app/data/node-ex1.dat /app/data/dashnode-ex1.dat /app/data/link-ex1.dat /app/data/route-ex1.dat 125 1000

rm buffer.txt
rm NOMURA_delay.txt
rm qlength.txt
rm delay.txt
#echo "I am Hein Htet" >> name.txt
#cat throughput.txt
mv throughput.txt /opt/throughput.txt
mv out.txt /opt/ap_information.txt
mv out.txt /opt/ap_information.txt
echo throughput:opt > /opt/result.txt
grep "TJ_VER: average throughput:"  /opt/throughput.txt >> /opt/result.txt
