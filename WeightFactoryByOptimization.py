import WeightFactory


class WeightFactoryByOptimization(WeightFactory.WeightFactory):
    """Generates Weight objects to desired standards."""

    def Solve(self):
        """Actually run the solver.

        Returns:
            desired_allocations {dict}: Dictionary of tickers to percent
                allocations.
        """
        # TODO-implement
        pass

    def _getPMPTWeight(self):
        """Generate weights using PMPT (Post-Modern Portfolio Theory).

        The theory involves maximizing the Sortino Ratio, defined as
            R = Portfolio rate of return.
            T = Required rate of return.
            D = Portfolio downside risk
            S = Sortino ratio

            S = (R - T) / D

        Downside risk equals:
            r = Portfolio daily return.
            T = Required rate of return.
            n = Number of daily observations.
            D = Downside risk.

            D = SQRT(SUM(MIN(r-T, 0)^2) / n)

        Daily return is defined as:
            u = Stock's daily return.
            w = Stock's weight.
            r = Portfolio daily return.

            r = SUM(u*w)
        """
        # Note: Following link calculates everything, but relies on actual
        # returns instead of distributions.
        # http://www.turingfinance.com/computational-investing-with-python-week-one/
        # TODO-implement
        pass
