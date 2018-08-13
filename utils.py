import numpy as np


def getRequiredReturn(cash_flow_list, funds_available):
    """Calculate a required rate of return.

    Find the minimum return such that money on hand never goes below 0.
    Note: np.irr expects deposits to be negative, so flip the sign.
    Args:
        cash_flow_list {list}: List of expected expenditures and incomes.
        funds_available {Decimal}: Sum of currently invested funds.
    Returns:
        required_return {float}: Rate required to break even for all years.
    """
    cash_flows = [funds_available]
    cash_flows.extend(cash_flow_list)
    irr = np.irr(cash_flows)
    if np.isnan(irr):
        return 0
    return 1 + irr
