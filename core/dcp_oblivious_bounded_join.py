"""Reversible bounded equijoin using fixed-address sorts, scans and requests.

Classical oblivious-join technique, with all histories retained and reversed.
No QRAM, hardware gates, quantum acceleration, or novelty is claimed.
"""
from __future__ import annotations

from dcp_balanced_pairing import sort_records, unsort_records


def _integer(v, name, lower=0):
    if type(v) is not int or v < lower:
        raise ValueError(name + " must be a canonical integer")


class _Tape:
    """Only fixed-address array computes, bitonic sorts and prefix scans."""
    def __init__(self):
        self.ops = []
        self.metrics = {"record_evaluations": 0, "comparators": 0, "scan_steps": 0}
        self.live_bits = 0
        self.peak_bits = 0

    def _charge(self, bits):
        self.live_bits += bits
        self.peak_bits = max(self.peak_bits, self.live_bits)

    def compute(self, factory, fields, bits):
        records = list(factory())
        if any(len(r) != fields or any(type(v) is not int or not 0 <= v < 1 << bits for v in r) for r in records):
            raise ArithmeticError("record exceeds its declared wire width")
        self.metrics["record_evaluations"] += len(records)
        charged = len(records) * fields * bits
        self._charge(charged)
        self.ops.append(("compute", records, factory, charged))
        return records

    def sort(self, records):
        flags = sort_records(records)
        self.metrics["comparators"] += len(flags)
        self._charge(len(flags))
        self.ops.append(("sort", records, flags, len(flags)))

    def scan(self, records, initial, step, bits):
        states = [initial]
        for i, record in enumerate(records):
            states.append(step(states[-1], record, i))
        if any(any(type(v) is not int or not 0 <= v < 1 << bits for v in state) for state in states):
            raise ArithmeticError("scan exceeds its declared wire width")
        self.metrics["scan_steps"] += len(records)
        charged = len(states)*len(initial)*bits
        self._charge(charged)
        self.ops.append(("scan", records, states, initial, step, charged))
        return states

    def reverse(self):
        for op in reversed(self.ops):
            if op[0] == "compute":
                _, records, factory, charged = op
                expected = list(factory())
                if len(expected) != len(records):
                    raise ArithmeticError("data-dependent allocation during reversal")
                for i, record in enumerate(expected):
                    records[i] = tuple(a ^ b for a, b in zip(records[i], record))
                if any(any(record) for record in records):
                    raise ArithmeticError("record compute did not uncompute")
                self.metrics["record_evaluations"] += len(records)
            elif op[0] == "sort":
                _, records, flags, charged = op
                self.metrics["comparators"] += unsort_records(records, flags)
                if flags:
                    raise ArithmeticError("sorting history not clean")
            else:
                _, records, states, initial, step, charged = op
                for i in range(len(records)-1, -1, -1):
                    states[-1] = tuple(a ^ b for a, b in zip(states[-1], step(states[-2], records[i], i)))
                    if any(states.pop()):
                        raise ArithmeticError("scan history did not uncompute")
                states[0] = tuple(a ^ b for a, b in zip(states[0], initial))
                if any(states[0]):
                    raise ArithmeticError("scan initialization not clean")
                self.metrics["scan_steps"] += len(records)
            self.live_bits -= charged
        self.ops.clear()
        if self.live_bits:
            raise ArithmeticError("live work remains after tape reversal")


