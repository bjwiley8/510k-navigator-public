import importlib
def test_import_reg_graph_modules():
    # Expected to fail initially until core/db.py and core/orm.py exist
    importlib.import_module("core.db")
    importlib.import_module("core.orm")
