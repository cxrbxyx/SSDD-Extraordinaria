"""Package for the calculator distribution."""

import os

import Ice

try:
    import RemoteCalculator  # noqa: F401

except ImportError:
    slice_path = os.path.join(
        os.path.dirname(__file__),
        "remotecalculator.ice",
    )

    Ice.loadSlice(slice_path)
    import RemoteCalculator  # noqa: F401
