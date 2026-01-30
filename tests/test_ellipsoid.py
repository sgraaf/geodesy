"""Tests for the ellipsoid module."""

import math
from dataclasses import FrozenInstanceError

import pytest

from geodesy.ellipsoid import (
    AIRY_1830,
    CLARKE_1866,
    GRS_1980,
    INTERNATIONAL_1924,
    WGS_84,
    Ellipsoid,
)


class TestEllipsoid:
    """Tests for the Ellipsoid class."""

    def test_create_ellipsoid_with_required_attributes(self) -> None:
        """Test creating an ellipsoid with required attributes."""
        ellipsoid = Ellipsoid(name="Test", code=1234, a=6378137.0, f=1 / 298.257223563)
        assert ellipsoid.name == "Test"
        assert ellipsoid.code == 1234
        assert ellipsoid.a == 6378137.0
        assert ellipsoid.f == pytest.approx(1 / 298.257223563)
        assert ellipsoid.remarks is None

    def test_create_ellipsoid_with_remarks(self) -> None:
        """Test creating an ellipsoid with remarks."""
        ellipsoid = Ellipsoid(
            name="Test",
            code=1234,
            a=6378137.0,
            f=1 / 298.257223563,
            remarks="Test remarks",
        )
        assert ellipsoid.remarks == "Test remarks"

    def test_ellipsoid_is_frozen(self) -> None:
        """Test that ellipsoid instances are immutable."""
        ellipsoid = Ellipsoid(name="Test", code=1234, a=6378137.0, f=1 / 298.257223563)
        with pytest.raises(FrozenInstanceError):
            ellipsoid.name = "Changed"  # type: ignore[misc]

    def test_ellipsoid_equality(self) -> None:
        """Test ellipsoid equality comparison."""
        e1 = Ellipsoid(name="Test", code=1234, a=6378137.0, f=1 / 298.257223563)
        e2 = Ellipsoid(name="Test", code=1234, a=6378137.0, f=1 / 298.257223563)
        e3 = Ellipsoid(name="Other", code=5678, a=6378137.0, f=1 / 298.257223563)
        assert e1 == e2
        assert e1 != e3

    def test_ellipsoid_hash(self) -> None:
        """Test that ellipsoids are hashable."""
        e1 = Ellipsoid(name="Test", code=1234, a=6378137.0, f=1 / 298.257223563)
        e2 = Ellipsoid(name="Test", code=1234, a=6378137.0, f=1 / 298.257223563)
        assert hash(e1) == hash(e2)
        # Can be used in sets
        ellipsoids = {e1, e2}
        assert len(ellipsoids) == 1


