from fit2geo.fit2shape import convert_to_geopandas


def test_practice():
    convert_to_geopandas("test/data/9270632244.fit")
    assert True
