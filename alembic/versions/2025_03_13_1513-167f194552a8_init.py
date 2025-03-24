"""init

Revision ID: 167f194552a8
Revises:
Create Date: 2025-03-13 15:13:13.106193

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "167f194552a8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "role_rights",
        sa.Column("role_right_id", sa.Integer(), nullable=False),
        sa.Column("right", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("role_right_id", name=op.f("pk_role_rights")),
    )
    op.create_index(
        op.f("ix_role_rights_right"), "role_rights", ["right"], unique=True
    )
    op.create_table(
        "roles",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("role_id", name=op.f("pk_roles")),
        sa.UniqueConstraint("role", name=op.f("uq_roles_role")),
    )
    op.create_table(
        "role_rights_association",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("right_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["right_id"],
            ["role_rights.role_right_id"],
            name=op.f("fk_role_rights_association_right_id_role_rights"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.role_id"],
            name=op.f("fk_role_rights_association_role_id_roles"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "role_id", "right_id", name=op.f("pk_role_rights_association")
        ),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hash_password", sa.LargeBinary(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.role_id"],
            name=op.f("fk_users_role_id_roles"),
            ondelete="SET DEFAULT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("role_rights_association")
    op.drop_table("roles")
    op.drop_index(op.f("ix_role_rights_right"), table_name="role_rights")
    op.drop_table("role_rights")
