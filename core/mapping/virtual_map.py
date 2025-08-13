"""
Virtual Map management for portfolio data
"""

from typing import Dict, List, Optional
from copy import deepcopy
import pandas as pd


class VirtualMap:
    """Manages portfolio mappings throughout the validation process"""
    
    def __init__(self):
        self.data: Dict[str, dict] = {}
        self.is_frozen = False
        self.frozen_copy = None
    
    def add_portfolio(self, name: str, base_bid: float, target_cpa: Optional[float] = None):
        """Add or update portfolio in the map"""
        if self.is_frozen:
            return
        
        self.data[name] = {
            'base_bid': base_bid,
            'target_cpa': target_cpa,
            'is_ignored': False
        }
    
    def remove_portfolio(self, name: str):
        """Remove portfolio from the map (used for Ignore)"""
        if self.is_frozen:
            return
        
        if name in self.data:
            del self.data[name]
    
    def merge_completion_template(self, df: pd.DataFrame, bulk_portfolios: List[str]) -> Dict[str, str]:
        """
        Merge completion template with full override
        
        Args:
            df: Completion template DataFrame
            bulk_portfolios: List of portfolios from bulk file
            
        Returns:
            Dictionary of errors (if any)
        """
        if self.is_frozen:
            return {'error': 'Virtual Map is frozen'}
        
        errors = {}
        
        for _, row in df.iterrows():
            portfolio_name = row['Portfolio Name']
            base_bid = row['Base Bid']
            target_cpa = row.get('Target CPA', None)
            
            # Check if portfolio exists in bulk
            if portfolio_name not in bulk_portfolios:
                errors[portfolio_name] = f"Portfolio '{portfolio_name}' does not exist in Bulk file"
                continue
            
            # Handle Ignore
            if str(base_bid).strip().lower() == 'ignore':
                self.remove_portfolio(portfolio_name)
            else:
                # Validate base_bid
                try:
                    base_bid_float = float(base_bid)
                    if base_bid_float < 0:
                        errors[portfolio_name] = f"Invalid Base Bid value for portfolio: {portfolio_name}"
                        continue
                except (ValueError, TypeError):
                    errors[portfolio_name] = f"Base Bid is required for portfolio: {portfolio_name}"
                    continue
                
                # Validate target_cpa if provided
                target_cpa_float = None
                if target_cpa and str(target_cpa).strip():
                    try:
                        target_cpa_float = float(target_cpa)
                        if target_cpa_float < 0:
                            errors[portfolio_name] = f"Invalid Target CPA value for portfolio: {portfolio_name}"
                            continue
                    except (ValueError, TypeError):
                        errors[portfolio_name] = f"Invalid Target CPA value for portfolio: {portfolio_name}"
                        continue
                
                # Add/update portfolio
                self.add_portfolio(portfolio_name, base_bid_float, target_cpa_float)
        
        return errors
    
    def get_missing_portfolios(self, bulk_portfolios: List[str]) -> List[str]:
        """Get list of portfolios in bulk but not in virtual map"""
        vm_portfolios = set(self.data.keys())
        bulk_set = set(bulk_portfolios)
        return list(bulk_set - vm_portfolios)
    
    def get_excess_portfolios(self, bulk_portfolios: List[str]) -> List[str]:
        """Get list of portfolios in virtual map but not in bulk"""
        vm_portfolios = set(self.data.keys())
        bulk_set = set(bulk_portfolios)
        return list(vm_portfolios - bulk_set)
    
    def freeze(self):
        """Lock the Virtual Map for Step 3"""
        self.is_frozen = True
        self.frozen_copy = deepcopy(self.data)
    
    def unfreeze(self):
        """Unlock the Virtual Map when returning to Step 2"""
        self.is_frozen = False
        # Keep the current data, don't revert
    
    def get_data(self) -> Dict[str, dict]:
        """Get the current data (frozen copy if frozen)"""
        if self.is_frozen and self.frozen_copy:
            return self.frozen_copy
        return self.data
    
    def is_empty(self) -> bool:
        """Check if virtual map is empty"""
        return len(self.data) == 0
    
    def clear(self):
        """Clear all data"""
        if not self.is_frozen:
            self.data = {}
            self.frozen_copy = None