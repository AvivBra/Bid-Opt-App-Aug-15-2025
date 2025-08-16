"""
Optimizations Package
Contains all optimization implementations for Bid Optimizer
"""

from .base import BaseOptimization
from .zero_sales import ZeroSalesOptimization

__all__ = [
    "BaseOptimization",
    "ZeroSalesOptimization",
]

# Registry of available optimizations
OPTIMIZATION_REGISTRY = {
    "Zero Sales": ZeroSalesOptimization,
    # Future optimizations will be added here:
    # "Portfolio Bid Optimization": PortfolioBidOptimization,
    # "Budget Optimization": BudgetOptimization,
    # etc.
}


def get_optimization(name: str) -> BaseOptimization:
    """
    Factory function to get optimization instance by name

    Args:
        name: Name of the optimization

    Returns:
        Instance of the requested optimization

    Raises:
        ValueError: If optimization name not found
    """
    if name not in OPTIMIZATION_REGISTRY:
        raise ValueError(f"Unknown optimization: {name}")

    optimization_class = OPTIMIZATION_REGISTRY[name]
    return optimization_class()
