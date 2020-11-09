#!/bin/bash

for d in `ls -d */`; do
	rm $d/*.{cells,playground,camp,png}
done
