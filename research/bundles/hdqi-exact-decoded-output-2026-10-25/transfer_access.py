"""Constructed exact sample/amplitude access, never an assumed amplitude oracle."""

from itertools import product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"hdqi-ecf-tree-sampler-2026-10-25"))
from tree_sampler import TreeSampler, conjugate, fraction, gaussian


class TransferAccess:
    def __init__(self, decomposition, couplings, parameters, *, max_pair_states=2_000_000):
        self.sampler = TreeSampler(decomposition, couplings, parameters,
                                   max_pair_states=max_pair_states)
        self.decomposition = decomposition
        self.couplings, self.parameters = self.sampler.couplings, self.sampler.parameters
        self.m, self.layers = decomposition.size, len(self.parameters)
        self.norm_squared = self.sampler.norm_squared
        self._rows = self._amplitude_rows()
        self.resources = {**self.sampler.resources,
                          "amplitude_bag_states": sum(len(masks)**self.layers
                                                      for masks in decomposition.independent_masks),
                          "amplitude_oracle_assumed": False}

    def _amplitude_rows(self):
        d, result = self.decomposition, []
        for bag_index, masks in enumerate(d.independent_masks):
            rows = []
            for selections in product(masks, repeat=self.layers):
                weight, parity = gaussian(1), 0
                for v in d.owned_vertices[bag_index]:
                    selected = [l for l, mask in enumerate(selections) if mask >> v & 1]
                    parity |= (len(selected) % 2) << v
                    for l in selected:
                        weight *= -self.parameters[l]*gaussian(self.couplings[v])
                crossings = sum(bool(selections[p] >> i & 1) and bool(selections[q] >> j & 1)
                                for i, j in d.owned_edges[bag_index]
                                for p in range(self.layers) for q in range(p))
                if crossings % 2:
                    weight = -weight
                if weight:
                    parent = tuple(mask & d.separators[bag_index] for mask in selections)
                    children = tuple(tuple(mask & d.separators[child] for mask in selections)
                                     for child in d.children[bag_index])
                    rows.append((parent, children, parity, weight))
            result.append(tuple(rows))
        return tuple(result)

    def amplitude(self, word):
        if type(word) is not int or not 0 <= word < 1 << self.m:
            raise ValueError("native m-bit word required")
        d, messages = self.decomposition, {}
        for bag_index in reversed(d.order):
            required = word & sum(1 << v for v in d.owned_vertices[bag_index])
            table = {}
            for parent, children, parity, weight in self._rows[bag_index]:
                if parity != required:
                    continue
                value = weight
                for child, key in zip(d.children[bag_index], children):
                    value *= messages[child].get(key, gaussian(0))
                    if not value:
                        break
                if value:
                    table[parent] = table.get(parent, gaussian(0))+value
            messages[bag_index] = table
        return messages[0].get((0,)*self.layers, gaussian(0))

    def probability(self, word):
        amplitude = self.amplitude(word)
        return fraction((amplitude*conjugate(amplitude)).x)/self.norm_squared

    def sample(self, rng):
        return sum(bit << i for i, bit in enumerate(self.sampler.sample(rng)))