class TestEllipsoidDerivedProperties:
    """Tests for ellipsoid derived properties."""

    def test_semi_minor_axis_b(self) -> None:
        """Test semi-minor axis calculation."""
        # For WGS 84: b = a * (1 - f)
        expected_b = WGS_84.a * (1 - WGS_84.f)
        assert WGS_84.b == pytest.approx(expected_b)
        assert WGS_84.b == pytest.approx(6356752.314245179, rel=1e-9)

    def test_first_eccentricity_squared_e2(self) -> None:
        """Test first eccentricity squared calculation.

        Formula: e2 = 2*f - f^2
        """
        expected_e2 = 2 * WGS_84.f - WGS_84.f**2
        assert WGS_84.e2 == pytest.approx(expected_e2)
        assert WGS_84.e2 == pytest.approx(0.00669437999014, rel=1e-9)

    def test_first_eccentricity_e(self) -> None:
        """Test first eccentricity calculation.

        Formula: e = sqrt(e2)
        """
        expected_e = math.sqrt(WGS_84.e2)
        assert WGS_84.e == pytest.approx(expected_e)
        assert WGS_84.e == pytest.approx(0.0818191908426, rel=1e-9)

    def test_second_eccentricity_squared_ep2(self) -> None:
        """Test second eccentricity squared calculation.

        Formula: ep2 = e2 / (1 - e2)
        """
        expected_ep2 = WGS_84.e2 / (1 - WGS_84.e2)
        assert WGS_84.ep2 == pytest.approx(expected_ep2)
        assert WGS_84.ep2 == pytest.approx(0.00673949674228, rel=1e-9)

    def test_urn(self) -> None:
        """Test URN generation."""
        assert WGS_84.urn == "urn:ogc:def:ellipsoid:EPSG::7030"

    def test_custom_ellipsoid_urn(self) -> None:
        """Test URN for custom ellipsoid."""
        ellipsoid = Ellipsoid(name="Custom", code=9999, a=6378137.0, f=1 / 300.0)
        assert ellipsoid.urn == "urn:ogc:def:ellipsoid:EPSG::9999"

    def test_derived_properties_computed_at_init(self) -> None:
        """Test that derived properties are computed at initialization."""
        ellipsoid = Ellipsoid(name="Test", code=1234, a=6378137.0, f=1 / 298.0)
        # Derived properties should be available immediately after creation
        assert ellipsoid.b == ellipsoid.a * (1 - ellipsoid.f)
        assert ellipsoid.e2 == 2 * ellipsoid.f - ellipsoid.f**2
        assert ellipsoid.e == ellipsoid.e2**0.5
        assert ellipsoid.urn == "urn:ogc:def:ellipsoid:EPSG::1234"

    def test_sphere_ellipsoid(self) -> None:
        """Test an ellipsoid with zero flattening (sphere)."""
        sphere = Ellipsoid(name="Sphere", code=0, a=6371000.0, f=0.0)
        assert sphere.b == sphere.a
        assert sphere.e2 == 0.0
        assert sphere.e == 0.0
        assert sphere.ep2 == 0.0


class TestBuiltinEllipsoids:
    """Tests for built-in ellipsoid definitions."""

    def test_wgs_84_attributes(self) -> None:
        """Test WGS 84 ellipsoid attributes."""
        assert WGS_84.name == "WGS 84"
        assert WGS_84.code == 7030
        assert WGS_84.a == 6378137.0
        assert WGS_84.f == pytest.approx(1 / 298.257223563)
        assert WGS_84.remarks is not None

    def test_grs_1980_attributes(self) -> None:
        """Test GRS 1980 ellipsoid attributes."""
        assert GRS_1980.name == "GRS 1980"
        assert GRS_1980.code == 7019
        assert GRS_1980.a == 6378137.0
        assert GRS_1980.f == pytest.approx(1 / 298.257222101)
        assert GRS_1980.remarks is not None

    def test_airy_1830_attributes(self) -> None:
        """Test Airy 1830 ellipsoid attributes."""
        assert AIRY_1830.name == "Airy 1830"
        assert AIRY_1830.code == 7001
        assert AIRY_1830.a == 6377563.396
        assert AIRY_1830.f == pytest.approx(1 / 299.3249646)
        assert AIRY_1830.remarks is not None

    def test_clarke_1866_attributes(self) -> None:
        """Test Clarke 1866 ellipsoid attributes."""
        assert CLARKE_1866.name == "Clarke 1866"
        assert CLARKE_1866.code == 7008
        assert CLARKE_1866.a == 6378206.4
        assert CLARKE_1866.f == pytest.approx(1 / 294.978698213898)
        assert CLARKE_1866.remarks is not None

    def test_international_1924_attributes(self) -> None:
        """Test International 1924 ellipsoid attributes."""
        assert INTERNATIONAL_1924.name == "International 1924"
        assert INTERNATIONAL_1924.code == 7022
        assert INTERNATIONAL_1924.a == 6378388.0
        assert INTERNATIONAL_1924.f == pytest.approx(1 / 297.0)
        assert INTERNATIONAL_1924.remarks is not None

    def test_wgs_84_and_grs_1980_same_semi_major_axis(self) -> None:
        """Test that WGS 84 and GRS 1980 share the same semi-major axis."""
        assert WGS_84.a == GRS_1980.a

    def test_wgs_84_and_grs_1980_different_flattening(self) -> None:
        """Test that WGS 84 and GRS 1980 have slightly different flattening."""
        assert WGS_84.f != GRS_1980.f
        # But they're very close
        assert WGS_84.f == pytest.approx(GRS_1980.f, rel=1e-6)

    def test_all_ellipsoids_have_unique_codes(self) -> None:
        """Test that all built-in ellipsoids have unique EPSG codes."""
        ellipsoids = [WGS_84, GRS_1980, AIRY_1830, CLARKE_1866, INTERNATIONAL_1924]
        codes = [e.code for e in ellipsoids]
        assert len(codes) == len(set(codes))

    def test_all_ellipsoids_have_positive_semi_major_axis(self) -> None:
        """Test that all built-in ellipsoids have positive semi-major axis."""
        ellipsoids = [WGS_84, GRS_1980, AIRY_1830, CLARKE_1866, INTERNATIONAL_1924]
        for ellipsoid in ellipsoids:
            assert ellipsoid.a > 0

    def test_all_ellipsoids_have_positive_flattening(self) -> None:
        """Test that all built-in ellipsoids have positive flattening."""
        ellipsoids = [WGS_84, GRS_1980, AIRY_1830, CLARKE_1866, INTERNATIONAL_1924]
        for ellipsoid in ellipsoids:
            assert ellipsoid.f > 0
            assert ellipsoid.f < 1  # Flattening must be less than 1


