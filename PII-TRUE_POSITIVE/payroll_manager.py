import csv

def export_payroll():
    employees = [
        {'name': 'John Doe', 'email': 'john.doe@example.com', 'ssn': '123-45-6789', 'salary': 80000},
        {'name': 'Jane Smith', 'email': 'jane.smith@example.org', 'ssn': '987-65-4321', 'salary': 95000}
    ]
    with open('payroll.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'email', 'ssn', 'salary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees:
            writer.writerow(emp)

if __name__ == '__main__':
    export_payroll()