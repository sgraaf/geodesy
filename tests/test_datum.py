"""Tests for the datum module."""

from dataclasses import FrozenInstanceError

import pytest

from geodesy.datum import (
    ED50,
    ETRS89,
    NAD27,
    NAD83,
    OSGB36,
    WGS84,
    Datum,
    HelmertParameters,
)
from geodesy.ellipsoid import (
    AIRY_1830,
    CLARKE_1866,
    GRS_1980,
    INTERNATIONAL_1924,
    WGS_84,
    Ellipsoid,
)


class TestHelmertParameters:
    """Tests for the HelmertParameters class."""

    def test_create_helmert_parameters(self) -> None:
        """Test creating Helmert parameters."""
        params = HelmertParameters(
            tx=1.0, ty=2.0, tz=3.0, rx=0.1, ry=0.2, rz=0.3, s=0.5
        )
        assert params.tx == 1.0
        assert params.ty == 2.0
        assert params.tz == 3.0
        assert params.rx == 0.1
        assert params.ry == 0.2
        assert params.rz == 0.3
        assert params.s == 0.5

    def test_helmert_parameters_zero_transform(self) -> None:
        """Test Helmert parameters for identity transform."""
        params = HelmertParameters(
            tx=0.0, ty=0.0, tz=0.0, rx=0.0, ry=0.0, rz=0.0, s=0.0
        )
        assert params.tx == 0.0
        assert params.ty == 0.0
        assert params.tz == 0.0
        assert params.rx == 0.0
        assert params.ry == 0.0
        assert params.rz == 0.0
        assert params.s == 0.0

    def test_helmert_parameters_is_frozen(self) -> None:
        """Test that Helmert parameters are immutable."""
        params = HelmertParameters(
            tx=1.0, ty=2.0, tz=3.0, rx=0.1, ry=0.2, rz=0.3, s=0.5
        )
        with pytest.raises(FrozenInstanceError):
            params.tx = 10.0  # type: ignore[misc]

    def test_helmert_parameters_equality(self) -> None:
        """Test Helmert parameters equality comparison."""
        p1 = HelmertParameters(tx=1.0, ty=2.0, tz=3.0, rx=0.1, ry=0.2, rz=0.3, s=0.5)
        p2 = HelmertParameters(tx=1.0, ty=2.0, tz=3.0, rx=0.1, ry=0.2, rz=0.3, s=0.5)
        p3 = HelmertParameters(tx=9.0, ty=2.0, tz=3.0, rx=0.1, ry=0.2, rz=0.3, s=0.5)
        assert p1 == p2
        assert p1 != p3

    def test_helmert_parameters_hash(self) -> None:
        """Test that Helmert parameters are hashable."""
        p1 = HelmertParameters(tx=1.0, ty=2.0, tz=3.0, rx=0.1, ry=0.2, rz=0.3, s=0.5)
        p2 = HelmertParameters(tx=1.0, ty=2.0, tz=3.0, rx=0.1, ry=0.2, rz=0.3, s=0.5)
        assert hash(p1) == hash(p2)
        # Can be used in sets
        params_set = {p1, p2}
        assert len(params_set) == 1

    def test_helmert_parameters_negative_values(self) -> None:
        """Test Helmert parameters with negative values."""
        params = HelmertParameters(
            tx=-87.0, ty=-98.0, tz=-121.0, rx=-0.1, ry=-0.2, rz=-0.3, s=-20.0
        )
        assert params.tx == -87.0
        assert params.ty == -98.0
        assert params.tz == -121.0
        assert params.rx == -0.1
        assert params.ry == -0.2
        assert params.rz == -0.3
        assert params.s == -20.0


