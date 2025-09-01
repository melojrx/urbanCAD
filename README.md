# 🚑 UrbanCAD

<div align="center">

**Sistema de Atendimento e Despacho**  
*Computer-Aided Dispatch System for Urban Emergency Management*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.1.2-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)

[📖 Documentação](#-documentação) • [🚀 Início Rápido](#-início-rápido) • [🏗️ Arquitetura](#-arquitetura) • [🔧 Configuração](#-configuração) • [🤝 Contribuição](#-contribuição)

</div>

---

## 📊 Visão Geral

O **UrbanCAD** é um sistema completo de gerenciamento de ocorrências urbanas desenvolvido para atender às necessidades de organizações públicas e privadas que lidam com emergências e serviços urbanos. O sistema oferece funcionalidades robustas para cadastro, despacho e acompanhamento de ocorrências em tempo real.

### 🎯 Principais Funcionalidades

- **📋 Gestão de Ocorrências**: Cadastro, edição e acompanhamento completo
- **🚗 Controle de Viaturas**: Gerenciamento de frota e localização em tempo real
- **👮 Gestão de Agentes**: Controle de equipes e escalas
- **📡 Despacho Inteligente**: Sistema automático de distribuição de chamados
- **📊 Dashboard Analítico**: Relatórios e métricas em tempo real
- **🗺️ Integração Geográfica**: Mapas e coordenadas com PostGIS
- **🔐 Controle de Acesso**: Sistema de roles e permissões
- **📱 Interface Responsiva**: Acesso via desktop, tablet e mobile

### 🎖️ Níveis de Acesso

| Role | Descrição | Permissões |
|------|-----------|------------|
| **CAD_ADMIN** | Administrador do Sistema | Acesso completo, configurações, relatórios |
| **CAD_DESPACHO** | Operador de Despacho | Gerenciar ocorrências, despachar viaturas |
| **CAD_AGENTE** | Agente de Campo | Visualizar e atualizar ocorrências atribuídas |

---

## 🏗️ Arquitetura

### 💻 Stack Tecnológico

#### Backend
- **Framework**: Flask 2.1.2 (Python)
- **ORM**: SQLAlchemy + Flask-SQLAlchemy
- **Autenticação**: Flask-Login com hash bcrypt
- **Validação**: WTForms
- **Migrações**: Flask-Migrate
- **WebSockets**: Flask-SocketIO para tempo real

#### Frontend
- **Template Engine**: Jinja2
- **CSS Framework**: Bootstrap 5.3.2
- **Ícones**: Font Awesome 6.3.0 + Bootstrap Icons
- **JavaScript**: Vanilla JS + Socket.IO client
- **Mapas**: Leaflet.js para visualização geográfica

#### Banco de Dados
- **SGBD**: PostgreSQL 13
- **Extensões**: PostGIS 3.1 para dados geoespaciais
- **Backup**: Volume persistente com Docker

#### Infraestrutura
- **Containerização**: Docker + Docker Compose
- **Web Server**: NGINX como proxy reverso
- **App Server**: Gunicorn com workers gevent
- **Rede**: Isolamento com redes Docker customizadas

### � Diagrama de Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   NGINX Proxy   │────│  Flask App      │────│  PostgreSQL     │
│   (Port 80/443) │    │  (Gunicorn)     │    │  + PostGIS      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
    Load Balancer          WebSocket Server         Persistent Data
    Static Files           Real-time Updates        Geographic Data
```

---

## 🚀 Início Rápido

### 📋 Pré-requisitos

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Git** 2.30+
- **Navegador** moderno (Chrome, Firefox, Edge, Safari)

### ⚡ Instalação Express

```bash
# 1. Clone o repositório
git clone https://github.com/melojrx/urbanCAD.git
cd urbanCAD

# 2. Execute o sistema
docker-compose up -d --build

# 3. Aguarde a inicialização (30-60 segundos)
docker-compose logs -f web

# 4. Acesse o sistema
open http://localhost
```

### 🔑 Credenciais de Acesso

| Usuário | Email | Senha | Função |
|---------|-------|-------|---------|
| **Admin** | admin@admin.com | `123456` | Administrador Geral |
| **Despacho** | despacho@despacho.com | `123456` | Operador de Despacho |
| **Agente** | agente@agente.com | `123456` | Agente de Campo |

> ⚠️ **Importante**: Altere as senhas padrão em ambiente de produção

---

## 🗃️ Estrutura do Projeto

```
urbanCAD/
├── 📁 app/                          # Aplicação principal
│   ├── 📄 __init__.py              # Configuração Flask
│   ├── 📄 database.py              # Configuração SQLAlchemy
│   ├── 📁 controller/              # Lógica de negócio
│   │   ├── 📄 loginController.py   # Autenticação
│   │   ├── 📄 ocorrenciaController.py
│   │   ├── 📄 despachoController.py
│   │   └── 📄 ...
│   ├── 📁 models/                  # Modelos de dados
│   │   ├── 📄 userModel.py         # Usuários
│   │   ├── 📄 ocorrenciaModel.py   # Ocorrências
│   │   ├── 📄 viaturaModel.py      # Viaturas
│   │   └── 📄 ...
│   ├── 📁 forms/                   # Formulários WTF
│   ├── 📁 templates/               # Templates HTML
│   ├── 📁 static/                  # Assets estáticos
│   │   ├── 📁 css/                 # Estilos personalizados
│   │   ├── 📁 js/                  # Scripts JavaScript
│   │   └── 📄 favicon.svg          # Ícone da aplicação
│   ├── 📁 rotas/                   # Definição de rotas
│   └── 📁 DAO/                     # Data Access Objects
├── 📄 docker-compose.yml           # Orquestração de serviços
├── 📄 Dockerfile                   # Build da aplicação
├── 📄 Script.sql                   # Schema e dados iniciais
├── 📄 requirements.txt             # Dependências Python
├── 📄 .env.example                 # Variáveis de ambiente
├── 📄 nginx.conf                   # Configuração NGINX
└── 📄 README.md                    # Esta documentação
```

---

## 🔧 Configuração

### 🌍 Variáveis de Ambiente

Copie o arquivo de exemplo e configure:

```bash
cp .env.example .env
```

```env
# Banco de Dados
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_segura
POSTGRES_DB=urbancad
POSTGRES_PORT=5544

# Aplicação
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=False

# Recursos Opcionais
ENABLE_ANALYTICS=true
MAP_API_KEY=sua_chave_do_mapa
```

### 🐳 Docker Compose

O sistema é totalmente containerizado:

```yaml
services:
  postgres:    # Banco de dados PostgreSQL + PostGIS
  web:         # Aplicação Flask com Gunicorn
  nginx:       # Proxy reverso e balanceador
```

### 🔐 Segurança

- **Autenticação**: Hash bcrypt para senhas
- **Sessões**: Flask-Login com cookies seguros  
- **CORS**: Configuração restritiva
- **Headers**: Segurança HTTP implementada
- **Rede**: Isolamento de containers

---

## 🛠️ Desenvolvimento

### 🔧 Comandos Úteis

```bash
# Ambiente de desenvolvimento
docker-compose -f docker-compose.dev.yml up -d

# Logs em tempo real
docker-compose logs -f web

# Acesso ao container
docker-compose exec web bash

# Backup do banco
docker-compose exec postgres pg_dump -U postgres urbancad > backup.sql

# Restaurar banco
docker-compose exec -T postgres psql -U postgres urbancad < backup.sql

# Rebuild completo
docker-compose down -v && docker-compose up -d --build
```

### 🗄️ Banco de Dados

#### Conexão Local
```
Host: localhost
Port: 5544
Database: urbancad
Username: postgres
Password: [definida no .env]
```

#### Estrutura Principal
- **usuario_usu**: Usuários do sistema
- **ocorrencia_oco**: Registro de ocorrências
- **despacho_des**: Despachos e atribuições
- **viatura_via**: Viaturas e equipamentos
- **agente_age**: Agentes e equipes

### 🧪 Testes

```bash
# Executar testes unitários
docker-compose exec web python -m pytest

# Testes com cobertura
docker-compose exec web python -m pytest --cov=app

# Testes de integração
docker-compose exec web python -m pytest tests/integration/
```

---

## 📚 Documentação

### 📖 Guias Disponíveis

- [🏃 Guia de Início Rápido](docs/quickstart.md)
- [🔧 Manual de Instalação](docs/installation.md)
- [👨‍💻 Guia do Desenvolvedor](docs/development.md)
- [🎛️ Manual do Usuário](docs/user-guide.md)
- [🔒 Guia de Segurança](docs/security.md)
- [📊 API Reference](docs/api.md)

### 🎯 Casos de Uso

1. **Recebimento de Chamada**: Operador registra nova ocorrência
2. **Despacho Automático**: Sistema atribui viatura mais próxima
3. **Acompanhamento**: Agente atualiza status em tempo real
4. **Resolução**: Fechamento e relatório da ocorrência
5. **Análise**: Dashboard com métricas e KPIs

---

## 🚀 Deployment

### 🌐 Produção

```bash
# Clone e configure
git clone https://github.com/melojrx/urbanCAD.git
cd urbanCAD

# Configure ambiente
cp .env.example .env
# [Edite o .env com configurações de produção]

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### ☁️ Cloud Deploy

Suporte para:
- **AWS**: ECS + RDS
- **Google Cloud**: Cloud Run + Cloud SQL
- **Azure**: Container Instances + PostgreSQL
- **DigitalOcean**: App Platform

### 📊 Monitoramento

- **Logs**: Centralizados via Docker
- **Métricas**: Health checks automáticos
- **Backup**: Scripts automatizados
- **SSL**: Certificados Let's Encrypt

---

## 🤝 Contribuição

### 🎯 Como Contribuir

1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie** uma branch para sua feature
4. **Develop** e teste suas mudanças
5. **Commit** com mensagens descritivas
6. **Push** para sua branch
7. **Abra** um Pull Request

### 📋 Padrões de Código

- **Python**: PEP 8
- **JavaScript**: ES6+
- **HTML/CSS**: Semântico e responsivo
- **Git**: Conventional Commits

### � Reportar Bugs

Use o [GitHub Issues](https://github.com/melojrx/urbanCAD/issues) com:
- Descrição clara do problema
- Passos para reproduzir
- Ambiente (OS, browser, versão)
- Screenshots se aplicável

---

## 📋 Roadmap

### 🎯 Próximas Versões

#### v2.0 - Q4 2025
- [ ] API REST completa
- [ ] App mobile (React Native)
- [ ] Integração com sistemas externos
- [ ] Notificações push

#### v2.1 - Q1 2026
- [ ] Machine Learning para otimização
- [ ] Relatórios avançados
- [ ] Multi-tenancy
- [ ] Backup automático

#### v3.0 - Q2 2026
- [ ] Microserviços
- [ ] Kubernetes
- [ ] Real-time analytics
- [ ] IoT Integration

---

## ⚖️ Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2024 Júnior Melo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 👨‍💻 Autor

**Júnior Melo**
- 🌐 GitHub: [@melojrx](https://github.com/melojrx)
- 📧 Email: [jrmeloafrf@gmail.com](mailto:jrmeloafrf@gmail.com)
- 💼 LinkedIn: [Júnior Melo](https://www.linkedin.com/in/j%C3%BAnior-melo-a4817127/)
- 🎯 Portfólio: [melojrx.github.io](https://melojrx.github.io/)

---

## 🙏 Agradecimentos

- Comunidade Flask pela excelente framework
- Equipe PostgreSQL pelo robusto SGBD
- Contribuidores do PostGIS
- Comunidade open source

---

<div align="center">

**[⬆ Voltar ao Topo](#-urbancad)**

---

*Desenvolvido com ❤️ para melhorar a gestão de emergências urbanas*

</div>

