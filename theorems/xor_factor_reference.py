"""Capped exact integer sum-product reference for public XOR Ising inputs.

Classical variable elimination, not a new algorithm. Exponential treewidth
costs are exposed. A cap failure is UNKNOWN, never a hardness certificate.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
import hashlib
from pathlib import Path

import networkx as nx
import numpy as np

from theorems.bpqm_gibbs_frontier import integer, rational


class FactorReferenceLimit(RuntimeError):
    pass


@dataclass(frozen=True)
class ConditionalTable:
    variable: int
    scope: tuple[int, ...]
    values: np.ndarray


class ExactXorReference:
    def __init__(self, model, overlap, *, query_bit=0, max_entries=1 << 20,
                 total_entry_budget=1 << 23):
        self.model = model
        self.c = rational(overlap)
        if not 0 <= self.c < 1:
            raise ValueError("finite nonnegative temperature required")
        integer(query_bit, "query spin", 0, model.spins-1)
        integer(max_entries, "factor entry cap", 2, 1 << 24)
        integer(total_entry_budget, "total factor entry budget", 2, 1 << 27)
        self.query_bit = query_bit
        self.tables = []
        self.draw_bits = []
        self.entries = 0
        self.peak_entries = 0
        graph = nx.Graph()
        graph.add_nodes_from(range(model.spins))
        supports = []
        for mask, _ in model.clauses:
            scope = tuple(j for j in range(model.spins) if (mask >> j) & 1)
            supports.append(scope)
            graph.add_edges_from(combinations(scope, 2))
        width, decomposition = nx.approximation.treewidth_min_fill_in(graph)
        tree = decomposition.copy()
        remaining = set(graph)
        order = []
        while len(tree) > 1:
            leaf = next(bag for bag in tree if tree.degree(bag) == 1)
            parent = next(iter(tree.neighbors(leaf)))
            remove = sorted((set(leaf)-set(parent)) & remaining)
            order.extend(remove)
            remaining.difference_update(remove)
            tree.remove_node(leaf)
        order.extend(sorted(remaining))
        if sorted(order) != list(range(model.spins)):
            raise ArithmeticError("tree-decomposition elimination order lost a spin")
        # Keep a selected public observable last for its exact marginal.
        order.remove(query_bit)
        order.append(query_bit)
        self.order = tuple(order)
        self.heuristic_treewidth_upper = width

        def reserve(entries):
            if entries > max_entries or self.entries+entries > total_entry_budget:
                raise FactorReferenceLimit("UNKNOWN: exact factor reference entry cap; no hardness conclusion")
            self.entries += entries
            self.peak_entries = max(self.peak_entries, entries)

        a, b = self.c.numerator, self.c.denominator
        factors = []
        for scope, (_, sign) in zip(supports, model.clauses):
            reserve(1 << len(scope))
            values = np.empty((2,)*len(scope), dtype=object)
            for bits in product((0, 1), repeat=len(scope)):
                values[bits] = b+a if sum(bits) % 2 == sign else b-a
            factors.append((scope, values))
        for variable in order:
            bucket = [(scope, values) for scope, values in factors if variable in scope]
            factors = [(scope, values) for scope, values in factors if variable not in scope]
            scope = tuple(sorted({variable} | {j for local, _ in bucket for j in local}))
            reserve(1 << len(scope))
            combined = np.ones((2,)*len(scope), dtype=object)
            for local, values in bucket:
                shape = tuple(2 if j in local else 1 for j in scope)
                combined *= values.reshape(shape)
            if any(type(v) is not int or v <= 0 for v in combined.flat):
                raise ArithmeticError("nonpositive or noninteger Gibbs factor")
            self.tables.append(ConditionalTable(variable, scope, combined))
            self.draw_bits.append(max(int(v).bit_length() for v in combined.flat)+1)
            message_scope = tuple(j for j in scope if j != variable)
            reserve(1 << len(message_scope))
            message = np.asarray(combined.sum(axis=scope.index(variable)), dtype=object)
            factors.append((message_scope, message))
        if any(scope for scope, _ in factors):
            raise ArithmeticError("uneliminated factor scope")
        self.partition_integer = 1
        for _, values in factors:
            self.partition_integer *= int(values.item())
        last = self.tables[-1]
        if last.scope != (query_bit,):
            raise ArithmeticError("selected last spin has an unexpected scope")
        p0, p1 = map(int, last.values)
        self.query_parity_mean = Fraction(p0-p1, p0+p1)

    @staticmethod
    def _conditional(table, word):
        indices = [(word >> j) & 1 for j in table.scope]
        position = table.scope.index(table.variable)
        indices[position] = 0
        zero = int(table.values[tuple(indices)])
        indices[position] = 1
        one = int(table.values[tuple(indices)])
        return zero, one

    def probability(self, word):
        integer(word, "reference word", 0, (1 << self.model.spins)-1)
        result = Fraction(1)
        for table in reversed(self.tables):
            zero, one = self._conditional(table, word)
            result *= Fraction(one if (word >> table.variable) & 1 else zero, zero+one)
        return result

    def sample(self, rng):
        word = 0
        for table in reversed(self.tables):
            zero, one = self._conditional(table, word)
            if rng.randrange(zero+one) >= zero:
                word |= 1 << table.variable
        return word

    def ledger(self):
        return {"method": "exact_integer_bucket_elimination_and_backward_sampling",
                "spins": self.model.spins, "clauses": len(self.model.clauses),
                "overlap_c_exact": str(self.c), "query_parity_mask_hex": hex(1 << self.query_bit),
                "query_parity_mean_exact": str(self.query_parity_mean),
                "partition_for_product_integer_factors": str(self.partition_integer),
                "heuristic_treewidth_upper_not_lower_bound": self.heuristic_treewidth_upper,
                "largest_bucket_variables": max(len(t.scope) for t in self.tables),
                "peak_single_factor_entries": self.peak_entries, "factor_entries_materialized": self.entries,
                "entry_counts_are_cumulative_not_peak_memory_bytes": True,
                "full_word_table_materialized": self.peak_entries == 1 << self.model.spins,
                "uniform_randrange_calls_per_sample": self.model.spins,
                "expected_uniform_bits_per_sample_upper_for_rejection_rng": 2*sum(self.draw_bits),
                "exact_sampling_law_assumes_uniform_randrange": True,
                "cost_exponential_in_elimination_width": True, "polynomial_general_algorithm_claimed": False,
                "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "networkx_version": nx.__version__}
