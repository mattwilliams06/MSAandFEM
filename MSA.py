import numpy as np

class MSA_truss:
    ''' This is a class of methods to perform Matrix Structural Analysis on 2D trusses using the direct stiffness method. 
    The limitations are the truss contain only pin-type joints, and that each member has joints only at the ends. 
    The user must specify inputs in a particular way, which will be described in this doctring.

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

    Methods
    -------

    This class contains the following methods:

    Ke_truss: generates a list of element stiffness matrices.

    KG: generates the global stiffness matrix by assembling all element stiffness matrices in the global coordinate system.
    
    partition: partitions the global stiffness matrix and the force and displacement vectors based on the locations of the
    'unk' entries in both the force and displacement vectors.

    solve: solves the system for the unknown forces and displacements. This is the only method that needs to be called. All other
    methods are implemented when calling solve.

    Returns
    -------

    The solve method returns the array of unknown displacements and the array of unknown forces. The entries in each array are
    in order of node numbering. For example, if there were unknown displacements at degrees of freedom 3, 4, 7, and 8, the returned
    array will be the displacements of those DOFs, respectively.

    Negative displacements are displacements in the negative x and y-directions (left and down). Positive forces indicate an 
    element is in tension, while negative forces indicate the member is in compression.

    This implementation of MSA is based on the methodology found in _An Introduction to Matrix Structural Analysis and
    Finite Element Methods_ by Jean Provost and Serguei Bagrianski.

    Author: Matt Williams, matthew.j.williams@protonmail.com.
    '''
    def __init__(self, coords, ien, props, u, P):
        self.coords = coords
        self.ien = ien.astype(np.int8)
        self.props = props
        self.u = u
        self.P = P
        self.n_nodes = len(self.coords)
        self.n_elements = len(self.ien)
        self.ind = np.zeros((self.n_nodes, 2), dtype=np.int8)
        self.ied = np.zeros((self.n_elements, 2, 2), dtype=np.int8)
    # Create indices for the degrees of freedom, two per node
    # Also create an matrix for the degree of freedom indices for each element

    def Ke_truss(self):
        ''' Generate the truss element stiffness matrix.
        Inputs
        ------
        
        xe: list of component-lengths for truss element. For example, a 5m member inclined at 32.9 deg will have
        xe elements of 4m and 3m. The same member inclined at zero degrees will have 5m and 0m.
        prop: list of properties [Young's modulus, cross-sectional area]
        '''
        # elem_idx -= 1 # adjusting for element numberings that begin with 1
        for elem_idx in range(self.n_elements):
            for i in range(self.n_nodes):
                self.ind[i, 0] = i * 2
                self.ind[i, 1] = i * 2 + 1
        
        for i in range(self.n_elements):
            self.ied[i, 0] = self.ind[self.ien[i, 0]]
            self.ied[i, 1] = self.ind[self.ien[i, 1]]

        Ke_all = []
        for elem_idx in range(self.n_elements):
            nx = (self.coords[self.ien[elem_idx, 1], 0] - self.coords[self.ien[elem_idx, 0], 0])
            ny = (self.coords[self.ien[elem_idx, 1], 1] - self.coords[self.ien[elem_idx, 0], 1])
            #print(nx, ny)
            L = np.linalg.norm([nx, ny])
            #print(L)
            T = np.zeros((2, 4), dtype=np.float32)
            T[0, :2] = [nx, ny] / L
            T[1, 2:] = [nx, ny] / L
            #print(T)
            E = self.props[elem_idx, 0]
            A = self.props[elem_idx, 1]
            
            # Local stiffness matrix
            k = np.array([[1., -1.], [-1., 1.]])
            k *= E*A/L
            
            # Global element stiffness matrix
            Ke = T.T @ k @ T
            Ke_all.append(Ke)
            
        return Ke_all


    def KG(self):
        ''' Assemble the global stiffness matrix from a tensor of the element stiffness matrices.
    For this 2D code, each element is associated with 2 nodes at each end. The tensor of 
    element stiffness matrices is of shape (num_elements, dof, dof) where dof is the number
    of degrees of freedom per element (4 in this case).
    '''
        Ke = self.Ke_truss()
        #print('Ke: ', Ke)
        Kg = np.zeros((self.n_nodes * 2, self.n_nodes * 2), dtype=np.float32)
        #print('Kg initialized: ', Kg)
        # assigning the entries of Ke to the locations in KG corresponding to the DOF at each
        # node in the element.
        for element in range(self.n_elements):
            for row in range(4):
                for col in range(4):
                    idx = self.ied[element].flatten()
                    Kg[idx[row], idx[col]] += Ke[element][row, col]
        return Kg


    def partition(self):
        ''' Partition the stiffness matrix based on the DOF locations of the known forces. 
        Degrees of freedom containing unknown forces or displacements should contain the string "unk"
        '''
        # Indices for natural and essential boundary conditions, respectively.
        Kg = self.KG()
        U_idx = self.P != 'unk'
        S_idx = self.P == 'unk'
    
        Pu = self.P[U_idx].astype(np.float32)
        du = self.u[U_idx]
        ds = self.u[S_idx].astype(np.float32)
        Kuu = Kg[np.ix_(U_idx, U_idx)]
        Kus = Kg[np.ix_(U_idx, S_idx)]
        Ksu = Kg[np.ix_(S_idx, U_idx)]
        Kss = Kg[np.ix_(S_idx, S_idx)]
    
        return Pu, ds, Kuu, Kus, Ksu, Kss


    def solve(self):
        Pu, ds, Kuu, Kus, Ksu, Kss = self.partition()
        du = np.linalg.inv(Kuu) @ (Pu - Kus @ ds)
        Rs = Ksu @ du + Kss @ ds

        return du, Rs

