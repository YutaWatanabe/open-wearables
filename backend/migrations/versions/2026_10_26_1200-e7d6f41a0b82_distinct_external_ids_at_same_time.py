"""Keep distinct SDK records at the same timestamp.

Revision ID: e7d6f41a0b82
Revises: c4e7a1d93b52
"""

from typing import Sequence, Union

from alembic import op

revision: str = "e7d6f41a0b82"
down_revision: Union[str, None] = "c4e7a1d93b52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_data_point_series_source_type_time", "data_point_series", type_="unique")
    op.create_unique_constraint(
        "uq_data_point_series_source_type_time",
        "data_point_series",
        ["data_source_id", "series_type_definition_id", "recorded_at", "external_id"],
        postgresql_nulls_not_distinct=True,
    )


def downgrade() -> None:
    op.drop_constraint("uq_data_point_series_source_type_time", "data_point_series", type_="unique")
    # Rows with distinct external IDs at one instant cannot fit the former key.
    # A downgrade must resolve those rows before restoring the old constraint.
    op.create_unique_constraint(
        "uq_data_point_series_source_type_time",
        "data_point_series",
        ["data_source_id", "series_type_definition_id", "recorded_at"],
    )
