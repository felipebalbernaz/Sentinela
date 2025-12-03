import os
import sqlite3
from pathlib import Path

# Tenta usar a aplicação (SQLAlchemy) quando possível; caso contrário, usa sqlite3 direto
try:
    from app import create_app, db
    from sqlalchemy import inspect, text

    app = create_app()
    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('notas_fiscais')]
        if 'pago' in columns:
            print('Coluna "pago" já existe na tabela notas_fiscais.')
        else:
            try:
                with engine.connect() as conn:
                    conn.execute(text('ALTER TABLE notas_fiscais ADD COLUMN pago BOOLEAN NOT NULL DEFAULT 0'))
                print('Coluna "pago" adicionada com sucesso (via SQLAlchemy).')
            except Exception as e:
                print(f'Erro ao adicionar coluna "pago" via SQLAlchemy: {e}')
except Exception:
    # Fallback direto no arquivo SQLite
    db_path = Path(__file__).resolve().parent / 'sentinela.db'
    if not db_path.exists():
        # também tenta um nível acima caso seja executado de outro working dir
        db_path = Path(__file__).resolve().parent.parent / 'instance' / 'sentinela.db'

    if not db_path.exists():
        print(f'Arquivo de banco de dados não encontrado em {db_path}. Não foi possível atualizar schema.')
    else:
        try:
            conn = sqlite3.connect(str(db_path))
            cur = conn.cursor()
            # Verifica se coluna já existe
            cur.execute("PRAGMA table_info(notas_fiscais)")
            cols = [row[1] for row in cur.fetchall()]
            if 'pago' in cols:
                print('Coluna "pago" já existe na tabela notas_fiscais (via sqlite3).')
            else:
                cur.execute("ALTER TABLE notas_fiscais ADD COLUMN pago BOOLEAN NOT NULL DEFAULT 0")
                conn.commit()
                print('Coluna "pago" adicionada com sucesso (via sqlite3).')
        except Exception as e:
            print(f'Erro ao executar ALTER TABLE via sqlite3: {e}')
        finally:
            try:
                conn.close()
            except Exception:
                pass
