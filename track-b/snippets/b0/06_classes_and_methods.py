"""Keep a quote's data and behavior together. Try: create a second quote."""

from dataclasses import dataclass


@dataclass
class TransportQuote:
    container_count: int
    usd_per_container: float

    def total_usd(self) -> float:
        return self.container_count * self.usd_per_container


quote = TransportQuote(container_count=3, usd_per_container=120.0)
print("Container count:", quote.container_count)
print("Total (USD):", quote.total_usd())

