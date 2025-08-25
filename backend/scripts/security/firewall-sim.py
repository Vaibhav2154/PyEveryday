import random
def generate_ip():
  return f"192.168.1.{random.randint(0,20)}"
def check_firewall_action(ip,rules):
  for ip_rule,action in rules.items():
    if ip == ip_rule:
      return action
  return "ALLOW!!"
def main():
  firewall_rules={
      "192.168.1.1":"Block",
      "192.168.1.15":"Block",
      "192.168.1.2":"Block",
      "192.168.1.5":"Block",
      "192.168.1.10":"Block",
      "192.168.1.7":"Block",
}
  for i in range(12):
    ip_adress=generate_ip()
    act=check_firewall_action(ip_adress,firewall_rules)
    print(f"IP:{ip_adress},Action:{act}")
if __name__ == "__main__":
  main()
