"""Umbral de lluvia del pronóstico del clima (segunda API externa).

- Parámetro ``porcentaje_lluvia_aviso`` = 60 (configurable en base de datos, SRS 3.5.3):
  desde qué probabilidad de lluvia el pronóstico de un alquiler muestra un aviso.

Sin cambios en las tablas: solo una fila en ``parametros_sistema``.

Revision ID: a1c3e5f7b9d2
Revises: ce778c5c8489
Create Date: 2026-11-17 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1c3e5f7b9d2"
down_revision: str | Sequence[str] | None = "ce778c5c8489"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_PARAMETROS = sa.table(
    "parametros_sistema",
    sa.column("clave", sa.String),
    sa.column("valor", sa.Integer),
    sa.column("descripcion", sa.Text),
)


def upgrade() -> None:
    """Agrega el umbral de lluvia del aviso del clima."""
    op.bulk_insert(
        _PARAMETROS,
        [
            {
                "clave": "porcentaje_lluvia_aviso",
                "valor": 60,
                "descripcion": (
                    "Probabilidad de lluvia (%) desde la cual el pronóstico de un alquiler "
                    "muestra un aviso al cliente."
                ),
            }
        ],
    )


def downgrade() -> None:
    """Quita el parámetro."""
    op.execute("DELETE FROM parametros_sistema WHERE clave = 'porcentaje_lluvia_aviso'")
