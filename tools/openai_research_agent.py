#!/usr/bin/env python3
"""One owner-authorized, saved OpenAI research request; no tools or retries."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sys

from claude_research_agent import REPO_ROOT, SYSTEM, read_repository_text, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prompt-file', required=True)
    parser.add_argument('--context', action='append', default=[])
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--effort', choices=['high', 'max'], default='max')
    parser.add_argument('--max-tokens', type=int, default=48000)
    parser.add_argument('--max-budget-usd', type=Decimal, default=Decimal('3'))
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.max_tokens <= 128000:
        parser.error('Invalid output token limit')
    if not args.max_budget_usd.is_finite() or not 0 < args.max_budget_usd <= 142:
        parser.error('Invalid request budget')
    files = [read_repository_text(x) for x in [args.prompt_file, *args.context]]
    content = '\n\n'.join(f'FILE: {name}\n{data.decode()}' for name, data in files)
    # A conservative UTF-8-byte allowance, not a provider-enforced spend cap.
    allowance = len((SYSTEM + content).encode()) + 2048
    estimate = (Decimal(allowance) * 10 + Decimal(args.max_tokens) * 50) / 10**6
    if estimate > args.max_budget_usd:
        parser.error('Conservative preflight estimate exceeds request budget')
    bundle = args.output_dir.resolve()
    bundle.relative_to(REPO_ROOT.resolve())
    bundle.mkdir(parents=True, exist_ok=False, mode=0o700)
    request = dict(model='gpt-6-astra', instructions=SYSTEM, input=content,
                   reasoning={'effort': args.effort}, max_output_tokens=args.max_tokens,
                   store=False)
    write_json(bundle / 'request.json', request)
    for i, (_, data) in enumerate(files):
        (bundle / f'context-{i:02}.txt').write_bytes(data)
    result = dict(status='dry_run' if args.dry_run else 'running', billing_status='unknown',
                  started_at=datetime.now(timezone.utc).isoformat(), model=request['model'],
                  effort=args.effort, max_tokens=args.max_tokens,
                  max_budget_usd=str(args.max_budget_usd), preflight_estimate_usd=str(estimate),
                  price_source='https://developers.openai.com/api/docs/models/gpt-6-astra',
                  pricing_checked='2026-11-12', rates_usd_per_million={'input': 10, 'cached_input': 1, 'output': 50},
                  files=[{'path': name, 'sha256': hashlib.sha256(data).hexdigest()} for name, data in files],
                  cost_note='Usage estimate only; not invoice or account balance. No automatic retry.')
    write_json(bundle / 'result.json', result)
    if args.dry_run:
        print(json.dumps({'status': 'dry_run', 'preflight_estimate_usd': str(estimate)}))
        return 0
    from openai import OpenAI
    response = None
    try:
        client = OpenAI(max_retries=0, timeout=1800)
        with (bundle / 'response.md').open('w') as output:
            with client.responses.create(**request, stream=True) as stream:
                for event in stream:
                    if event.type == 'response.created':
                        result['response_id'] = event.response.id
                        write_json(bundle / 'result.json', result)
                    elif event.type == 'response.output_text.delta':
                        output.write(event.delta)
                        output.flush()
                    elif event.type in ('response.completed', 'response.incomplete', 'response.failed'):
                        response = event.response
        if response is None:
            raise RuntimeError('Stream ended without terminal response')
        raw = response.model_dump(mode='json')
        write_json(bundle / 'provider-response.json', raw)
        result.update(status=raw['status'], response_id=raw['id'], usage=raw.get('usage'),
                      incomplete_details=raw.get('incomplete_details'), error=raw.get('error'))
        if raw.get('usage'):
            u = raw['usage']
            cached = (u.get('input_tokens_details') or {}).get('cached_tokens', 0)
            charge = (Decimal(u['input_tokens'] - cached) * 10 + Decimal(cached) + Decimal(u['output_tokens']) * 50) / 10**6
            result.update(billing_status='usage_reported', usage_cost_estimate_usd=str(charge))
    except Exception as exc:
        # Do not log request headers, credentials, or exception body.
        result.update(status='failed', failure_type=type(exc).__name__)
    result['finished_at'] = datetime.now(timezone.utc).isoformat()
    write_json(bundle / 'result.json', result)
    print(json.dumps({k: result.get(k) for k in ['status', 'billing_status', 'usage_cost_estimate_usd', 'failure_type']}))
    return 0 if result['status'] == 'completed' else 1


if __name__ == '__main__':
    sys.exit(main())
