from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Limpiando base de datos (desactivando FK checks temporalmente)...")
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    db.drop_all()
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    
    print("Creando estrictamente las 9 tablas...")
    db.create_all()
    db.session.commit()
    
    print("¡Base de datos lista con las 9 tablas solicitadas!")
    print(f"Tablas actuales en la DB: {list(db.metadata.tables.keys())}")
