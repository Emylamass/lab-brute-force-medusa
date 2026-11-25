<div align="center">

# 🔐 Simulação de Ataques de Força Bruta e Análise Defensiva com Kali Linux e Medusa

![Status](https://img.shields.io/badge/Status-Concluído-2ea44f?style=for-the-badge)
![Ambiente](https://img.shields.io/badge/Lab-VirtualBox%20Host--Only-1f6feb?style=for-the-badge)
![Ferramentas](https://img.shields.io/badge/Tools-Kali%20Linux%20%7C%20Medusa%20%7C%20Nmap-238636?style=for-the-badge)
![Foco](https://img.shields.io/badge/Foco-AppSec%20%7C%20Blue%20Team%20%7C%20Forense-3fb950?style=for-the-badge)

*Projeto prático desenvolvido para o desafio da DIO: auditoria de credenciais em ambiente controlado, análise de rastros em logs e recomendações de hardening.*

</div>

---

## ⚠️ Aviso Legal e Ético

Todas as atividades documentadas neste repositório foram executadas **exclusivamente em ambiente virtualizado, isolado e controlado** (rede interna *Host-Only*), utilizando máquinas intencionalmente vulneráveis para fins educacionais. O objetivo deste estudo é compreender vetores de ataque baseados em credenciais fracas para fortalecer mecanismos de defesa, detecção e resposta a incidentes.

---

## 🎯 Objetivos do Projeto

- Configurar um laboratório isolado de testes de segurança utilizando **VirtualBox**, **Kali Linux** e **Metasploitable 2** (incluindo **DVWA**).
- Executar testes controlados de força bruta e *password spraying* com o **Medusa** nos serviços **FTP**, **HTTP (Formulário Web)** e **SMB**.
- Automatizar a geração de wordlists simples e a análise básica de evidências/logs de tentativas de autenticação.
- Identificar vulnerabilidades de autenticação e propor contramedidas práticas de mitigação e monitoramento.

---

## 🖥️ Arquitetura do Laboratório

As duas máquinas virtuais foram configuradas no **VirtualBox** utilizando o adaptador de rede **Host-Only**, garantindo comunicação apenas entre o host e as VMs, sem exposição à internet.

| Componente | Sistema / Serviço | Endereço IP | Função no Lab |
| :--- | :--- | :--- | :--- |
| **Atacante / Auditor** | Kali Linux | `192.168.56.102` | Reconhecimento, criação de wordlists e execução do Medusa |
| **Alvo Vulnerável** | Metasploitable 2 / DVWA | `192.168.56.101` | Hospedagem dos serviços FTP, HTTP (DVWA) e SMB |

### Verificação Inicial e Reconhecimento

Antes de iniciar os testes de autenticação, foi validada a conectividade e realizada a varredura de portas no alvo com o `nmap`:

```bash
ping -c 4 192.168.56.101
nmap -sV -p 21,80,139,445 192.168.56.101
