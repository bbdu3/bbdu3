import importlib.util
import os
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("GITHUB_TOKEN", "unit-test-token")

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "generate_biweekly_report.py"
spec = importlib.util.spec_from_file_location("weekly_report", MODULE_PATH)
weekly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weekly)
BJ = weekly.BEIJING_TZ


def dt(y, m, d, hour=0, minute=0):
    return datetime(y, m, d, hour, minute, tzinfo=BJ)


class WeeklyPeriodTests(unittest.TestCase):
    def test_migration_and_boundary_selection(self):
        self.assertEqual(weekly.latest_periods(dt(2026, 8, 14, 23, 59)), [(dt(2026, 8, 10), dt(2026, 8, 15))])
        self.assertEqual(weekly.latest_periods(dt(2026, 8, 15, 0, 10)), [
            (dt(2026, 8, 10), dt(2026, 8, 15)),
            (dt(2026, 8, 15), dt(2026, 8, 22)),
        ])
        self.assertEqual(weekly.latest_periods(dt(2026, 8, 22, 0, 10)), [
            (dt(2026, 8, 15), dt(2026, 8, 22)),
            (dt(2026, 8, 22), dt(2026, 8, 29)),
        ])

    def test_periods_have_no_gaps_or_overlap(self):
        periods = weekly.generate_periods(dt(2026, 10, 3, 0, 10))
        self.assertTrue(all(left[1] == right[0] for left, right in zip(periods, periods[1:])))
        self.assertTrue(all((end - start).days == 7 for start, end in periods[1:]))

    def test_invalid_interval_is_rejected(self):
        with self.assertRaises(ValueError):
            weekly.validate_periods([(dt(2026, 8, 15), dt(2026, 8, 15))])

    def test_filename_display_uses_friday(self):
        end = dt(2026, 8, 22)
        self.assertEqual(weekly.period_last_moment(end).strftime("%Y.%m.%d"), "2026.08.21")
        placeholder = weekly.generate_placeholder_report(dt(2026, 8, 15), end)
        self.assertIn("2026年8月15日 — 2026年8月21日", placeholder)


class TimeBoundaryTests(unittest.TestCase):
    def test_api_query_converts_beijing_interval_to_utc(self):
        queries = []
        def fake_search(endpoint, query, **kwargs):
            queries.append((endpoint, query))
            return []
        with patch.object(weekly, "search_items", side_effect=fake_search), \
             patch.object(weekly, "api_get", return_value=[]), \
             patch.object(weekly.time, "sleep", return_value=None):
            weekly.fetch_period_data(dt(2026, 8, 10), dt(2026, 8, 15))
        self.assertEqual(len(queries), 3)
        for _, query in queries:
            self.assertIn("2026-08-09T16:00:00Z", query)
            self.assertIn("2026-08-14T15:59:59Z", query)

    def test_daily_activity_uses_beijing_calendar_date(self):
        stats = {"prs": [{"created_at": "2026-08-10T17:00:00Z", "number": 1, "repository_url": "https://api.github.com/repos/a/b"}], "issues": [], "commits": []}
        daily, _ = weekly.analyze_daily_activity(stats, dt(2026, 8, 10), dt(2026, 8, 15))
        self.assertEqual(daily["2026-08-11"], 1)

    def test_api_timestamp_display_is_beijing_date(self):
        self.assertEqual(weekly.fmt_api_date_beijing("2026-08-14T17:00:00Z"), "2026-08-15")


if __name__ == "__main__":
    unittest.main()