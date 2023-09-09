import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an new mac, use --help for more info.")
    return options
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.run(["ifconfig ", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw ", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")

options = get_arguments() # 프로그램 실행 시 옵션으로 인터페이스 값과 새로운 맥 주소 값을 입력 받음.
current_mac = get_current_mac(options.interface) # 실행 된 메소드에서 디바이스가 가지고 있는 맥 주소를 추출함.
print("Current MAC = " + str(current_mac)) # 현재 맥 주소 출력.
change_mac(options.interface, options.new_mac) # 원하는 맥 주소로 기존 맥 주소를 변경
current_mac = get_current_mac(options.interface) # 실행 된 메소드에서 디바이스가 가지고 있는 맥 주소를 추출함.
if current_mac == options.new_mac: # 바꾸려는 맥 주소와 현재 맥 주소가 같은 지 확인함.
    print("[+] MAC address was successfully changed to " + current_mac) # 같다면 성공적으로 바뀌었음을 출력.
else:
    print("[-] MAC address did not get changed.") # 다르면 바뀌지 않았다고 출력.