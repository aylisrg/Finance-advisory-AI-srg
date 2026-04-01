import pytest

from src.services.financial_calculator import FinancialCalculator


class TestCompoundInterest:
    def test_basic_compound_interest(self):
        result = FinancialCalculator.compound_interest(1000, 0.05, 10)
        assert round(result, 2) == 1647.01

    def test_zero_principal(self):
        result = FinancialCalculator.compound_interest(0, 0.05, 10)
        assert result == 0

    def test_zero_rate(self):
        result = FinancialCalculator.compound_interest(1000, 0, 10)
        assert result == 1000

    def test_zero_years(self):
        result = FinancialCalculator.compound_interest(1000, 0.05, 0)
        assert result == 1000

    def test_negative_principal_raises(self):
        with pytest.raises(ValueError, match="Principal cannot be negative"):
            FinancialCalculator.compound_interest(-1000, 0.05, 10)

    def test_negative_rate_raises(self):
        with pytest.raises(ValueError, match="Annual rate cannot be negative"):
            FinancialCalculator.compound_interest(1000, -0.05, 10)

    def test_annual_compounding(self):
        result = FinancialCalculator.compound_interest(1000, 0.10, 1, 1)
        assert round(result, 2) == 1100.00

    def test_large_principal(self):
        result = FinancialCalculator.compound_interest(1_000_000, 0.07, 30)
        assert result > 1_000_000


class TestSimpleReturn:
    def test_positive_return(self):
        result = FinancialCalculator.simple_return(100, 150)
        assert result == 50.0

    def test_negative_return(self):
        result = FinancialCalculator.simple_return(100, 80)
        assert result == -20.0

    def test_zero_initial_value(self):
        result = FinancialCalculator.simple_return(0, 100)
        assert result == 0.0

    def test_no_change(self):
        result = FinancialCalculator.simple_return(100, 100)
        assert result == 0.0


class TestAnnualizedReturn:
    def test_basic_annualized(self):
        result = FinancialCalculator.annualized_return(100, 5)
        assert round(result, 2) == 14.87

    def test_zero_years_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.annualized_return(50, 0)

    def test_one_year(self):
        result = FinancialCalculator.annualized_return(25, 1)
        assert result == 25.0


class TestSharpeRatio:
    def test_positive_sharpe(self):
        result = FinancialCalculator.sharpe_ratio(0.12, 0.03, 0.10)
        assert round(result, 2) == 0.90

    def test_zero_std_dev(self):
        result = FinancialCalculator.sharpe_ratio(0.12, 0.03, 0)
        assert result == 0.0


class TestPresentValue:
    def test_basic_pv(self):
        result = FinancialCalculator.present_value(1000, 0.05, 5)
        assert round(result, 2) == 783.53

    def test_zero_years(self):
        result = FinancialCalculator.present_value(1000, 0.05, 0)
        assert result == 1000


class TestFutureValueAnnuity:
    def test_basic_annuity(self):
        result = FinancialCalculator.future_value_annuity(500, 0.06, 10)
        assert result > 0

    def test_zero_rate(self):
        result = FinancialCalculator.future_value_annuity(500, 0, 10)
        assert result == 500 * 12 * 10


class TestDebtToIncome:
    def test_basic_dti(self):
        result = FinancialCalculator.debt_to_income_ratio(2000, 6000)
        assert round(result, 2) == 33.33

    def test_zero_income_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.debt_to_income_ratio(2000, 0)


class TestEmergencyFundMonths:
    def test_basic(self):
        result = FinancialCalculator.emergency_fund_months(30000, 5000)
        assert result == 6.0

    def test_zero_expenses_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.emergency_fund_months(30000, 0)
