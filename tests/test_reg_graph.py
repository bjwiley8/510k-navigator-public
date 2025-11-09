import importlib
from sqlalchemy.orm import Session

def test_db_get_engine_default_sqlite():
    db = importlib.import_module("core.db")
    eng = db.get_engine()  # should default to in-memory sqlite
    assert "sqlite" in eng.dialect.name

def test_models_exist_and_roundtrip():
    orm = importlib.import_module("core.orm")
    db = importlib.import_module("core.db")

    for name in ("Base", "Device", "ProductCode", "Regulation", "Indication"):
        assert hasattr(orm, name), f"Missing {name}"

    engine = db.get_engine()
    orm.Base.metadata.create_all(engine)

    with Session(engine) as s:
        reg = orm.Regulation(cfr="21 CFR 888.2790")
        pc  = orm.ProductCode(code="KWD", name="Toe joint resurfacing", regulation=reg)
        ind = orm.Indication(text="Hemiarthroplasty of the metatarsal head")
        dev = orm.Device(name="Ormi Great Toe Hemi", product_code=pc, indications=[ind])
        s.add(dev)
        s.commit()

        got = s.query(orm.Device).filter_by(name="Ormi Great Toe Hemi").one()
        assert got.product_code.code == "KWD"
        assert got.product_code.regulation.cfr.startswith("21 CFR")
        assert got.indications and got.indications[0].text.startswith("Hemiarthroplasty")
