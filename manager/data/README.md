# Manager data files

The complete simulation and real-study workflow is in:

```text
manager/README.md
```

This folder contains:

- `pseudo_raw_workers.xlsx`: original 50-worker example workbook;
- `pseudo_raw_workers_1400.xlsx`: full 1,400-worker rehearsal workbook;
- `raw_workers.csv`: original 50-worker example CSV;
- `raw_workers_1400.csv`: unmatched 1,400-worker simulation input;
- `worker_pairs.csv`: fixed output from `create_random_pairs.py`; and
- `manager_assignments.csv`: fixed treatment/manager/round schedule from
  `create_manager_assignments.py`.

Do not regenerate final pair or assignment files after real oTree sessions have
been created. Keep the raw input, both generated CSVs, and both seeds in the
experiment's reproducibility archive.
