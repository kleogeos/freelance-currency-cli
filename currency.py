#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.request

API_URL = "https://open.er-api.com/v6/latest/{base}"


def fetch_rate(base, quote, timeout=10):
    url = API_URL.format(base=base.upper())
    with urllib.request.urlopen(url, timeout=timeout) as r:
        data = json.load(r)
    if data.get("result") != "success":
        raise RuntimeError(f"rate lookup failed: {data.get('error-type', 'unknown error')}")
    rates = data["rates"]
    if quote.upper() not in rates:
        raise RuntimeError(f"currency '{quote}' not found (base was '{base}')")
    return rates[quote.upper()], data.get("time_last_update_utc")


def compute(amount, rate):
    return round(amount * rate, 2)


def main():
    p = argparse.ArgumentParser(
        prog="freelance-currency",
        description=(
            "Convert an invoice amount between currencies. Unlike the other tools in this "
            "suite, this one makes a network call (to open.er-api.com, free, no API key, "
            "rates updated daily) unless you pass --rate yourself. No dependencies beyond "
            "the Python standard library."
        ),
    )
    p.add_argument("--amount", type=float, required=True, help="Amount to convert")
    p.add_argument("--from", dest="base", required=True, help="Source currency code, e.g. USD")
    p.add_argument("--to", dest="quote", required=True, help="Target currency code, e.g. RUB")
    p.add_argument(
        "--rate",
        type=float,
        default=None,
        help="Skip the network lookup and use this exchange rate directly "
        "(1 unit of --from equals this many units of --to) — useful offline, "
        "or for a rate not covered by the API (e.g. a specific crypto peg).",
    )
    p.add_argument("--json", action="store_true", help="Output as JSON")
    args = p.parse_args()

    updated = None
    if args.rate is not None:
        rate = args.rate
    else:
        rate, updated = fetch_rate(args.base, args.quote)

    converted = compute(args.amount, rate)

    if args.json:
        print(json.dumps(
            {
                "amount": args.amount,
                "from": args.base.upper(),
                "to": args.quote.upper(),
                "rate": rate,
                "converted": converted,
                "rate_source": "manual" if args.rate is not None else "open.er-api.com",
                "rate_updated_utc": updated,
            },
            indent=2,
        ))
        return

    print(f"{args.amount:,.2f} {args.base.upper()} = {converted:,.2f} {args.quote.upper()}")
    print(f"Rate used: 1 {args.base.upper()} = {rate} {args.quote.upper()}", end="")
    if args.rate is not None:
        print(" (manual, --rate)")
    else:
        print(f" (open.er-api.com, updated {updated})")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1)
