"""empty message

Revision ID: 7150c3c3edbb
Revises: 
Create Date: 2024-10-13 18:12:32.278834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7150c3c3edbb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipe_id', sa.Integer(), nullable=False))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_foreign_key(None, 'recipe', ['recipe_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        # batch_op.drop_constraint(None, type_='foreignkey')
        # batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('recipe_id')

    # ### end Alembic commands ###