#!/bin/bash

for filename in ~/Desktop/Sonal/Output/*; do
	echo $filename
    cd $filename
    cat download | parallel --gnu "wget {}"
done