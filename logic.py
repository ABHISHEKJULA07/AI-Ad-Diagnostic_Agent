def detect_issue(query):
    query = query.lower()

    if "not spending" in query:
        return "NOT_SPENDING"
    elif "rejected" in query:
        return "AD_REJECTED"
    elif "low reach" in query:
        return "LOW_REACH"
    else:
        return "UNKNOWN"


def check_rules(data):
    if data["campaign_status"] == "paused":
        return "Campaign is paused"
    elif data["budget"] < 10:
        return "Budget too low"
    elif not data["ad_approved"]:
        return "Ad not approved"
    else:
        return "No major issue found"