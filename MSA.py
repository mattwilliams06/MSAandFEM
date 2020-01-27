class MSA:
    ''' This is a class of methods to perform Matrix Structural Analysis on 2D trusses. The limitations are the truss
    contain only pin-type joints, and that each member has joints only at the ends. The user must specify inputs in a
    particular way, which will be spelled out in the docstring for each method.

    Inputs
    ------

    Note: The user can use whatever units they choose, so long as they will be compatible during computation.

    coords: a 2D array. This array contains the cartesian coordinates of each node, or joint. The first node should have 
    coordinates [0, 0]. For metric entries, the preferred units are millimeters.

    ien: a 2D array. This is a matrix of the indices of element nodes. It indexes which node numbers are associated with each member.
    The purpose is to map node coordinates to elements. For example, if the array of node coordinates were [[0, 0], [4000, 0], 
    [4000, 3000]], and a truss element had node 2 on one end and node 3 on the other, its entry in ien would be [1, 2], 
    and therefore the coordinates of each end of the member would be (4000, 0) and (4000, 3000) respectively.

    props: a 2D array. This array contains the Young's Modulus and cross-sectional area for each member. Units should be chosen such that
    they will be consistent through the computations. Preferred units are MPa and mm^2. For example, a member having Young's 
    Modulus of 200,000 MPa and a cross-sectional area of 100 mm^2 would have a props entry of [200000, 100].

    u = a 1D array. This array contains all known displacements (essential boundary conditions) and unknown displacements. Each
    node will have two displacements, one in the x and one in the y-directions. Unknown displacements should be entered as 'unk'.
    For example, a truss with 3 nodes that is pinned at both ends should have a u vector of [0, 0, 'unk', 'unk', 0, 0]. Preferred units
    are millimeters.

    P = a 1D array. This array contains all known and unknown forces (natural boundary conditions). Each node will have two entries 
    for forces in the x and y directions. For example, a truss with 3 nodes that is pinned at both ends and has a downward load of 
    9000 kN applied at node 3 will have a P vector of ['unk', 'unk', 0, -9000, 'unk', 'unk'].

    This implementation of MSA is based on the methodology found in _An Introduction to Matrix Structural Analysis and
    Finite Element Methods_ by Jean Provost and Serguei Bagrianski.

    Author: Matt Williams, matthew.j.williams@protonmail.com.
    '''


