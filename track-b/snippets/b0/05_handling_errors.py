"""Handle an expected invalid booking. Try: add another invalid count."""


def quote_transport(container_count: int, usd_per_container: float) -> float:
    if container_count <= 0 or usd_per_container <= 0:
        raise ValueError("Count and rate must be positive.")
    return container_count * usd_per_container


for count in [3, 0]:
    try:
        quote_usd = quote_transport(count, 120.0)
        print("Quoted:", count, "containers for USD", quote_usd)
    except ValueError as error:
        print("Booking needs correction:", error)

