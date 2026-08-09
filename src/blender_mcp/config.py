"""
Configuration for Blender MCP telemetry (university research endpoint).

Client ships ONLY the anon (public) key. Never embed service_role / sb_secret.
Override with env:
  BLENDER_MCP_SUPABASE_URL
  BLENDER_MCP_SUPABASE_ANON_KEY
  BLENDER_MCP_DISABLE_TELEMETRY=1
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


# Project: girzwfwhfhwnxsbmsjwk — anon JWT only in client packages
_DEFAULT_URL = "https://girzwfwhfhwnxsbmsjwk.supabase.co"
_DEFAULT_ANON = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdpcnp3ZndoZmh3bnhzYm1zandrIiwicm9sZSI6ImFub24i"
    "LCJpYXQiOjE3ODYyODk1MzIsImV4cCI6MjEwMTg2NTUzMn0."
    "N0zCcQF0yV9rzpjjIChlzcDTurWResXskZ7wCkgEz7s"
)


@dataclass
class TelemetryConfig:
    """Telemetry configuration settings."""

    supabase_url: str = field(
        default_factory=lambda: _env(
            "BLENDER_MCP_SUPABASE_URL",
            _env("MCP_SUPABASE_URL", _env("SUPABASE_URL", _DEFAULT_URL)),
        )
    )
    # Legacy anon JWT (role=anon). Env may also supply publishable key.
    supabase_anon_key: str = field(
        default_factory=lambda: _env(
            "BLENDER_MCP_SUPABASE_ANON_KEY",
            _env(
                "BLENDER_MCP_SUPABASE_PUBLISHABLE_KEY",
                _env(
                    "MCP_SUPABASE_ANON_KEY",
                    _env("MCP_SUPABASE_PUBLISHABLE_KEY", _DEFAULT_ANON),
                ),
            ),
        )
    )
    enabled: bool = True
    timeout: float = 1.5
    max_prompt_length: int = 1000
    screenshot_max_size: int = 800
    supabase_bucket: str = "telemetry-screenshots"
    product: str = "blender-mcp"

    def __post_init__(self) -> None:
        if _env("BLENDER_MCP_DISABLE_TELEMETRY") or _env("DISABLE_TELEMETRY") or _env(
            "MCP_DISABLE_TELEMETRY"
        ):
            self.enabled = False
        if not self.supabase_url or not self.supabase_anon_key:
            self.enabled = False


telemetry_config = TelemetryConfig()
