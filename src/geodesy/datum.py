"""Geodetic datum definitions.

A datum defines the position and orientation of a reference ellipsoid
relative to the Earth.
"""

from dataclasses import dataclass

from geodesy.ellipsoid import (
    AIRY_1830,
    CLARKE_1866,
    GRS_1980,
    INTERNATIONAL_1924,
    WGS_84,
    Ellipsoid,
)


@dataclass(frozen=True, slots=True)
class HelmertParameters:
    """7-parameter Helmert transformation (Bursa-Wolf) to WGS84.

    Attributes:
        tx: Translation along X-axis in metres.
        ty: Translation along Y-axis in metres.
        tz: Translation along Z-axis in metres.
        rx: Rotation around X-axis in arc-seconds.
        ry: Rotation around Y-axis in arc-seconds.
        rz: Rotation around Z-axis in arc-seconds.
        s: Scale factor in parts per million (ppm).

    Example:
        >>> OSGB36.to_wgs84.tx
        446.448
    """

    tx: float
    ty: float
    tz: float
    rx: float
    ry: float
    rz: float
    s: float


@dataclass(frozen=True, slots=True)
class Datum:
    """A geodetic datum for coordinate reference systems.

    Attributes:
        name: Human-readable name.
        code: EPSG code.
        ellipsoid: Reference ellipsoid.
        to_wgs84: Helmert transformation parameters to WGS84, if applicable.
        remarks: Remarks, if any.

    Example:
        >>> WGS84.ellipsoid.a
        6378137.0
        >>> WGS84.urn
        'urn:ogc:def:datum:EPSG::6326'
    """

    name: str
    code: int
    ellipsoid: Ellipsoid
    to_wgs84: HelmertParameters | None = None
    remarks: str | None = None

    @property
    def urn(self) -> str:
        """Uniform Resource Name (URN)."""
        return f"urn:ogc:def:datum:EPSG::{self.code}"


# Built-in datums
ED50 = Datum(
    name="European Datum 1950",
    code=6230,
    ellipsoid=INTERNATIONAL_1924,
    to_wgs84=HelmertParameters(
        tx=-87.0,
        ty=-98.0,
        tz=-121.0,
        rx=0.0,
        ry=0.0,
        rz=0.0,
        s=0.0,
    ),
)
""": :European Datum 1950 (`EPSG:6230 <https://epsg.io/6230-datum>`_). Uses International 1924 ellipsoid."""

ETRS89 = Datum(
    name="European Terrestrial Reference System 1989 ensemble",
    code=6258,
    ellipsoid=GRS_1980,
    to_wgs84=HelmertParameters(tx=0.0, ty=0.0, tz=0.0, rx=0.0, ry=0.0, rz=0.0, s=0.0),
    remarks="Has been realized through ETRF89, ETRF90, ETRF91, ETRF92, ETRF93, ETRF94, ETRF96, ETRF97, ETRF2000, ETRF2005, ETRF2014 and ETRF2020. This 'ensemble' covers any or all of these realizations without distinction.",
)
""": :European Terrestrial Reference System 1989 (`EPSG:6258 <https://epsg.io/6258-datum>`_), coincident with WGS84 at epoch 1989.0. Uses GRS 1980 ellipsoid."""

NAD27 = Datum(
    name="North American Datum 1927",
    code=6267,
    ellipsoid=CLARKE_1866,
    to_wgs84=HelmertParameters(
        tx=-8.0,
        ty=160.0,
        tz=176.0,
        rx=0.0,
        ry=0.0,
        rz=0.0,
        s=0.0,
    ),
    remarks="In United States (USA) and Canada, replaced by North American Datum 1983 (NAD83) (code 6269) ; in Mexico, replaced by Mexican Datum of 1993 (code 1042).",
)
""": :North American Datum 1927 (`EPSG:6267 <https://epsg.io/6267-datum>`_). Uses Clarke 1866 ellipsoid."""

NAD83 = Datum(
    name="North American Datum 1983",
    code=6269,
    ellipsoid=GRS_1980,
    to_wgs84=HelmertParameters(tx=0.0, ty=0.0, tz=0.0, rx=0.0, ry=0.0, rz=0.0, s=0.0),
    remarks="Although the 1986 adjustment included connections to Greenland and Mexico, it has not been adopted there. In Canada and US, replaced NAD27.",
)
""": :North American Datum 1983 (`EPSG:6269 <https://epsg.io/6269-datum>`_), coincident with WGS84 within original realization accuracy. Uses GRS 1980 ellipsoid."""

OSGB36 = Datum(
    name="Ordnance Survey of Great Britain 1936",
    code=6277,
    ellipsoid=AIRY_1830,
    to_wgs84=HelmertParameters(
        tx=446.448,
        ty=-125.157,
        tz=542.060,
        rx=0.1502,
        ry=0.2470,
        rz=0.8421,
        s=-20.4894,
    ),
    remarks="The average accuracy of OSTN compared to the old triangulation network (down to 3rd order) is 0.1m. With the introduction of OSTN15, the area for OGSB36 has effectively been extended from Britain to cover the adjacent UK Continental Shelf.",
)
""": :Ordnance Survey of Great Britain 1936 (`EPSG:6277 <https://epsg.io/6277-datum>`_). Uses Airy 1830 ellipsoid."""

WGS84 = Datum(
    name="World Geodetic System 1984 ensemble",
    code=6326,
    ellipsoid=WGS_84,
    to_wgs84=HelmertParameters(tx=0.0, ty=0.0, tz=0.0, rx=0.0, ry=0.0, rz=0.0, s=0.0),
    remarks="EPSG::6326 has been the then current realization. No distinction is made between the original and subsequent (G730, G873, G1150, G1674, G1762, G2139 and G2296) WGS 84 frames. Since 1997, WGS 84 has been maintained within 10cm of the then current ITRF.",
)
""": :World Geodetic System 1984 (`EPSG:6326 <https://epsg.io/6326-datum>`_), the global reference datum for GPS. Uses WGS 84 datum."""
