# 📲🔳 🏷️SCAPS - Sistema de Chamadas Automáticas para o SUAP

## 📋 Sobre o projeto:
Trata-se de um projeto acadêmico referente a disciplina de Seminário de Orientação ao Projeto Integrador.
O projeto consiste no desenvolvimento de uma solução para automação da presença em sala de aula.
O sistema utiliaza-se de teconologia QR para realizar a autenticação dos discentes, com o número de matricula e senha institucional.
A solução está atrelada ao Sistema Unificado de Admiministração Pública (SUAP). 

## ✅ Objetivos:
#### Otimizar o tempo destinado a frequência em sala de aula 
#### Redução de falhas humanas 
#### Foco em organização, confiabilidade e integração com sistemas institucionais

## 🤖 Teconologias e ferramentas:
### Backend e Dashboard:
####  🐍 Python
#### 📊 Django

### Banco de Dados
🛢 PostgreSQL

### Infraestrutura
#### 🐳 Docker
#### 🏗️ Docker Compose

### Rede e Acesso
🌐 Nginx (proxy reverso)




🛠️ Composição:




🛠️ Estrutura do Projeto
Este projeto é dividido em múltiplos serviços:

Frontend (Django) — responsável: Ian Guilherme
Banco de Dados — responsável: Tamires Angélica
Docker Compose — responsável: Jordan Julio
Nginx Proxy — responsável: Pedro Jordan
🚀 Como Executar o Proxy (Nginx)
O proxy Nginx roteia requisições para os serviços frontend e backend e serve arquivos estáticos.

Pré-requisitos
Docker e Docker Compose instalados
Serviços e devem estar rodando na mesma rede Docker (frontendbackendqr_network)
###Commands para ligar os contêineres

*Insira o diretório de Códigos: cd .\Codigos\

*Então execute os comandos abaixo:

Compilação Docker Compose Docker Compose -D

NOTA: Abra o Docker Desktop antes de iniciar o processo.

Acesse o navegador: Django: http://localhost:8000

http://localhost:8001/gera_qr


