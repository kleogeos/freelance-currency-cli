import json
import subprocess
import sys

PY = sys.executable
SCRIPT = "currency.py"


def run(*args):
    r = subprocess.run([PY, SCRIPT, *args], capture_output=True, text=True)
    return r


def test_manual_rate_basic():
    r = run("--amount", "100", "--from", "USDT", "--to", "RUB", "--rate", "83.5", "--json")
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["converted"] == 8350.0
    assert data["rate_source"] == "manual"
    assert data["rate_updated_utc"] is None


def test_manual_rate_rounding():
    r = run("--amount", "33.333", "--from", "USD", "--to", "EUR", "--rate", "0.9", "--json")
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["converted"] == round(33.333 * 0.9, 2)


def test_human_readable_output_has_both_amounts():
    r = run("--amount", "100", "--from", "USD", "--to", "RUB", "--rate", "80")
    assert r.returncode == 0, r.stderr
    assert "100.00 USD" in r.stdout
    assert "8,000.00 RUB" in r.stdout
    assert "(manual, --rate)" in r.stdout


def test_bad_currency_without_manual_rate_fails_cleanly():
    # No --rate given, so it must try the network and fail gracefully
    # (or, if network is reachable, fail because ZZZ isn't a real currency).
    r = run("--amount", "100", "--from", "USD", "--to", "ZZZ")
    assert r.returncode == 1
    assert "error:" in r.stderr
    assert "Traceback" not in r.stderr


def test_missing_required_arg_fails():
    r = run("--amount", "100", "--from", "USD")
    assert r.returncode != 0


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL: {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
