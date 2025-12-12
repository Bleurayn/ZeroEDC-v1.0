import hashlib
import time
import json

ledger = []  # In production: immutable cloud storage

def certify(value, patient_id, variable, source_hash, twin_confidence):
    record = {
        "timestamp": time.time(),
        "patient_id": patient_id,
        "variable": variable,
        "value": value,
        "source_hash": source_hash or "none",
        "twin_confidence": twin_confidence,
        "final_confidence": min(1.0, twin_confidence + 0.1),
        "previous_hash": ledger[-1]["hash"] if ledger else "GENESIS"
    }
    record["hash"] = hashlib.sha3_256(json.dumps(record, sort_keys=True).encode()).hexdigest()
    ledger.append(record)
    return record["hash"], record["final_confidence"]

if __name__ == "__main__":
    hash1, conf = certify(7.2, "P003", "HbA1c", "sha256:ab12…", 0.994)
    print(f"Certified with confidence {conf:.4f} → hash {hash1}")
