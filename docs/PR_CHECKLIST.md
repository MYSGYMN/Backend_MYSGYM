PR Review Checklist — Migration script
===================================

Use this checklist when reviewing the migration utility PR.

- [ ] Run migrations on a staging Postgres instance (`flask db upgrade`).
- [ ] Verify schema in Postgres matches expectations (columns, types, identities).
- [ ] Perform a dry run: count rows in source and target for each table.
- [ ] Run the migration script on a small subset or a copy of the DB and validate data integrity.
- [ ] Ensure primary keys and unique constraints will not be violated by the insert strategy.
- [ ] Confirm `SOURCE_DB_URI` and `TARGET_DB_URI` are not hard-coded in repo or logs.
- [ ] Back up target DB before full import.
- [ ] Run test suite and any integration checks against the staging DB.
- [ ] Confirm that sensitive credentials are not leaked in logs or commits.
- [ ] Documentation: examples and usage are clear in `docs/MIGRATION.md`.
- [ ] Add a reviewer to verify DNS/connection and permissions for the target DB.

Optional:
- [ ] Consider using CSV export/import or an ETL tool for very large datasets.
- [ ] Plan a rollback procedure in case of issues after import.
