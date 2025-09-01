# Orquestração Docker para UrbanCAD

## Estrutura da Orquestração

A aplicação está configurada com Docker Compose utilizando 3 containers:

1. **PostgreSQL com PostGIS** - Banco de dados geoespacial
2. **Aplicação Flask** - Backend com WebSocket
3. **NGINX** - Proxy reverso e servidor de arquivos estáticos

## Como Usar

### 1. Configurar variáveis de ambiente

Copie o arquivo de exemplo e configure suas variáveis:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
- `POSTGRES_PASSWORD`: Senha segura para o banco
- `SECRET_KEY`: Chave secreta para a aplicação Flask
- Outras configurações conforme necessário

### 2. Construir e executar

```bash
# Construir e iniciar todos os serviços
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (cuidado: apaga dados do banco!)
docker-compose down -v
```

### 3. Acessar a aplicação

- **Aplicação Web**: http://localhost (porta 80)
- **PostgreSQL**: localhost:5432 (para conexões externas)

## Arquitetura

### Fluxo de Requisições

```
Cliente → NGINX (:80) → Flask App (:8009) → PostgreSQL (:5432)
           ↓
      Arquivos estáticos
      servidos diretamente
```

### Recursos Configurados

1. **NGINX**:
   - Proxy reverso para aplicação Flask
   - Serve arquivos estáticos diretamente
   - Suporte completo para WebSocket
   - Cache de arquivos estáticos (30 dias)

2. **PostgreSQL**:
   - Extensão PostGIS habilitada
   - Script SQL executado automaticamente na inicialização
   - Volume persistente para dados
   - Health check configurado

3. **Flask App**:
   - Gunicorn com eventlet para WebSocket
   - Variáveis de ambiente para configuração
   - Restart automático em caso de falha

## Migrações (Flask-Migrate)

O projeto inclui Flask-Migrate para versionar mudanças de modelos.

Gerar estrutura inicial de migrações (primeira vez):
```bash
docker-compose exec web flask db init
docker-compose exec web flask db migrate -m "estrutura inicial"
docker-compose exec web flask db upgrade
```

Após alterar modelos:
```bash
docker-compose exec web flask db migrate -m "<descricao>"
docker-compose exec web flask db upgrade
```

## Usuários Seed

O `Script.sql` cria dois usuários básicos (somente nome/email/cpf):

- admin@urbancad.local
- agente@urbancad.local

Se precisar recriar (reinicializar base):
```bash
docker-compose down -v
docker-compose up -d --build
```

## Desenvolvimento

Para desenvolvimento local com hot-reload:

```bash
# Criar override para desenvolvimento
cat > docker-compose.override.yml << EOF
version: '3.8'

services:
  web:
    command: python app.py
    volumes:
      - ./:/app
    environment:
      FLASK_ENV: development
      FLASK_DEBUG: 1
EOF

# Executar em modo desenvolvimento
docker-compose up
```

## Troubleshooting

### Erro de conexão com banco de dados
- Verifique se o container do PostgreSQL está saudável: `docker-compose ps`
- Confirme as credenciais no arquivo `.env`

### WebSocket não funciona
- Certifique-se de que o NGINX está configurado corretamente
- Verifique os logs: `docker-compose logs nginx web`

### Aplicação não inicia
- Verifique dependências: `docker-compose logs web`
- Confirme que o banco foi inicializado: `docker-compose logs postgres`