class TestDatum:
    """Tests for the Datum class."""

    def test_create_datum_with_required_attributes(self) -> None:
        """Test creating a datum with required attributes."""
        datum = Datum(name="Test Datum", code=1234, ellipsoid=WGS_84)
        assert datum.name == "Test Datum"
        assert datum.code == 1234
        assert datum.ellipsoid is WGS_84
        assert datum.to_wgs84 is None
        assert datum.remarks is None

    def test_create_datum_with_helmert_transform(self) -> None:
        """Test creating a datum with Helmert transformation."""
        helmert = HelmertParameters(
            tx=446.448,
            ty=-125.157,
            tz=542.060,
            rx=0.1502,
            ry=0.2470,
            rz=0.8421,
            s=-20.4894,
        )
        datum = Datum(name="Test", code=1234, ellipsoid=AIRY_1830, to_wgs84=helmert)
        assert datum.to_wgs84 is helmert
        assert datum.to_wgs84.tx == 446.448

    def test_create_datum_with_remarks(self) -> None:
        """Test creating a datum with remarks."""
        datum = Datum(
            name="Test",
            code=1234,
            ellipsoid=WGS_84,
            remarks="Test remarks for this datum",
        )
        assert datum.remarks == "Test remarks for this datum"

    def test_create_datum_with_all_attributes(self) -> None:
        """Test creating a datum with all attributes."""
        helmert = HelmertParameters(
            tx=1.0, ty=2.0, tz=3.0, rx=0.0, ry=0.0, rz=0.0, s=0.0
        )
        datum = Datum(
            name="Full Test",
            code=9999,
            ellipsoid=GRS_1980,
            to_wgs84=helmert,
            remarks="Complete test",
        )
        assert datum.name == "Full Test"
        assert datum.code == 9999
        assert datum.ellipsoid is GRS_1980
        assert datum.to_wgs84 is helmert
        assert datum.remarks == "Complete test"

    def test_datum_is_frozen(self) -> None:
        """Test that datum instances are immutable."""
        datum = Datum(name="Test", code=1234, ellipsoid=WGS_84)
        with pytest.raises(FrozenInstanceError):
            datum.name = "Changed"  # type: ignore[misc]

    def test_datum_equality(self) -> None:
        """Test datum equality comparison."""
        d1 = Datum(name="Test", code=1234, ellipsoid=WGS_84)
        d2 = Datum(name="Test", code=1234, ellipsoid=WGS_84)
        d3 = Datum(name="Other", code=5678, ellipsoid=WGS_84)
        assert d1 == d2
        assert d1 != d3

    def test_datum_hash(self) -> None:
        """Test that datums are hashable."""
        d1 = Datum(name="Test", code=1234, ellipsoid=WGS_84)
        d2 = Datum(name="Test", code=1234, ellipsoid=WGS_84)
        assert hash(d1) == hash(d2)
        # Can be used in sets
        datums = {d1, d2}
        assert len(datums) == 1


class TestDatumURN:
    """Tests for datum URN property."""

    def test_datum_urn(self) -> None:
        """Test datum URN generation."""
        datum = Datum(name="Test", code=6326, ellipsoid=WGS_84)
        assert datum.urn == "urn:ogc:def:datum:EPSG::6326"

    def test_custom_datum_urn(self) -> None:
        """Test URN for custom datum code."""
        datum = Datum(name="Custom", code=9999, ellipsoid=WGS_84)
        assert datum.urn == "urn:ogc:def:datum:EPSG::9999"

    def test_wgs84_urn(self) -> None:
        """Test WGS84 datum URN."""
        assert WGS84.urn == "urn:ogc:def:datum:EPSG::6326"


