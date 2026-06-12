import search_engine

def run_simulation(problem_proposal: dict, N: int) -> dict:
    """
    Executes the theorist's code to dynamically create the oracle and secrets generator
    for a given number of qubits N, then runs the circuit search.
    """
    local_ns = {}
    
    # We execute all definitions in local_ns
    exec(problem_proposal['base_function_code'], globals(), local_ns)
    exec(problem_proposal['oracle_generator_code'], globals(), local_ns)
    exec(problem_proposal['secrets_generator_code'], globals(), local_ns)
    
    # Extract functions
    make_oracle = local_ns.get('make_oracle')
    if not make_oracle:
        for k, v in local_ns.items():
            if callable(v) and ('oracle' in k or 'make' in k):
                make_oracle = v
                break
                
    get_secrets = local_ns.get('get_secrets')
    if not get_secrets:
        for k, v in local_ns.items():
            if callable(v) and ('secret' in k or 'get' in k):
                get_secrets = v
                break
                
    # Extract search options from problem proposal
    gates_to_use = problem_proposal.get('gates_to_use', ['H', 'I'])
    max_queries = problem_proposal.get('max_queries', 1)
    requires_linear_solver = problem_proposal.get('requires_linear_solver', False)
    
    # Run circuit search
    rate, config = search_engine.search_circuits(
        N, problem_proposal,
        gates_to_use=gates_to_use,
        max_queries=max_queries,
        requires_linear_solver=requires_linear_solver
    )
    
    if config:
        pre_gates, post_gates, mid_gates, mapping = config
        depth, gate_counts = search_engine.get_circuit_properties(
            N, pre_gates, post_gates, mid_gates, max_queries
        )
    else:
        pre_gates, post_gates, mid_gates, mapping = None, None, None, None
        depth, gate_counts = 0, {}
        
    return {
        'success_rate': rate,
        'pre_gates': pre_gates,
        'post_gates': post_gates,
        'mid_gates': mid_gates,
        'mapping': mapping,
        'depth': depth,
        'gate_counts': gate_counts
    }

