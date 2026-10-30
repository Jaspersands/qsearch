from itertools import combinations, product

from flint import nmod_mat
import pytest

import flat_optimality as f


@pytest.mark.parametrize("p,K",[(19,5),(31,9),(43,12)])
def test_native_flats_saturate_all_base_field_bound(p,K):
    row = f.native_control(p,K)
    assert row["dimension"] == row["all_Fp_linear_flat_dimension_bound"]
    assert row["projection_rank"] == row["dimension"]
    assert row["signed_determinant_square_class"] == (1 if row["active_blocks"]%2==0 else p-1)


def test_non_extension_linear_subspace_does_not_need_theta_closure():
    row = f.native_control(19,5,remove_last=True)
    assert not row["theta_closed"]
    assert row["dimension"] == row["projection_rank"] == 3


def test_every_dual_root_choice_projects_injectively():
    for roots in combinations(range(6),2):
        row = f.native_control(19,5,roots=roots)
        assert row["projection_rank"] == 4
        assert len(row["active_indices"]) == 4


@pytest.mark.parametrize("p,K,target_K",[(31,9,8),(43,12,10)])
def test_optimal_flat_exists_even_when_completion_rank_gate_fails(p,K,target_K):
    row = f.native_control(p,K,target_K=target_K)
    assert row["dimension"] == row["all_Fp_linear_flat_dimension_bound"]
    assert row["dimension"] < row["parity_rank"]
    assert not row["full_row_rank_completion_possible_by_dimension"]


def test_odd_active_block_count_really_excludes_one_more_dimension():
    row = f.native_control(43,12)
    assert row["active_blocks"] == 9
    assert row["all_Fp_linear_flat_dimension_bound"] == 8
    assert row["signed_determinant_square_class"] == 42


def test_main_point_eight_case_stays_unresolved_not_hard():
    row = f.dimension_bound(4096,2460)
    assert row["all_Fp_linear_flat_dimension_bound"] == 1636
    assert not row["full_row_rank_completion_possible_by_dimension"]
    assert "hardness" not in row


def test_anisotropy_is_essential_not_an_implementation_convenience():
    # With nu=1, independent vectors x_i=y_i give an M-dimensional common
    # flat, contradicting the nonsquare bound and its support lemma.
    p,M,r = 19,6,3
    identity = [[int(i==j) for j in range(M)] for i in range(M)]
    basis = identity+identity
    nodes,weights = list(range(1,7)),[1]*6
    assert nmod_mat(basis,p).rank() > f.dimension_bound(M,r)["all_Fp_linear_flat_dimension_bound"]
    for j in range(r):
        diagonal = [pow(c,j,p) for c in nodes]
        diagonal += [-v%p for v in diagonal]
        assert not any(f.restricted_gram(basis,diagonal,p).entries())
    with pytest.raises(ValueError,match="anisotropic"):
        f.certificate(p,nodes,weights,1,r,basis)


def test_nonsquare_norm_support_equals_block_support_exhaustively():
    for p,nu in [(7,3),(19,2),(31,3)]:
        assert pow(nu,(p-1)//2,p)==p-1
        for x,y in product(range(p),repeat=2):
            assert ((x*x-nu*y*y)%p==0) == (x==y==0)


def test_pairwise_gram_check_catches_false_basis_only_flat():
    # In a split plane, both coordinate basis vectors have zero quadratic
    # value but their sum does not. Full Gram testing must catch the pair.
    basis = [[1,1],[1,18]]
    gram = f.restricted_gram(basis,[1,18],19)
    assert gram[0,0] == gram[1,1] == 0
    assert gram[0,1] != 0


@pytest.mark.parametrize("mutation",["duplicate_node","zero_weight","dependent_basis","broken_basis","duplicate_root"])
def test_invalid_or_nonflat_certificate_is_rejected(mutation):
    row = f.native_control(19,5)
    nodes,weights,basis,roots = row["nodes"],row["weights"],row["basis"],row["root_indices"]
    if mutation=="duplicate_node":
        nodes[1]=nodes[0]
    elif mutation=="zero_weight":
        weights[0]=0
    elif mutation=="dependent_basis":
        basis=[r+[r[0]] for r in basis]
    elif mutation=="broken_basis":
        basis[0][0]=(basis[0][0]+1)%19
    else:
        roots=[0,0]
    with pytest.raises(ValueError):
        f.certificate(19,nodes,weights,row["nu"],3,basis,roots)
