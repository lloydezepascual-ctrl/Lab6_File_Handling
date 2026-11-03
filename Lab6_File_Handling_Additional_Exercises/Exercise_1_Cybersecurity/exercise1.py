
import csv
import json
import shutil
from collections import Counter

SEED_DIGIT = 1
ID_SUM = 18
TARGET_YEAR = 2015 + SEED_DIGIT

# Read CSV
with open("Global_Cybersecurity_Threats_2015-2024.csv", "r") as file:
    data = list(csv.DictReader(file))

# Filter incidents by year
incidents = [row for row in data if row["Year"] == str(TARGET_YEAR)]

# Count attack types
attacks = Counter(row["Attack Type"] for row in incidents)

# Calculate financial loss
valid = []

for row in incidents:
    try:
        loss = float(row["Financial Loss (in Million $)"])
        if loss >= 0:
            valid.append((loss, row))
    except ValueError:
        pass

total = sum(loss for loss, row in valid)
average = total / len(valid) if valid else 0

# Get top 5 incidents
top5 = sorted(valid, key=lambda x: -x[0])[:5]
top5_data = [row for loss, row in top5]

# Export filtered CSV
with open("filtered_incidents.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(incidents)

# Export top 5 JSON
with open("top5_incidents.json", "w") as file:
    json.dump(top5_data, file, indent=4)

# Create backup
shutil.copy("top5_incidents.json", "top5_backup.json")

# Verify backup
with open("top5_incidents.json", "rb") as original:
    with open("top5_backup.json", "rb") as backup:
        verified = original.read() == backup.read()

# Generate report
with open("incident_report.txt", "w") as file:
    file.write(f"Target Year: {TARGET_YEAR}\n")
    file.write(f"Total Incidents: {len(incidents)}\n")
    file.write(f"Attack Types: {dict(attacks)}\n")
    file.write(f"Total Financial Loss: {total:.2f} Million $\n")
    file.write(f"Average Financial Loss: {average:.2f} Million $\n")
    file.write(f"Top 5 Incidents: {top5_data}\n")
    file.write(f"Backup Verified: {verified}\n")

# Display results
print("CYBERSECURITY INCIDENT REPORT")
print("Target Year:", TARGET_YEAR)
print("Total Incidents:", len(incidents))
print("Attack Types:", dict(attacks))
print("Total Financial Loss:", round(total, 2))
print("Average Financial Loss:", round(average, 2))
print("\nTOP 5 COSTLIEST INCIDENTS:")

for loss, row in top5:
    print(row["Country"], row["Attack Type"], loss)

print("\nBackup Verified:", verified)
print("EXERCISE 1 COMPLETED!")
