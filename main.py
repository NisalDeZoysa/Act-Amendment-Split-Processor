from src.tracker import AIAmendmentTracker

if __name__ == "__main__":
    base_pdf = "data/14-2010_E.pdf"
    amendments = ["data/24-2023_E.pdf"]

    tracker = AIAmendmentTracker(base_pdf, amendments)
    all_summaries = tracker.run()

    print("\n=== Extracted Changes ===")
    for summary in all_summaries:
        for change in summary["changes"]:
            print(f"Section {change['section']} ({change.get('subsection')}) → {change['change_type']}")
