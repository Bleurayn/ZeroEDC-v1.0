def offline_certify(value, twin_confidence):
    if twin_confidence > 0.98:
        return "Auto-certified offline"
    return "Sync required"

if __name__ == "__main__":
    print(offline_certify(7.2, 0.994))
