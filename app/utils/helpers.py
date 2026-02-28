import secrets
import string
from user_agents import parse


# this function generates autocode of 6 alpha_numerics
def generate_short_code():
    alphanumerics = (
        string.ascii_letters + string.digits
    )  # concatenation of all uppercase lowecase and digits
    code = "".join(
        secrets.choice(alphanumerics) for _ in range(6)
    )  # choose 6 symbols from alphanumeric variable
    return code


# ip_masking masks the given ip address as i.e; 192.168.XXX
def ip_masking(ip):
    octals = ip.split(".")
    ip_masked = octals
    ip_masked[-1] = "XXX"  # converting last octal of IP address into ""XXX"""
    ip_masked = ".".join(ip_masked)
    return ip_masked


def user_agent_info(user_agent_string):
    user_agent = parse(user_agent_string)
    browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
    os = f"{user_agent.os.family} {user_agent.os.version_string}"
    return browser, os
