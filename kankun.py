#!/usr/bin/env python3
import argparse
import csv
import os
import socket
import struct
import sys
from urllib.error import URLError, HTTPError
from urllib.request import urlopen

try:
    import fcntl  # POSIX only
except ImportError:  # pragma: no cover
    fcntl = None


# Author: Yahya Khaled (original)
# Python 3 port + fixes


DEFAULT_TIMEOUT_SCAN_SECS = 0.15
DEFAULT_TIMEOUT_HTTP_SECS = 5.0
DEFAULT_PORT = 80


def devices_list_path() -> str:
    return os.path.join(os.path.expanduser("~"), ".kankun-devices.list")


def get_ip_address(ifname: str) -> str:
    """
    Return IPv4 address for a given network interface (Linux/Unix).
    """
    if fcntl is None:
        raise RuntimeError("Interface lookup via ioctl requires a POSIX system (fcntl not available).")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ifname_b = ifname[:15].encode("utf-8", "ignore")
        res = fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack("256s", ifname_b),
        )
        return socket.inet_ntoa(res[20:24])
    finally:
        s.close()


def http_get_text(url: str, timeout: float) -> str:
    with urlopen(url, timeout=timeout) as resp:
        data = resp.read()
    # Devices typically return ASCII-ish payloads; be forgiving.
    return data.decode("utf-8", errors="replace")


def discover_kankun_devices(ifname: str) -> list[tuple[str, str]]:
    """
    Scan the /24 of the interface IP for Kankun devices by fetching /cgi-bin/relay.cgi?
    Returns list of tuples: (ip=..., response_text)
    """
    local_ip = get_ip_address(ifname)
    octets = local_ip.split(".")
    if len(octets) != 4:
        raise RuntimeError(f"Unexpected local IP format: {local_ip}")

    prefix = ".".join(octets[:3])
    found: list[tuple[str, str]] = []

    for i in range(1, 254):
        address = f"{prefix}.{i}"
        url = f"http://{address}/cgi-bin/relay.cgi?"
        try:
            # Keep it fast while scanning; avoid separate TCP connect + HTTP fetch.
            text = http_get_text(url, timeout=DEFAULT_TIMEOUT_SCAN_SECS).rstrip()
            print((address, text))
            found.append((f"ip={address}", text))
        except (URLError, HTTPError, socket.timeout, OSError):
            pass

    return found


def write_devices_list(rows: list[tuple[str, str]]) -> None:
    path = devices_list_path()
    with open(path, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out)
        for row in rows:
            w.writerow(row)


def read_devices_list() -> tuple[list[str], list[str]]:
    path = devices_list_path()
    if not os.path.exists(path):
        return [], []

    ips: list[str] = []
    responses: list[str] = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or len(row) < 2:
                continue
            ips.append(row[0])
            responses.append(row[1])
    return ips, responses


def find_matching_devices(device_query: str, ips: list[str], responses: list[str]) -> list[tuple[str, str]]:
    q = (device_query or "").lower()
    matches: list[tuple[str, str]] = []
    for ip_tag, resp in zip(ips, responses):
        if q in (resp or "").lower():
            matches.append((ip_tag, resp))
    return matches


def device_ip_from_tag(ip_tag: str) -> str:
    # Stored as ip=1.2.3.4
    if ip_tag.startswith("ip="):
        return ip_tag.split("ip=", 1)[1]
    return ip_tag


def switch_kankun(device_query: str, state: str) -> None:
    ips, responses = read_devices_list()
    if not ips:
        print('Please try "kankun -l" first', file=sys.stderr)
        raise SystemExit(2)

    matches = find_matching_devices(device_query, ips, responses)
    if not matches:
        print("No matching device found. Update your list (-l) or check your spelling.", file=sys.stderr)
        raise SystemExit(2)

    for ip_tag, _resp in matches:
        ip = device_ip_from_tag(ip_tag)
        url = f"http://{ip}/cgi-bin/relay.cgi?{state}"
        try:
            text = http_get_text(url, timeout=DEFAULT_TIMEOUT_HTTP_SECS)
            print(text)
        except (URLError, HTTPError, socket.timeout, OSError):
            print("http Error, please update your list or check your spelling", file=sys.stderr)
            raise SystemExit(2)


def status_kankun(device_query: str) -> None:
    ips, responses = read_devices_list()
    if not ips:
        print('Please try "kankun -l" first', file=sys.stderr)
        raise SystemExit(2)

    matches = find_matching_devices(device_query, ips, responses)
    if not matches:
        print("No matching device found. Update your list (-l) or check your spelling.", file=sys.stderr)
        raise SystemExit(2)

    for ip_tag, _resp in matches:
        ip = device_ip_from_tag(ip_tag)
        url = f"http://{ip}/cgi-bin/relay.cgi?"
        try:
            text = http_get_text(url, timeout=DEFAULT_TIMEOUT_HTTP_SECS)
            print(text)
        except (URLError, HTTPError, socket.timeout, OSError):
            print("http Error, please update your list or check your spelling", file=sys.stderr)
            raise SystemExit(2)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Kankun automation (Python 3)")
    # Keep backward-compatible flags:
    # - old usage: -l list  (accepts optional value)
    parser.add_argument("-l", "--list", nargs="?", const="list", default=None,
                        help="List Kankun devices on the network (optionally: -l or -l list)")
    parser.add_argument("-s", "--switch", choices=["on", "off"], required=False,
                        help="Issue switch command: on or off")
    parser.add_argument("-d", "--device", required=False,
                        help="Substring to match device name returned by relay.cgi")
    parser.add_argument("--ifname", default=os.environ.get("KANKUN_IFNAME", "eth0"),
                        help="Network interface to scan (default: eth0 or $KANKUN_IFNAME)")

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if args.list is not None:
        try:
            rows = discover_kankun_devices(args.ifname)
        except Exception as e:
            print(f"Failed to scan devices: {e}", file=sys.stderr)
            return 2
        write_devices_list(rows)
        return 0

    if args.device is not None and args.switch is not None:
        switch_kankun(args.device, args.switch)
        return 0

    if args.device is not None:
        status_kankun(args.device)
        return 0

    # Nothing requested
    print("Nothing to do. Use -l to scan, or -d DEVICE [-s on|off].", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
