"""Generate fake ticket data for benchmarking."""

from datetime import timedelta
from decimal import Decimal

from faker import Faker

from domain.ticket import Ticket


def generate_fake_tickets(count: int, seed: int = 42) -> list[Ticket]:
    """Generate deterministic fake tickets for benchmarking.

    Args:
        count: Number of tickets to generate
        seed: Random seed for reproducibility

    Returns:
        List of fake Ticket objects
    """
    fake = Faker()
    Faker.seed(seed)

    zones = ["Blue", "Green", "Red", "Yellow", "Orange"]
    tickets = list[Ticket]()

    for i in range(count):
        ticket_code = f"{i:010d}"
        car_plate = fake.license_plate()
        rate_name = fake.random_element(zones)
        starting_date_time = fake.date_time_between(start_date="-30d", end_date="now")
        duration_minutes = fake.random_int(min=30, max=480)  # 30 min to 8 hours
        ending_date_time = starting_date_time + timedelta(minutes=duration_minutes)
        price = Decimal(str(round(fake.random.uniform(0.50, 20.00), 2)))
        payment_id = f"PAY{fake.random_int(min=100000000, max=999999999)}"

        ticket = Ticket(
            ticket_code=ticket_code,
            car_plate=car_plate,
            rate_name=rate_name,
            starting_date_time=starting_date_time,
            ending_date_time=ending_date_time,
            price=price,
            payment_id=payment_id,
        )
        tickets.append(ticket)

    return tickets
