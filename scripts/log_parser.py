from collections import Counter
import re

# Simulação de linhas de log de autenticação (ex: auth.log / vsftpd.log)
SAMPLE_LOGS = [
    "Nov 25 18:35:01 metasploitable vsftpd: FAIL LOGIN: Client 192.168.56.102 user=user",
    "Nov 25 18:35:01 metasploitable vsftpd: FAIL LOGIN: Client 192.168.56.102 user=admin",
    "Nov 25 18:35:02 metasploitable vsftpd: FAIL LOGIN: Client 192.168.56.102 user=root",
    "Nov 25 18:35:02 metasploitable vsftpd: FAIL LOGIN: Client 192.168.56.102 user=msfadmin",
    "Nov 25 18:35:03 metasploitable vsftpd: OK LOGIN: Client 192.168.56.102 user=msfadmin",
]

def analyze_logs(logs: list[str], threshold: int = 3) -> None:
    failed_ips = Counter()
    successful_logins = []

    for line in logs:
        ip_match = re.search(r"Client (\d+\.\d+\.\d+\.\d+)", line)
        user_match = re.search(r"user=(\w+)", line)
        ip = ip_match.group(1) if ip_match else "desconhecido"
        user = user_match.group(1) if user_match else "desconhecido"

        if "FAIL LOGIN" in line:
            failed_ips[ip] += 1
        elif "OK LOGIN" in line:
            successful_logins.append((ip, user))

    print("=== Relatório de Triagem de Autenticação ===")
    for ip, count in failed_ips.items():
        status = "ALERTA: Possível Brute Force" if count >= threshold else "Normal"
        print(f"[IP: {ip}] Falhas detectadas: {count} -> {status}")

    if successful_logins:
        print("\n=== Acessos Bem-Sucedidos Após Tentativas ===")
        for ip, user in successful_logins:
            print(f"[+] Login confirmado | IP: {ip} | Usuário: {user}")

if __name__ == "__main__":
    analyze_logs(SAMPLE_LOGS)
