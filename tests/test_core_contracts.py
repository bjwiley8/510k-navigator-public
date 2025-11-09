from core.models import DeviceProfile

def test_profile_roundtrip():
    p = DeviceProfile(
        device_name="Ormi Great Toe Hemi (metatarsal head)",
        route_product_code="KWD",
        fixation="cemented",
        sterilization="EO",
        packaging="Double",
        shelf_life_months=24,
        indications="single-use hemi arthroplasty of the metatarsal head...",
        materials=["CoCrMo (AM, polished rim)", "Polycarbonate urethane (Carbothane 85A)", "Poly(sulfobetaine amide) brush <200 nm"],
        mr_labeling="none",
        sizes_mm=["14x12","16x14","16x16"],
        worst_case_wear="16x16",
        worst_case_strength="14x12",
    )
    assert p.route_product_code == "KWD"
    assert p.worst_case_wear in p.sizes_mm
    assert p.worst_case_strength in p.sizes_mm

# Added test for core.db and core.orm

def test_imports():
    import core.db
    import core.orm