class TestBuiltinDatums:
    """Tests for built-in datum definitions."""

    def test_wgs84_attributes(self) -> None:
        """Test WGS84 datum attributes."""
        assert WGS84.name == "World Geodetic System 1984 ensemble"
        assert WGS84.code == 6326
        assert WGS84.ellipsoid is WGS_84
        assert WGS84.to_wgs84 is not None
        assert WGS84.remarks is not None

    def test_wgs84_identity_transform(self) -> None:
        """Test WGS84 has identity Helmert transform."""
        assert WGS84.to_wgs84 is not None
        assert WGS84.to_wgs84.tx == 0.0
        assert WGS84.to_wgs84.ty == 0.0
        assert WGS84.to_wgs84.tz == 0.0
        assert WGS84.to_wgs84.rx == 0.0
        assert WGS84.to_wgs84.ry == 0.0
        assert WGS84.to_wgs84.rz == 0.0
        assert WGS84.to_wgs84.s == 0.0

    def test_etrs89_attributes(self) -> None:
        """Test ETRS89 datum attributes."""
        assert ETRS89.name == "European Terrestrial Reference System 1989 ensemble"
        assert ETRS89.code == 6258
        assert ETRS89.ellipsoid is GRS_1980
        assert ETRS89.to_wgs84 is not None
        assert ETRS89.remarks is not None

    def test_etrs89_identity_transform(self) -> None:
        """Test ETRS89 has identity Helmert transform (coincident with WGS84)."""
        assert ETRS89.to_wgs84 is not None
        assert ETRS89.to_wgs84.tx == 0.0
        assert ETRS89.to_wgs84.ty == 0.0
        assert ETRS89.to_wgs84.tz == 0.0

    def test_nad83_attributes(self) -> None:
        """Test NAD83 datum attributes."""
        assert NAD83.name == "North American Datum 1983"
        assert NAD83.code == 6269
        assert NAD83.ellipsoid is GRS_1980
        assert NAD83.to_wgs84 is not None
        assert NAD83.remarks is not None

    def test_nad83_identity_transform(self) -> None:
        """Test NAD83 has identity Helmert transform."""
        assert NAD83.to_wgs84 is not None
        assert NAD83.to_wgs84.tx == 0.0
        assert NAD83.to_wgs84.ty == 0.0
        assert NAD83.to_wgs84.tz == 0.0

    def test_nad27_attributes(self) -> None:
        """Test NAD27 datum attributes."""
        assert NAD27.name == "North American Datum 1927"
        assert NAD27.code == 6267
        assert NAD27.ellipsoid is CLARKE_1866
        assert NAD27.to_wgs84 is not None
        assert NAD27.remarks is not None

    def test_nad27_transform(self) -> None:
        """Test NAD27 Helmert transformation parameters."""
        assert NAD27.to_wgs84 is not None
        assert NAD27.to_wgs84.tx == -8.0
        assert NAD27.to_wgs84.ty == 160.0
        assert NAD27.to_wgs84.tz == 176.0
        assert NAD27.to_wgs84.rx == 0.0
        assert NAD27.to_wgs84.ry == 0.0
        assert NAD27.to_wgs84.rz == 0.0
        assert NAD27.to_wgs84.s == 0.0

    def test_ed50_attributes(self) -> None:
        """Test ED50 datum attributes."""
        assert ED50.name == "European Datum 1950"
        assert ED50.code == 6230
        assert ED50.ellipsoid is INTERNATIONAL_1924
        assert ED50.to_wgs84 is not None

    def test_ed50_transform(self) -> None:
        """Test ED50 Helmert transformation parameters."""
        assert ED50.to_wgs84 is not None
        assert ED50.to_wgs84.tx == -87.0
        assert ED50.to_wgs84.ty == -98.0
        assert ED50.to_wgs84.tz == -121.0
        assert ED50.to_wgs84.rx == 0.0
        assert ED50.to_wgs84.ry == 0.0
        assert ED50.to_wgs84.rz == 0.0
        assert ED50.to_wgs84.s == 0.0

    def test_osgb36_attributes(self) -> None:
        """Test OSGB36 datum attributes."""
        assert OSGB36.name == "Ordnance Survey of Great Britain 1936"
        assert OSGB36.code == 6277
        assert OSGB36.ellipsoid is AIRY_1830
        assert OSGB36.to_wgs84 is not None
        assert OSGB36.remarks is not None

    def test_osgb36_transform(self) -> None:
        """Test OSGB36 Helmert transformation parameters."""
        assert OSGB36.to_wgs84 is not None
        assert OSGB36.to_wgs84.tx == 446.448
        assert OSGB36.to_wgs84.ty == -125.157
        assert OSGB36.to_wgs84.tz == 542.060
        assert OSGB36.to_wgs84.rx == 0.1502
        assert OSGB36.to_wgs84.ry == 0.2470
        assert OSGB36.to_wgs84.rz == 0.8421
        assert OSGB36.to_wgs84.s == -20.4894


