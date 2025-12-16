#!/usr/bin/env python3
"""
Generate practical email templates for a local environment/aquaculture beat.

Usage:
  python generate_email_templates.py --output email_templates.md
"""
import argparse
from pathlib import Path

TEMPLATES = {
    "request_policy_comment": (
        "Request for Policy Comment",
        "Subject: Request for comment on [policy/agenda item] in [place]\n\n"
        "Hello [Title Lastname],\n\n"
        "I'm covering [topic] for the [Outlet] in [County/Town]. Ahead of [meeting/hearing/date], I'd like your comment on [specific proposal/decision], including:\n"
        "- What the change would do in [jurisdiction]\n"
        "- Timeline and public input opportunities\n"
        "- Key data or reports informing your position\n\n"
        "Please share any documents or contacts you recommend. My deadline is [time].\n\n"
        "Best,\n[Name]\n[Outlet]\n[Phone]"
    ),
    "request_science_explanation": (
        "Request for Scientific Explanation",
        "Subject: Quick help understanding [metric/report] in [river/area]\n\n"
        "Hi [Dr./Prof. Lastname],\n\n"
        "Could you briefly explain [term/metric] in the context of [river/monitoring program]?\n"
        "I’m trying to understand what a change from [X] to [Y] means for [local impact].\n"
        "If possible, could you point me to a short report or figure?\n\n"
        "Thank you,\n[Name]\n[Outlet]\n[Phone]"
    ),
    "request_community_perspective": (
        "Request for Community Perspective",
        "Subject: Quick interview about [issue] near [place]\n\n"
        "Hello [Name],\n\n"
        "I’m reporting on [issue] affecting [neighborhood/riverfront]. I’d like to hear your perspective on how this shows up day to day,\n"
        "and who’s most impacted. If you’re available, could we talk for 10–15 minutes by phone or in person this week?\n\n"
        "Thanks very much,\n[Name]\n[Outlet]\n[Phone]"
    ),
    "follow_up_late_response": (
        "Follow-Up on Late Response",
        "Subject: Quick follow-up on [issue/request]\n\n"
        "Hello [Title Lastname],\n\n"
        "I wanted to follow up on my request from [date] regarding [issue]. My deadline is [time];\n"
        "even a short statement confirming [position/status/timeline] would be helpful.\n\n"
        "Best,\n[Name]\n[Outlet]\n[Phone]"
    ),
}


def main():
    ap = argparse.ArgumentParser(description="Write email templates for beat reporting.")
    ap.add_argument("--output", default="email_templates.md")
    args = ap.parse_args()

    lines = ["# Email Templates\n"]
    for key, (title, body) in TEMPLATES.items():
        lines.append(f"## {title}\n")
        lines.append(body + "\n\n")
    Path(args.output).write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"Wrote templates → {args.output}")

if __name__ == "__main__":
    main()
