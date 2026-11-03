
import csv
import json
import shutil
from collections import Counter

SEED_DIGIT = 1
ID_SUM = 18
TARGET_OS = "iOS"
TARGET_CLASS = 2

# Read dataset
with open("user_behavior_dataset.csv", newline="", encoding="utf-8") as f:
    data = list(csv.DictReader(f))

# Filter users
selected = [
    row for row in data
    if row["Operating System"] == TARGET_OS
    and int(row["User Behavior Class"]) == TARGET_CLASS
]

# Calculate averages
battery = [float(row["Battery Drain (mAh/day)"]) for row in data]
usage = [float(row["Data Usage (MB/day)"]) for row in data]

avg_battery = sum(battery) / len(battery)
avg_usage = sum(usage) / len(usage)

# Export filtered CSV
fields = [
    "User ID",
    "Device Model",
    "Operating System",
    "Battery Drain (mAh/day)",
    "Data Usage (MB/day)"
]

with open("filtered_users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for row in selected:
        writer.writerow({field: row[field] for field in fields})

# Create summary
summary = {
    "Total Records": len(data),
    "Selected OS": TARGET_OS,
    "Selected Behavior Class": TARGET_CLASS,
    "Matching Users": len(selected),
    "Average Battery Drain": round(avg_battery, 2),
    "Average Data Usage": round(avg_usage, 2),
    "Behavior Class Counts": dict(Counter(
        row["User Behavior Class"] for row in data
    ))
}

# Export JSON
with open("usage_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4)

# Create backup
shutil.copy("filtered_users.csv", "users_backup.csv")

# Verify backup
verified = (
    open("filtered_users.csv", "rb").read()
    == open("users_backup.csv", "rb").read()
)

# Create report
with open("exercise2_report.txt", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4)

# Display results
print(json.dumps(summary, indent=4))
print("Backup Verified:", verified)
print("EXERCISE 2 COMPLETED!")