# cluster-anywhr

cluster contains the API
cluster-shows contains the Front end form and hex structure

in cluster :
overview :

1. You can add a hexagon to a node and it gets reflected
2. one you add , it gets connected to its neghbour and reflected in the grid structure in frontend
3. you can delete a hex using its name 
4. you can only delete , if its degree is greater than 2

used aws - lambdas for API's

DB - idea :
Three table :

1. hexagons: uniquely identifies a Hexagon 
2. clusters: uniquely indentifies neighbours of a hexagon using all UUID's , so search queries are at depth =  1
3. locations: uniquely locates a hex 


comfortable :

Tech stacks : python , flask, JS , reactjs 
