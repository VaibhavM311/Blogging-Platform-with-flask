"""Add comments, categories, tags and post category association.

Revision ID: f31a9c2d8e41
Revises: e527b84c176b
"""
from alembic import op
import sqlalchemy as sa

revision = "f31a9c2d8e41"
down_revision = "e527b84c176b"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=60), nullable=False),
        sa.Column("slug", sa.String(length=70), nullable=False),
    )
    op.create_index("ix_categories_name", "categories", ["name"], unique=True)
    op.create_index("ix_categories_slug", "categories", ["slug"], unique=True)
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.Column("slug", sa.String(length=50), nullable=False),
    )
    op.create_index("ix_tags_name", "tags", ["name"], unique=True)
    op.create_index("ix_tags_slug", "tags", ["slug"], unique=True)
    op.create_table(
        "post_tags",
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("tag_id", sa.Integer(), sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    )
    op.add_column("posts", sa.Column("category_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_posts_category_id_categories", "posts", "categories", ["category_id"], ["id"])
    op.create_index("ix_posts_category_id", "posts", ["category_id"])
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_index("ix_comments_created_at", "comments", ["created_at"])

def downgrade():
    op.drop_index("ix_comments_created_at", table_name="comments")
    op.drop_table("comments")
    op.drop_index("ix_posts_category_id", table_name="posts")
    op.drop_constraint("fk_posts_category_id_categories", "posts", type_="foreignkey")
    op.drop_column("posts", "category_id")
    op.drop_table("post_tags")
    op.drop_index("ix_tags_slug", table_name="tags")
    op.drop_index("ix_tags_name", table_name="tags")
    op.drop_table("tags")
    op.drop_index("ix_categories_slug", table_name="categories")
    op.drop_index("ix_categories_name", table_name="categories")
    op.drop_table("categories")
