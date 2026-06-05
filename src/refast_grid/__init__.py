"""Spreadsheet component for refast

Provides the RefastGrid component for Refast applications.
"""

from pathlib import Path

from refast.extensions import Extension

from .components import RefastGrid


class RefastGridExtension(Extension):
    """
    RefastGrid extension for Refast.

    Spreadsheet component for refast

    Example:
        ```python
        from refast import RefastApp
        from refast_grid import RefastGrid, RefastGridExtension

        ui = RefastApp(extensions=[RefastGridExtension()])

        @ui.page("/")
        def home(ctx):
            return RefastGrid(
                value="Hello, World!",
            )
        ```

    For auto-discovery, install the package and it will be automatically loaded.
    """

    name = "refast-refast_grid"
    version = "0.1.0"
    description = "Spreadsheet component for refast"

    # Static assets to load (relative to static_path)
    scripts = ["refast-refast_grid.js"]
    styles = ["refast-refast_grid.css"]

    @property
    def static_path(self) -> Path:
        """Path to the static assets directory."""
        return Path(__file__).parent / "static"

    @property
    def components(self) -> list:
        """List of Python component classes provided by this extension."""
        return [RefastGrid]


__all__ = ["RefastGrid", "RefastGridExtension"]
