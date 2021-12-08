"""empty message

Revision ID: 6354c5ee5605
Revises: 6e7142d03a43
Create Date: 2021-12-06 19:10:30.316151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6354c5ee5605'
down_revision = '6e7142d03a43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complaints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('photo_url', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('create_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='state'), nullable=False),
    sa.Column('complainer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['complainer_id'], ['complainers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('complaints')
    # ### end Alembic commands ###
