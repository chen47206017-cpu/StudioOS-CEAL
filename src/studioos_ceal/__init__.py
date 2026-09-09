"""StudioOS-CEAL public API."""

from .contracts import ContractError, validate_task_package
from .engine import PolicyEngine
from .matrix import generate_scenarios
from .runner import run_assurance

__all__ = [
    "ContractError",
    "PolicyEngine",
    "generate_scenarios",
    "run_assurance",
    "validate_task_package",
]

__version__ = "0.1.0"
