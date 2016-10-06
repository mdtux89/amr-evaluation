#! /usr/bin/env python

import sys
import re

for graph in open(sys.argv[1]).read().split("\n\n"):
	graph = re.sub("/ [a-zA-Z0-9-]+", "/ label", graph)
	graph = re.sub(":[a-zA-Z0-9-]+ ", ":label ", graph)
	print graph
	print ""
