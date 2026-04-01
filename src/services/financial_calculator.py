import math


class FinancialCalculator:
    """Core financial calculation engine."""

    @staticmethod
    def compound_interest(
        principal: float, annual_rate: float, years: float, compounds_per_year: int = 12
    ) -> float:
        """Calculate compound interest.

        Returns the final amount (principal + interest).
        """
        if principal < 0:
            raise ValueError("Principal cannot be negative")
        if annual_rate < 0:
            raise ValueError("Annual rate cannot be negative")
        if years < 0:
            raise ValueError("Years cannot be negative")
        if compounds_per_year <= 0:
            raise ValueError("Compounds per year must be positive")

        return principal * (1 + annual_rate / compounds_per_year) ** (compounds_per_year * years)

    @staticmethod
    def simple_return(initial_value: float, final_value: float) -> float:
        """Calculate simple return as a percentage."""
        if initial_value == 0:
            return 0.0
        return ((final_value - initial_value) / initial_value) * 100

    @staticmethod
    def annualized_return(total_return_pct: float, years: float) -> float:
        """Calculate annualized return from total return percentage."""
        if years <= 0:
            raise ValueError("Years must be positive")
        return ((1 + total_return_pct / 100) ** (1 / years) - 1) * 100

    @staticmethod
    def sharpe_ratio(
        portfolio_return: float, risk_free_rate: float, portfolio_std_dev: float
    ) -> float:
        """Calculate Sharpe ratio for risk-adjusted return measurement."""
        if portfolio_std_dev == 0:
            return 0.0
        return (portfolio_return - risk_free_rate) / portfolio_std_dev

    @staticmethod
    def portfolio_variance(weights: list[float], returns_matrix: list[list[float]]) -> float:
        """Calculate portfolio variance given weights and covariance matrix."""
        n = len(weights)
        if n != len(returns_matrix) or any(len(row) != n for row in returns_matrix):
            raise ValueError("Dimensions of weights and covariance matrix must match")

        variance = 0.0
        for i in range(n):
            for j in range(n):
                variance += weights[i] * weights[j] * returns_matrix[i][j]
        return variance

    @staticmethod
    def portfolio_std_dev(weights: list[float], covariance_matrix: list[list[float]]) -> float:
        """Calculate portfolio standard deviation."""
        variance = FinancialCalculator.portfolio_variance(weights, covariance_matrix)
        return math.sqrt(max(variance, 0))

    @staticmethod
    def present_value(future_value: float, discount_rate: float, years: float) -> float:
        """Calculate present value of a future cash flow."""
        if years < 0:
            raise ValueError("Years cannot be negative")
        return future_value / (1 + discount_rate) ** years

    @staticmethod
    def future_value_annuity(
        payment: float, annual_rate: float, years: int, payments_per_year: int = 12
    ) -> float:
        """Calculate future value of regular annuity payments."""
        if annual_rate == 0:
            return payment * payments_per_year * years
        rate_per_period = annual_rate / payments_per_year
        total_periods = payments_per_year * years
        return payment * (((1 + rate_per_period) ** total_periods - 1) / rate_per_period)

    @staticmethod
    def debt_to_income_ratio(monthly_debt: float, monthly_income: float) -> float:
        """Calculate debt-to-income ratio as a percentage."""
        if monthly_income <= 0:
            raise ValueError("Monthly income must be positive")
        return (monthly_debt / monthly_income) * 100

    @staticmethod
    def emergency_fund_months(total_savings: float, monthly_expenses: float) -> float:
        """Calculate how many months of expenses an emergency fund covers."""
        if monthly_expenses <= 0:
            raise ValueError("Monthly expenses must be positive")
        return total_savings / monthly_expenses