def schedule(left_slots, right_slots, capacity, key_bits, payload_bits):
    for v, name in ((left_slots, "left slots"), (right_slots, "right slots"),
                    (capacity, "capacity"), (key_bits, "key bits"), (payload_bits, "payload bits")):
        _integer(v, name, 1)
    C = min(capacity, left_slots*right_slots)
    P = 1 << (left_slots+right_slots-1).bit_length()
    R = 1 << (P+C-1).bit_length()
    F = 1 << (P+2*R-1).bit_length()
    # One uniform wire width simplifies the conservative storage certificate.
    bits = max(key_bits+1, payload_bits, (left_slots*right_slots+C+P+F+1).bit_length())
    sorts = [P, R, F, F]
    cmp = sum(s*(s.bit_length()-1)*s.bit_length()//4 for s in sorts)
    scans = 2*P + R + F
    computes = P + P + R + 2*R + F + F
    workspace = bits*(5*P + 5*(P+1) + 8*P + (P+1) + 8*R + 6*(R+1)
                      + 5*2*R + 5*F + 2*(F+1) + 3*F) + cmp
    return {"left_slots": left_slots, "right_slots": right_slots, "capacity": capacity,
            "output_slots": C, "input_sort_slots": P, "rank_sort_slots": R,
            "fetch_sort_slots": F, "record_field_bits": bits,
            "sort_sizes": sorts, "comparators": 2*cmp, "scan_steps": 2*scans,
            "record_evaluations": 2*computes, "persistent_workspace_bits": workspace,
            "time_and_coherent_storage_form": "O((left_slots+right_slots+capacity)*log^2(left_slots+right_slots+capacity)*poly(record_bits))",
            "data_dependent_RAM_reads": False, "whole_attempt_overflow_rejection": True,
            "hardware_gate_export_implemented": False}


def join_xor(left, right, capacity, key_bits, payload_bits, target=None, overflow_target=0):
    """Rows are(valid,key,payload); all matching row PAIRS, never deduplicated.

    Returns XOR target plus an overflow XOR wire. Count is a basis diagnostic,
    not an additional free coherent count oracle or an error-label register.
    """
    S = schedule(len(left), len(right), capacity, key_bits, payload_bits)
    C, P, R, F, bits = (S[k] for k in ("output_slots", "input_sort_slots", "rank_sort_slots", "fetch_sort_slots", "record_field_bits"))
    if F > 65536 or key_bits > 4096 or payload_bits > 4096:
        raise ValueError("UNKNOWN: explicit oblivious-join interpreter work cap")
    left, right = tuple(tuple(r) for r in left), tuple(tuple(r) for r in right)
    for row in left+right:
        if len(row) != 3 or any(type(v) is not int for v in row) or row[0] not in (0, 1) or not 0 <= row[1] < 1 << key_bits or not 0 <= row[2] < 1 << payload_bits:
            raise ValueError("canonical valid/key/payload row required")
    if target is None:
        target = [(0, 0, 0)]*C
    target = list(tuple(r) for r in target)
    if len(target) != C or any(len(r) != 3 or any(type(v) is not int for v in r) or r[0] not in (0, 1) or any(not 0 <= v < 1 << payload_bits for v in r[1:]) for r in target):
        raise ValueError("fixed-size canonical XOR target wires required")
    if type(overflow_target) is not int or overflow_target not in (0, 1):
        raise ValueError("overflow XOR target must be a bit")
    tape = _Tape()
    sentinel = 1 << key_bits
    def source():
        for side, rows in enumerate((left, right)):
            for j, (valid, key, payload) in enumerate(rows):
                yield (key, side, j, payload, 1) if valid else (sentinel, 2, j, 0, 0)
        for _ in range(P-len(left)-len(right)):
            yield sentinel, 2, 0, 0, 0
    rows = tape.compute(source, 5, bits)
    tape.sort(rows)
    def group_step(state, row, i):
        prev, nl, nr, ls, rs = state
        key, side, _, _, valid = row
        if key != prev:
            nl = nr = ls = rs = 0
        if valid and side == 0:
            if nl == 0:
                ls = i
            nl += 1
        if valid and side == 1:
            if nr == 0:
                rs = i
            nr += 1
        return key, nl, nr, ls, rs
    groups = tape.scan(rows, (0, 0, 0, 0, 0), group_step, bits)
    # Count a group once, at its fixed-position end; preserve every prefix.
    pair_prefix = tape.scan(rows, (0,), lambda state, row, i: (
        state[0] + (groups[i+1][1]*groups[i+1][2] if i+1 == P or rows[i+1][0] != row[0] else 0),), bits)
    count = pair_prefix[-1][0]
    rank_sentinel = len(left)*len(right)+C+1
    def descriptors():
        for i in range(P):
            start, end = pair_prefix[i][0], pair_prefix[i+1][0]
            _, nl, nr, ls, rs = groups[i+1]
            yield (start, 0, end, ls, rs, nr, 0, 1) if end > start else (rank_sentinel, 2, 0, 0, 0, 0, 0, 0)
    desc = tape.compute(descriptors, 8, bits)
    def rank_input():
        yield from desc
        for j in range(C):
            yield j, 1, 0, 0, 0, 0, j, 1
        for _ in range(R-P-C):
            yield rank_sentinel, 2, 0, 0, 0, 0, 0, 0
    ranks = tape.compute(rank_input, 8, bits)
    tape.sort(ranks)
    def rank_step(state, row, i):
        start, side, end, ls, rs, nr, _, valid = row
        return (start, end, ls, rs, nr, valid) if side == 0 else state
    rank_state = tape.scan(ranks, (0, 0, 0, 0, 0, 0), rank_step, bits)
    def request_input():
        for i, row in enumerate(ranks):
            j, side, _, _, _, _, out, _ = row
            start, end, ls, rs, nr, valid = rank_state[i+1]
            enabled = int(side == 1 and bool(valid) and start <= j < end)
            # Addresses are DATA FIELDS. Never index a source array with them.
            offset = j-start if enabled else 0
            indices = (ls+offset//nr, rs+offset%nr) if enabled else (0, 0)
            for branch, index in enumerate(indices):
                yield index, 1, 2*out+branch if side == 1 else 2*C, enabled, 0
    requests = tape.compute(request_input, 5, bits)
    def fetch_input():
        for i, row in enumerate(rows):
            yield i, 0, 0, 0, row[3]
        yield from requests
        for _ in range(F-P-2*R):
            yield P, 2, 2*C, 0, 0
    fetch = tape.compute(fetch_input, 5, bits)
    tape.sort(fetch)
    carry = tape.scan(fetch, (0, 0), lambda state, row, i: (row[0], row[4]) if row[1] == 0 else state, bits)
    def response_input():
        for i, row in enumerate(fetch):
            _, side, out, enabled, _ = row
            if side == 1 and out < 2*C:
                yield out, enabled, carry[i+1][1] if enabled else 0
            else:
                yield 2*C, 0, 0
    responses = tape.compute(response_input, 3, bits)
    tape.sort(responses)
    overflow = int(count > capacity)
    for j in range(C):
        a, b = responses[2*j], responses[2*j+1]
        if a[0] != 2*j or b[0] != 2*j+1 or a[1] != b[1]:
            raise ArithmeticError("oblivious request routing failed")
        answer = (a[1], a[2], b[2]) if not overflow else (0, 0, 0)
        target[j] = tuple(v ^ w for v, w in zip(target[j], answer))
    overflow_target ^= overflow
    tape.reverse()
    for key in tape.metrics:
        if tape.metrics[key] != S[key]:
            raise ArithmeticError("fixed schedule cost mismatch: "+key)
    if tape.peak_bits != S["persistent_workspace_bits"]:
        raise ArithmeticError("retained history storage mismatch")
    return {"target": target, "overflow_output": overflow_target, "workspace_clean": True,
            "basis_pair_count_diagnostic": count, "schedule": S, "metrics": tape.metrics}
