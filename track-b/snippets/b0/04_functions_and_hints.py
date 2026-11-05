"""Name a reusable calculation. Try: call with named arguments."""


def quote_transport(container_count: int, usd_per_container: float) -> float:
    """Return a synthetic flat transport quote for positive inputs."""
    if container_count <= 0 or usd_per_container <= 0:
        raise ValueError("Count and rate must be positive.")
    return container_count * usd_per_container


quote_usd = quote_transport(3, 120.0)
print(f"Transport quote: USD {quote_usd:.2f}")

