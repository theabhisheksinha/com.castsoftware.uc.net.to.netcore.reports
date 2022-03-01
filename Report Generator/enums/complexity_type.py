from enum import Enum


class ComplexityType(Enum):
    """
    Type of Imaging Artifacts
    """
    ESSENTIAL = "Essential Complexity",
    INTEGRATION = "Integration Complexity",
    CYCLOMATIC = "Cyclomatic Complexity"
