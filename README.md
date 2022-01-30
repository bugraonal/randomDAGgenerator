# Random DAG Generator
A python script for randomly generating directed acyclic graphs. Generates a PDF file using Graphviz. Configurable parameters are number of nodes, number of levels and saturation fraction. 

The nodes are distrubuted to levels using a partial distrubution functions. The function has two parts; a linear part and a constant part. The saturation fraction will determine the limits of the functions. 

There are various randomization parameters in the code for distrubution and connectivity. These can also be modified. 

This was written to benchmark different memory architectures for a custom processor. 

The script will create a Graphviz file for the graph generation along with a PDF containing the generated graph. 
