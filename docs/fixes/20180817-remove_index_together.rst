Removing ``index_together`` triggers a migration but the migration fails with a ``ValueError``.

I have removed any reference to the ``index_together``, removed ``AlterIndexTogether`` from the ``initial`` migration.

For existing systems that have migrated up to ``0004`` you need to delete the index before migrating past ``0004``.

Run this mysql command::

	mysql ambition_production -Bse "alter table edc_reference_reference drop index edc_reference_reference_identifier_timepoint_repo_526121ab_idx;"
