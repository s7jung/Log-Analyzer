# Log Parser — Limitations & Migration Plan

## Current approach

`app/services/log_parser.py` uses hard-coded regex patterns to extract
`timestamp`, `level`, and `message` from each log line.

## Supported formats

| Pattern | Example |
|---------|---------|
| Bracketed | `[2026-02-12 10:32:11] ERROR Something failed` |
| Dash-separated | `2024-11-19 08:00:15 - ERROR: Database connection failed` |

## Known limitations

| # | Limitation | Impact |
|---|-----------|--------|
| 1 | Hard-coded patterns — each new format needs a new regex | Does not generalize to arbitrary log sources |
| 2 | Single-line only — no multi-line support | Stack traces and JSON logs are split/lost |
| 3 | Brittle to minor variations (`[ERROR]` vs `ERROR:` vs `error`) | High failure rate on real-world logs |
| 4 | Pattern list grows linearly | Maintenance burden increases with each format |

## What to change

| File | What | Why |
|------|------|-----|
| `app/services/log_parser.py` | Replace regex parsing with LLM-based extraction | Handle any format without new patterns |
| `app/services/log_processing.py` | Add embedding generation after parsing | Enable similarity search and clustering |
| `app/models/log_entry.py` | Populate `embedding` column (currently always `NULL`) | Store vectors for pgvector queries |
| `app/models/cluster.py` | Populate via clustering service | Group similar log entries automatically |

## Planned replacement

1. **LLM-based extraction** — Send raw log text to an LLM, receive structured `{timestamp, level, message}` regardless of format.
2. **Embedding-based classification** — Vectorize log messages, store in `embedding` column, use pgvector for similarity search.
3. **Clustering** — Group similar error logs into `Cluster` records with centroid embeddings.

Until then, the regex parser serves as the MVP fallback.
