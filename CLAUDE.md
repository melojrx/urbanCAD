# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos Comuns de Desenvolvimento

### Executar a aplicação
```bash
# Desenvolvimento
python app.py

# Produção (usando gunicorn)
gunicorn --bind 0.0.0.0:8009 --workers 1 --worker-class eventlet wsgi:app
```

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Configuração do banco de dados
- Banco de dados: PostgreSQL com extensão PostGIS
- String de conexão configurada em `app/database.py`
- Script de inicialização: `Script.sql`

### Docker
```bash
# Construir imagem
docker build -t urbancad .

# Executar container
docker run -p 8009:8009 urbancad
```

## Arquitetura do Sistema

### Visão Geral
O UrbanCAD é um sistema de Despacho Assistido por Computador (CAD) desenvolvido em Flask para gerenciamento de ocorrências urbanas. Utiliza arquitetura MVC com comunicação em tempo real via WebSocket.

### Estrutura Principal

#### Backend (Flask)
- **Blueprints**: Módulos organizados em `app/rotas/` para cada entidade do sistema
- **DAO (Data Access Objects)**: Camada de acesso a dados em `app/DAO/`
- **Models**: Modelos SQLAlchemy em `app/models/` com schema `cad`
- **Controllers**: Lógica de negócio em `app/controller/`
- **WebSocket**: Comunicação em tempo real usando Flask-SocketIO

#### Frontend
- **Templates**: Jinja2 em `app/templates/`
- **Assets**: CSS/JS/imagens em `app/static/`
- **Mapas**: Integração com Leaflet/OpenStreetMap
- **Gráficos**: Chart.js para visualizações no dashboard

### Entidades Principais
- **Ocorrência**: Incidentes reportados no sistema
- **Despacho**: Atribuição de recursos para ocorrências
- **Viatura**: Veículos de patrulha
- **Agente**: Usuários operacionais do sistema
- **Composição**: Grupos de viaturas/agentes
- **GPS**: Rastreamento de localização em tempo real

### Fluxo de Dados
1. **Registro de Ocorrência** → Criação no banco com coordenadas geográficas
2. **Despacho** → Atribuição de viaturas/agentes disponíveis
3. **Acompanhamento** → Atualizações em tempo real via WebSocket
4. **Histórico** → Registros de todas as mudanças de status

### Autenticação e Segurança
- Flask-Login para gerenciamento de sessões
- Grupos de despacho para controle de acesso
- CORS configurado para permitir comunicação WebSocket

### Características Especiais
- **Geoespacial**: Utiliza GeoAlchemy2 e PostGIS para operações espaciais
- **Tempo Real**: WebSocket para notificações e atualizações de status
- **Relatórios**: Geração de PDFs com FPDF
- **Dashboard**: Visualização de métricas e estatísticas operacionais

### Padrões de Desenvolvimento
- Models seguem padrão de nomenclatura: `tb_[entidade]_[abreviação]`
- Colunas com prefixo indicando tipo: `id_`, `txt_`, `dat_`, `num_`
- Relacionamentos definidos explicitamente nos models
- Blueprints registrados em `app/__init__.py`