class TestBuiltinDatumsConsistency:
    """Tests for consistency across built-in datums."""

    def test_all_datums_have_unique_codes(self) -> None:
        """Test that all built-in datums have unique EPSG codes."""
        datums = [WGS84, ETRS89, NAD83, NAD27, ED50, OSGB36]
        codes = [d.code for d in datums]
        assert len(codes) == len(set(codes))

    def test_all_datums_have_helmert_transform(self) -> None:
        """Test that all built-in datums have Helmert transformation to WGS84."""
        datums = [WGS84, ETRS89, NAD83, NAD27, ED50, OSGB36]
        for datum in datums:
            assert datum.to_wgs84 is not None

    def test_all_datums_have_valid_ellipsoid(self) -> None:
        """Test that all built-in datums reference valid ellipsoids."""
        datums = [WGS84, ETRS89, NAD83, NAD27, ED50, OSGB36]
        for datum in datums:
            assert isinstance(datum.ellipsoid, Ellipsoid)
            assert datum.ellipsoid.a > 0


class TestDatumEllipsoidRelationships:
    """Tests for datum-ellipsoid relationships."""

    def test_wgs84_uses_wgs_84_ellipsoid(self) -> None:
        """Test WGS84 datum uses WGS 84 ellipsoid."""
        assert WGS84.ellipsoid is WGS_84

    def test_etrs89_and_nad83_share_ellipsoid(self) -> None:
        """Test ETRS89 and NAD83 share GRS 1980 ellipsoid."""
        assert ETRS89.ellipsoid is GRS_1980
        assert NAD83.ellipsoid is GRS_1980
        assert ETRS89.ellipsoid is NAD83.ellipsoid

    def test_osgb36_uses_airy_1830(self) -> None:
        """Test OSGB36 uses Airy 1830 ellipsoid."""
        assert OSGB36.ellipsoid is AIRY_1830

    def test_nad27_uses_clarke_1866(self) -> None:
        """Test NAD27 uses Clarke 1866 ellipsoid."""
        assert NAD27.ellipsoid is CLARKE_1866

    def test_ed50_uses_international_1924(self) -> None:
        """Test ED50 uses International 1924 ellipsoid."""
        assert ED50.ellipsoid is INTERNATIONAL_1924

    def test_datum_ellipsoid_properties_accessible(self) -> None:
        """Test that ellipsoid properties are accessible through datum."""
        assert WGS84.ellipsoid.a == 6378137.0
        assert OSGB36.ellipsoid.b < OSGB36.ellipsoid.a


class TestDatumDocstringExamples:
    """Tests to verify docstring examples work correctly."""

    def test_docstring_example_ellipsoid_a(self) -> None:
        """Test docstring example: WGS84.ellipsoid.a."""
        assert WGS84.ellipsoid.a == 6378137.0

    def test_docstring_example_urn(self) -> None:
        """Test docstring example: WGS84.urn."""
        assert WGS84.urn == "urn:ogc:def:datum:EPSG::6326"

    def test_docstring_example_osgb36_tx(self) -> None:
        """Test docstring example: OSGB36.to_wgs84.tx."""
        assert OSGB36.to_wgs84 is not None
        assert OSGB36.to_wgs84.tx == 446.448
