"""date index add

Revision ID: 09a456d71e4a
Revises: 965ec35ea309
Create Date: 2024-10-14 20:56:54.333669

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "09a456d71e4a"
down_revision: Union[str, None] = "965ec35ea309"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        op.f("ix_spimex_trading_results_date"),
        "spimex_trading_results",
        ["date"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_spimex_trading_results_date"), table_name="spimex_trading_results"
    )
