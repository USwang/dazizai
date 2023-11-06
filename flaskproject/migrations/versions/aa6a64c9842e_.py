"""empty message

Revision ID: aa6a64c9842e
Revises: 29791f08941d
Create Date: 2023-11-03 11:43:55.943866

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aa6a64c9842e'
down_revision = '29791f08941d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('SECURITY_CODE', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('SECURITY_NAME_ABBR', sa.String(length=50), nullable=True))
        batch_op.drop_index('codenumber')
        batch_op.drop_index('stockname')
        batch_op.create_unique_constraint(None, ['SECURITY_NAME_ABBR'])
        batch_op.create_unique_constraint(None, ['SECURITY_CODE'])
        batch_op.drop_column('stockname')
        batch_op.drop_column('codenumber')

    with op.batch_alter_table('stock_list', schema=None) as batch_op:
        batch_op.add_column(sa.Column('SECURITY_CODE', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('SECURITY_NAME_ABBR', sa.String(length=50), nullable=True))
        batch_op.drop_index('codenumber')
        batch_op.drop_index('stockname')
        batch_op.create_unique_constraint(None, ['SECURITY_CODE'])
        batch_op.create_unique_constraint(None, ['SECURITY_NAME_ABBR'])
        batch_op.drop_column('markettag')
        batch_op.drop_column('stockname')
        batch_op.drop_column('codenumber')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock_list', schema=None) as batch_op:
        batch_op.add_column(sa.Column('codenumber', mysql.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('stockname', mysql.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('markettag', mysql.VARCHAR(length=50), nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('stockname', ['stockname'], unique=False)
        batch_op.create_index('codenumber', ['codenumber'], unique=False)
        batch_op.drop_column('SECURITY_NAME_ABBR')
        batch_op.drop_column('SECURITY_CODE')

    with op.batch_alter_table('stock_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('codenumber', mysql.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('stockname', mysql.VARCHAR(length=50), nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('stockname', ['stockname'], unique=False)
        batch_op.create_index('codenumber', ['codenumber'], unique=False)
        batch_op.drop_column('SECURITY_NAME_ABBR')
        batch_op.drop_column('SECURITY_CODE')

    # ### end Alembic commands ###