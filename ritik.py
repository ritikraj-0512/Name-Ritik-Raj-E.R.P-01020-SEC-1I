import json
import os

FILE_NAME = "services.txt"
GST_RATE = 0.18
STATUSES = ["Pending", "In Progress", "Completed"]

PRICE_LIST = {
    "Oil Change": 1500,
    "Wheel Alignment": 800,
    "Full Service": 4500,
    "Brake Repair": 2200,
}


class ServiceRecord:
    def __init__(self, reg_no, owner, vehicle, service, status="Pending"):
        self.reg_no = reg_no
        self.owner = owner
        self.vehicle = vehicle
        self.service = service
        self.status = status

    def calculate_cost(self):
        """Price from the price list plus 18% GST."""
        return round(PRICE_LIST[self.service] * (1 + GST_RATE), 2)

    def display(self):
        return (f"{self.reg_no} | {self.owner} | {self.vehicle} | {self.service} | "
                f"Cost incl. 18% GST: Rs. {self.calculate_cost():.2f} | "
                f"Status: {self.status}")

    def to_dict(self):
        return {"reg_no": self.reg_no, "owner": self.owner,
                "vehicle": self.vehicle, "service": self.service,
                "status": self.status}



def save_records(records):
    with open(FILE_NAME, "w") as f:
        json.dump({k: v.to_dict() for k, v in records.items()}, f, indent=2)


def load_records():
    records = {}
    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        return records
    try:
        with open(FILE_NAME) as f:
            data = json.load(f)
        for reg, d in data.items():
            records[reg] = ServiceRecord(d["reg_no"], d["owner"], d["vehicle"],
                                         d["service"], d["status"])
    except (json.JSONDecodeError, KeyError):
        print("Warning: could not read services.txt, starting empty.")
    return records


def match(value, options):
    """Case-insensitive match against a list of valid options."""
    for opt in options:
        if value.strip().lower() == opt.lower():
            return opt
    return None



def add_record(records):
    reg_no = input("Reg no: ").strip().upper()
    owner = input("Owner: ").strip()
    vehicle = input("Vehicle: ").strip()
    service_in = input("Service: ").strip()

    service = match(service_in, PRICE_LIST)
    if service is None:
        print("Invalid service type. Choose from: " + ", ".join(PRICE_LIST) + ".")
        return
    if reg_no in records:
        print(f"Record already exists for {reg_no}.")
        return

    rec = ServiceRecord(reg_no, owner, vehicle, service)
    records[reg_no] = rec
    save_records(records)
    print(f"Record added. {reg_no} | {service} | "
          f"Cost incl. 18% GST: Rs. {rec.calculate_cost():.2f} | "
          f"Status: {rec.status}")


def view_records(records):
    if not records:
        print("No records available.")
        return
    for rec in records.values():
        print(rec.display())


def update_status(records):
    reg_no = input("Reg no: ").strip().upper()
    new_in = input("New status: ").strip()

    if reg_no not in records:
        print(f"No record found for {reg_no}.")
        return
    new_status = match(new_in, STATUSES)
    if new_status is None:
        print("Invalid status. Choose from: " + ", ".join(STATUSES) + ".")
        return

    old = records[reg_no].status
    records[reg_no].status = new_status
    save_records(records)
    print(f"Status updated: {old} -> {new_status}")


def delete_record(records):
    reg_no = input("Reg no: ").strip().upper()
    if reg_no not in records:
        print(f"No record found for {reg_no}.")
        return
    del records[reg_no]
    save_records(records)
    print(f"Record for {reg_no} deleted.")



def main():
    records = load_records()
    while True:
        print("\n--- Vehicle Service Management System ---")
        print("1. Add record")
        print("2. View records")
        print("3. Update status")
        print("4. Delete record")
        print("5. Exit")
        try:
            choice = input("Menu: ").strip().lower()
        except EOFError:
            break

        if choice in ("1", "add record", "add"):
            add_record(records)
        elif choice in ("2", "view records", "view"):
            view_records(records)
        elif choice in ("3", "update status", "update"):
            update_status(records)
        elif choice in ("4", "delete record", "delete"):
            delete_record(records)
        elif choice in ("5", "exit"):
            print("Goodbye!")
            break
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()