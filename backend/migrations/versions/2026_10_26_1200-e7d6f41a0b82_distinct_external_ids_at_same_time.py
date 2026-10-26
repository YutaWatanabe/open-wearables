"""Keep distinct SDK records at the same timestamp.

Revision ID: e7d6f41a0b82
Revises: c4e7a1d93b52
"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

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
    duplicate = (
        op.get_bind()
        .execute(
            text(
                "SELECT 1 FROM data_point_series "
                "GROUP BY data_source_id, series_type_definition_id, recorded_at "
                "HAVING COUNT(*) > 1 LIMIT 1"
            )
        )
        .first()
    )
    if duplicate is not None:
        raise RuntimeError(
            "Cannot restore the old data_point_series uniqueness constraint: "
            "delete or consolidate rows with the same source, type, and timestamp first."
        )
    op.drop_constraint("uq_data_point_series_source_type_time", "data_point_series", type_="unique")
    op.create_unique_constraint(
        "uq_data_point_series_source_type_time",
        "data_point_series",
        ["data_source_id", "series_type_definition_id", "recorded_at"],
    )
