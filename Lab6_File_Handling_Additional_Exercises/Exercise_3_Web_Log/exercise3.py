
import csv
import json
import shutil
from collections import Counter

SEED_DIGIT = 1
ID_SUM = 18
RECORD_LIMIT = 1000 + ID_SUM
TARGET_STATUS = "3"

# Process only the first 1,018 records
status_counts = Counter()
url_counts = Counter()
selected = []

with open("weblog.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader):
        if i >= RECORD_LIMIT:
            break

        if len(row) < 4:
            continue

        ip, time, request, status = row[:4]

        status = status.strip()
        url = request.split(" ")[1] if len(request.split()) >= 2 else request

        status_counts[status] += 1

        if status.startswith(TARGET_STATUS):
            selected.append({
                "IP": ip,
                "Time": time,
                "URL": url,
                "Status": status
            })
            url_counts[url] += 1

# Export selected records to CSV
fields = ["IP", "Time", "URL", "Status"]

with open("redirect_requests.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(selected)

# Create JSON summary
summary = {
    "Records Processed": min(RECORD_LIMIT, sum(status_counts.values())),
    "Target Status Class": "3xx",
    "Matching Records": len(selected),
    "Status Code Counts": dict(status_counts),
    "Top 5 URLs": [
        {"URL": url, "Count": count}
        for url, count in url_counts.most_common(5)
    ]
}

with open("web_log_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4)

# Create backup and verify
shutil.copy("redirect_requests.csv", "redirect_backup.csv")

verified = (
    open("redirect_requests.csv", "rb").read()
    == open("redirect_backup.csv", "rb").read()
)

# Create report
with open("web_log_report.txt", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4)

print(json.dumps(summary, indent=4))
print("Backup Verified:", verified)
print("EXERCISE 3 COMPLETED!")