class TestEllipsoidDerivedPropertiesConsistency:
    """Tests for consistency of derived properties across ellipsoids."""

    @pytest.mark.parametrize(
        "ellipsoid",
        [WGS_84, GRS_1980, AIRY_1830, CLARKE_1866, INTERNATIONAL_1924],
        ids=["WGS_84", "GRS_1980", "AIRY_1830", "CLARKE_1866", "INTERNATIONAL_1924"],
    )
    def test_semi_minor_axis_less_than_semi_major(self, ellipsoid: Ellipsoid) -> None:
        """Test that b < a for all ellipsoids (oblate spheroid)."""
        assert ellipsoid.b < ellipsoid.a

    @pytest.mark.parametrize(
        "ellipsoid",
        [WGS_84, GRS_1980, AIRY_1830, CLARKE_1866, INTERNATIONAL_1924],
        ids=["WGS_84", "GRS_1980", "AIRY_1830", "CLARKE_1866", "INTERNATIONAL_1924"],
    )
    def test_eccentricity_squared_positive(self, ellipsoid: Ellipsoid) -> None:
        """Test that e2 > 0 for all ellipsoids."""
        assert ellipsoid.e2 > 0

    @pytest.mark.parametrize(
        "ellipsoid",
        [WGS_84, GRS_1980, AIRY_1830, CLARKE_1866, INTERNATIONAL_1924],
        ids=["WGS_84", "GRS_1980", "AIRY_1830", "CLARKE_1866", "INTERNATIONAL_1924"],
    )
    def test_eccentricity_less_than_one(self, ellipsoid: Ellipsoid) -> None:
        """Test that e < 1 for all ellipsoids."""
        assert ellipsoid.e < 1

    @pytest.mark.parametrize(
        "ellipsoid",
        [WGS_84, GRS_1980, AIRY_1830, CLARKE_1866, INTERNATIONAL_1924],
        ids=["WGS_84", "GRS_1980", "AIRY_1830", "CLARKE_1866", "INTERNATIONAL_1924"],
    )
    def test_b_formula_consistency(self, ellipsoid: Ellipsoid) -> None:
        """Test that b = a * (1 - f) holds."""
        expected_b = ellipsoid.a * (1 - ellipsoid.f)
        assert ellipsoid.b == pytest.approx(expected_b)

    @pytest.mark.parametrize(
        "ellipsoid",
        [WGS_84, GRS_1980, AIRY_1830, CLARKE_1866, INTERNATIONAL_1924],
        ids=["WGS_84", "GRS_1980", "AIRY_1830", "CLARKE_1866", "INTERNATIONAL_1924"],
    )
    def test_eccentricity_relationship(self, ellipsoid: Ellipsoid) -> None:
        """Test the relationship e^2 = (a^2 - b^2) / a^2."""
        expected_e2 = (ellipsoid.a**2 - ellipsoid.b**2) / ellipsoid.a**2
        assert ellipsoid.e2 == pytest.approx(expected_e2, rel=1e-12)
