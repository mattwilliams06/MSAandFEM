# Matrix Structural Analysis and Finite Element Methods

This repository contains msa.py, which implements Matrix Structural Analysis using the direct stiffness methods on 2-dimensional trusses in Python. The analysis is limited to structures which are pin or roller joined, with one joint per end. The required inputs are a matrix of node/joint coordinates, an index of which nodes belong to each element, an array of the known and unknown displacements, an array of the known and unknown forces, and an array containing material properties for each element, specifically Young's Modulus and cross-sectional area.

## Example Demonstrating the Inputs

To demonstrate the required inputs, consider the ![truss shown here](https://github.com/mattwilliams06/MSAandFEM/blob/master/Truss1.jpg) 

The truss has 5 elements and 4 nodes/joints. The truss is pinned in two locations. Node/joint indices are shown in red, while element indices are shown in green. There are prescribed loads and displacements, which will be addressed further down this document.

Considering each node's location in a cartesian coordinate system, placing the origin at node 0, the coordinates array can be assembled. In millimeters, this array is:

```python
np.array([[0., 0.], [4000., 0.], [4000., 3000.], [8000., 3000.]])
``` 

Each element's coordinates are stored along axis 0.

The index of element nodes (IEN) matrix can also be constructed, indicating which nodes are associated with each element. The ordering of the nodes for a particular element does not affect the solution. This array will be used to compute the element lengths and the direction cosines. The IEN matrix for the example truss is shown below.

```python
np.array([[0, 1], [0, 2], [1, 2], [1, 3], [2, 3]])
```

The program will automatically assign degree of freedom indices to each node based on the node number. Node 0 will have degrees of freedom 0 and 1 for the x and y-directions respectively. Node 1 will have DOFs 2 and 3, and so on. Therefore, element 0 is associated with degrees of freedom 0, 1, 2, and 3. Element 1 has degrees of freedom 0, 1, 4, and 5, and so on.

For the properties array, each row contains the Young's Modulus and cross-sectional area for the associated element. If each element has a Young's Modulus of 200,000 MPa, and taking the cross-sectional areas from the picture, the property array will be 

```python
np.array([[200000., 100.], [200000., 200.], [200000., 100.], [200000., 200.], [200000., 100.]])
```

The displacements array will have known entries due to prescribed displacements and essential boudary conditions. There needs to be one entry per degree of freedom. If a DOF has an unknown displacement, the entry should be the string 'unk'. From the diagram, we can see that node 0 has a prescribed displacement of 4 mm in the negative direction for DOF 0. Due to the boundary conditions, DOFs 1, 6, and 7 will have 0 displacement. All others are unknown. The displacement array is therefore 

```python
np.array([-4., 0., 'unk', 'unk', 'unk', 'unk', 0., 0.])
```

The force array is similar. Reaction forces will be unknown typically, and the prescribed forces at various nodes will be known. There is one prescribed force in the diagram at node 2 in the negative y-direction (negative DOF 5.). There are no applied loads at DOFs 2, 3, or 4. DOFs 0, 1, 6, and 7 will be the unknown reaction forces. The force vector is therefore 

```python
np.array(['unk', 'unk', 0., 0., 0., -9000., 'unk', 'unk'])
```

It should be noted there are no locations where both the displacement and the force are unknown. Generally, unless a problem is very contrived, wherever either the displacement or the force is unknown, the other will be prescribed. 

These vectors serve as the input to MSA_truss when first creating an instance of the class. Then, the solve method only needs to be called. The output will be the unkown values that were solved for, in order of DOF index number.