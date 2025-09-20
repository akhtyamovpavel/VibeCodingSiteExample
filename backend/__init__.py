"""Backend package initialization."""

# Expose commonly used helpers for convenience when imported as a package.
try:  # pragma: no cover - optional re-export
    from . import database, models, schemas  # noqa: F401
except ImportError:
    # When executed as scripts, relative imports may not resolve; this module
    # still marks the directory as a package without failing eagerly.
    pass
