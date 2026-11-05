"""Quote one synthetic container pickup. Try: change the container count."""

container_count = 3
usd_per_container = 120.0
budget_usd = 500.0

quote_usd = container_count * usd_per_container
budget_left_usd = budget_usd - quote_usd

print("Transport quote (USD):", quote_usd)
print("Budget left (USD):", budget_left_usd)

