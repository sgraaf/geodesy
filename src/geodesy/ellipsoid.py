"""Reference ellipsoid definitions.

An ellipsoid is defined by its semi-major axis (a) and flattening (f).
All other parameters are derived from these.
"""

from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class Ellipsoid:
    """A reference ellipsoid for geodetic calculations.

    Attributes:
        name: Human-readable name
        code: EPSG code
        a: Semi-major axis in metres
        f: Flattening (dimensionless)
        remarks: Remarks, if any

    Example:
        >>> WGS_84.a
        6378137.0
        >>> WGS_84.b  # semi-minor axis (derived)
        6356752.314245179
    """

    name: str
    code: int
    a: float  # semi-major axis (metres)
    f: float  # flattening
    remarks: str | None = None

    @cached_property
    def b(self) -> float:
        """Semi-minor axis in metres."""
        return self.a * (1 - self.f)

    @cached_property
    def e2(self) -> float:
        """First eccentricity squared."""
        return 2 * self.f - self.f**2

    @cached_property
    def e(self) -> float:
        """First eccentricity."""
        return self.e2**0.5

    @cached_property
    def ep2(self) -> float:
        """Second eccentricity squared."""
        return self.e2 / (1 - self.e2)

    @cached_property
    def urn(self) -> str:
        """Uniform Resource Name (URN)."""
        return f"urn:ogc:def:ellipsoid:EPSG::{self.code}"


# Built-in ellipsoids
AIRY_1830 = Ellipsoid(
    name="Airy 1830",
    code=7001,
    a=6377563.396,
    f=1 / 299.3249646,
    remarks="Original definition is a=20923713, b=20853810 feet of 1796. 1/f is given to 7 decimal places. For the 1936 retriangulation OSGB defines the relationship of 10 feet of 1796 to the International metre through ([10^0.48401603]/10) exactly = 0.3048007491...",
)
""": :Airy 1830 ellipsoid (`EPSG:7001 <https://epsg.io/7001-ellipsoid>`_). Used by OSGB36 datum."""

CLARKE_1866 = Ellipsoid(
    name="Clarke 1866",
    code=7008,
    a=6378206.4,
    f=1 / 294.978698213898,
    remarks="Original definition a=20926062 and b=20855121 (British) feet. Uses Clarke's 1865 inch-metre ratio of 39.370432 to obtain metres. (Metric value then converted to US survey feet for use in the US and international feet for use in Cayman Islands).",
)
""": :Clarke 1866 ellipsoid (`EPSG:7008 <https://epsg.io/7008-ellipsoid>`_). Used by NAD27 datum."""

GRS_1980 = Ellipsoid(
    name="GRS 1980",
    code=7019,
    a=6378137.0,
    f=1 / 298.257222101,
    remarks="Adopted by IUGG 1979 Canberra. Inverse flattening is derived from geocentric gravitational constant GM = 3986005e8 m*m*m/s/s; dynamic form factor J2 = 108263e-8 and Earth's angular velocity = 7292115e-11 rad/s.",
)
""": :GRS 1980 ellipsoid (`EPSG:7019 <https://epsg.io/7019-ellipsoid>`_). Used by NAD83 and ETRS89 datums."""

INTERNATIONAL_1924 = Ellipsoid(
    name="International 1924",
    code=7022,
    a=6378388.0,
    f=1 / 297.0,
    remarks="Adopted by IUGG 1924 in Madrid. Based on Hayford 1909/1910 figures.",
)
""": :International 1924 ellipsoid (`EPSG:7022 <https://epsg.io/7022-ellipsoid>`_), also known as Hayford 1909. Used by ED50 datum."""

WGS_84 = Ellipsoid(
    name="WGS 84",
    code=7030,
    a=6378137.0,
    f=1 / 298.257223563,
    remarks="1/f derived from four defining parameters semi-major axis; C20 = -484.16685*10e-6; earth's angular velocity ω = 7292115e-11 rad/sec; gravitational constant GM = 3986005e8 m*m*m/s/s. In 1994 new GM = 3986004.418e8 m*m*m/s/s but a and 1/f retained.",
)
""": :WGS 84 ellipsoid (`EPSG:7030 <https://epsg.io/7030-ellipsoid>`_). Used by WGS84 datum."""
