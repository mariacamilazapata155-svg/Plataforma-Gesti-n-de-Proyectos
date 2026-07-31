from sqlalchemy import text

from app.db.session import engine


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        print("✅ Conexión exitosa")
        print(result.scalar())

except Exception as e:
    print("❌ Error al conectar")
    print(e)