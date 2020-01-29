import msa
import numpy as np
from numpy.testing import assert_allclose


coords = np.array([[0, 0], [1, 0], [1, 1]])
ien = np.array([[0, 1], [0, 2]])
props = np.array([[1, 1], [1, 1]])
P = np.array([0., -1., 'unk', 'unk', 'unk', 'unk'])
u = np.array(['unk', 'unk', 0., 0., 0., 0.])
mymsa = msa.MSA_truss(coords, ien, props, u, P)

def test_solve():
    u_solved, P_solved = mymsa.solve() 
    assert_allclose(u_solved, [1.0, -3.828427])
    assert_allclose(P_solved, [-1.       ,  0.       ,  0.9999999,  0.9999999])
    #assert u_solved == 