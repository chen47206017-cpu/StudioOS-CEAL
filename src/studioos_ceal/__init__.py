"""StudioOS-CEAL public assurance API."""

from .contracts import ContractError, validate_task_package
from .engine import PolicyEngine
from .matrix import generate_scenarios
from .runner import run_assurance, verify_manifest

__all__ = [
    "ContractError",
    "PolicyEngine",
    "generate_scenarios",
    "run_assurance",
    "validate_task_package",
    "verify_manifest",
]

__version__ = "0.2.0"
