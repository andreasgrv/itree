# i-tree

disclaimer: you can't listen to songs on an i-tree

## what is it then?

### something like an indexable tree

At some point I wanted a treelike structure with list-like access using indices. I'm not sure this
is necessarily a good idea, but I tried to do it anyways.
I noticed I could probably get away with using 2 indices, a vertical index (depth) and a horizontal
index (width). Those two numbers should uniquely identify a node in the tree if we use:

	* depth = distance from root to "lowest" leaf node
	* width = number of nodes away from last node on the left on that level

So here it is.

## how is it implemented?

Well, it's pretty obvious that you might as well use an array of arrays of dynamic size to store the nodes.
That way the nodes are indexable using 2 indices. Nodes of course, have to contain pointers to a parent
node and their child nodes in order to represent the treeish information.

But we can probably do better than that, since we could encode the tree information as functions of the array
indices. We can use each row in the outer array to represent a level of the tree
starting from the root. That way we know that if we are on level i, our parent is necessarily on level i-1 and our
children on i+1. That way we can get away with only storing one index for the parent and the children, namely
the width (\# nodes away from last node on the left).
