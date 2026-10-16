# freelance-currency-cli

![Test CLI](https://github.com/kleogeos/freelance-currency-cli/actions/workflows/test.yml/badge.svg)

Convert an invoice amount between currencies — USD, EUR, RUB, and 160+ others. The one tool in this suite that makes a network call: it fetches a live rate from [open.er-api.com](https://www.exchangerate-api.com/docs/free) (free, no API key, rates updated daily) unless you pass `--rate` yourself for an offline or manual conversion. No third-party dependencies — just the Python standard library.

```bash
python3 currency.py --amount 1000 --from USD --to RUB
```
```
1,000.00 USD = 83,873.79 RUB
Rate used: 1 USD = 83.873791 RUB (open.er-api.com, updated Fri, 16 Oct 2026 00:02:31 +0000)
```

## Why this exists

The other CLIs in this suite (`freelance-invoice-cli`, `freelance-rate-cli`, etc.) are deliberately offline — nothing leaves your machine. Currency conversion is the one exception: there's no honest way to get a live exchange rate without a network call. This tool is upfront about that trade-off and gives you an escape hatch (`--rate`) when you don't want it — useful if you're offline, behind a restrictive firewall, or want to use a specific rate (e.g. a stablecoin peg or a rate your client already quoted you) instead of the live market rate.

## Usage

```bash
# Live rate lookup
python3 currency.py --amount 500 --from EUR --to USD

# Manual rate (no network call) — e.g. pricing an invoice in USDT at a fixed 1:1 USD peg
python3 currency.py --amount 500 --from USDT --to RUB --rate 83.5

# JSON output, for piping into another tool
python3 currency.py --amount 1000 --from USD --to RUB --json
```

```json
{
  "amount": 1000.0,
  "from": "USD",
  "to": "RUB",
  "rate": 83.873791,
  "converted": 83873.79,
  "rate_source": "open.er-api.com",
  "rate_updated_utc": "Fri, 16 Oct 2026 00:02:31 +0000"
}
```

## Install

```bash
pip install freelance-currency-cli
```

Or just download `currency.py` — it's a single file with no dependencies.

## Notes

- Rates come from the European Central Bank's reference rates, redistributed daily by exchangerate-api.com's free tier — fine for invoicing estimates, not for high-frequency trading.
- RUB is included (unlike some ECB-direct feeds, which have excluded it since 2022) — this was the reason this specific free API was chosen over alternatives.
- Not tax or financial advice. For the actual rate used on a specific date for tax reporting, check your country's official source (e.g. the Central Bank of Russia's archive for RUB).

Part of a free toolkit for freelance admin: [invoice generator](https://github.com/kleogeos/freelance-invoice-cli), [rate calculator](https://github.com/kleogeos/freelance-rate-cli), [tax estimator](https://github.com/kleogeos/freelance-tax-cli), and more at [awesome-freelance-tools](https://github.com/kleogeos/awesome-freelance-tools).
