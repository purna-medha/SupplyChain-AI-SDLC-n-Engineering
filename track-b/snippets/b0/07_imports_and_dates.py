"""Use date objects for a fixed classroom case. Try: change the as-of date."""

from datetime import date

discharge_date = date(2026, 11, 1)
calculation_date = date(2026, 11, 8)
free_days = 5

dwell_days = max(0, (calculation_date - discharge_date).days)
overdue_days = max(0, dwell_days - free_days)

print("As of:", calculation_date.isoformat())
print("Dwell days:", dwell_days)
print("Overdue days:", overdue_days)

