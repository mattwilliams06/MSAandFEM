# Matrix Structural Analysis and Finite Element Methods

This repository contains msa.py, which implements Matrix Structural Analysis using the direct stiffness methods on 2-dimensional trusses in Python. The analysis is limited to structures which are pin or roller joined, with one joint per end. The required inputs are a matrix of node/joint coordinates, an index of which nodes belong to each element, an array of the known and unknown displacements, an array of the known and unknown forces, and an array containing material properties for each element, specifically Young's Modulus and cross-sectional area.

## Example Demonstrating the Inputs

To demonstrate the required inputs, consider the ![truss shown here](https://github.com/mattwilliams06/MSAandFEM/blob/master/truss1.png) The truss has 5 elements and 4 nodes/joints. The truss is also pinned in two locations. Indices will start at zero, as is the convention in computer programming languages. Numbering the nodes, node 0 is the location of the pinned node in the lower left corner, node 1 is the node at the directly to the right from node 0 (across the bottom horizontal member), node 2 is the node directly upward from node 1, and node 3 is the pinned node at the upper right corner of the truss. We can now develop the coordinates array from this information. Using a 2D array where each row is a node, the coordinates array will be

 'np.array([[0, 0], [4, 0], [4, 3], [8, 3]])' 

if working in meters.

Numbering the truss elements, element 0 is the lower horizontal bar, element 1 is the sloped element on the left, element 2 is the vertical element, element 3 is the sloped element on the right, and element 4 is the upper horizontal element. The index of element nodes (IEN) is an array containing the node numbers for each element. We can see that element zero is attached to nodes 0 and 1, etc. In this case, the IEN will be 

'np.array([[0, 1], [0, 2], [1, 2], [1, 3], [2, 3]])'

The program will automatically assign degree of freedom indices to each node based on the node number. Node 0 will have degrees of freedom 0 and 1 for the x and y-directions respectively. Node 1 will have DOFs 2 and 3, and so on.

For the properties array, each row contains the Young's Modulus and cross-sectional area for the associated element. If each element has a Young's Modulus of 200,000 MPa, and taking the cross-sectional areas from the picture, the property array will be 

'np.array([[200000., 100.], [200000., 200.], [200000., 100.], [200000., 200.], [200000., 100.]])'

The displacements array will have known entries due to prescribed displacements and essential boudary conditions. There needs to be one entry per degree of freedom. If a DOF has an unknown displacement, the entry should be the string 'unk'. From the diagram, we can see that node 0 has a prescribed displacement of 4 mm in the negative direction for DOF 0. Due to the boundary conditions, DOFs 1, 6, and 7 will have 0 displacement. All others are unknown. The displacement array is therefore 

'np.array([-4, 0, 'unk', 'unk', 'unk', 'unk', 0, 0])'

The force array is similar. Reaction forces will be unknown typically, and the prescribed forces at various nodes will be known. There is one prescribed force in the diagram at node 2 in the negative y-direction (negative DOF 5.). There are no applied loads at DOFs 2, 3, or 4. DOFs 0, 1, 6, and 7 will be the unknown reaction forces. The force vector is therefore 

'np.array(['unk', 'unk', 0., 0., 0., -9000., 'unk', 'unk'])'

These vectors serve as the input to MSA_truss when first creating an instance of the class. Then, the solve method only needs to be called. The output will be the unkown values that were solved for, in order of DOF index number.