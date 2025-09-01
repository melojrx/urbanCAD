# Guia de Instalação - UrbanCAD

## Problema: Docker não está instalado no WSL2

Você tem 3 opções para executar o UrbanCAD:

## Opção 1: Instalar Docker Desktop (Recomendado)

1. **Baixe e instale o Docker Desktop no Windows:**
   - https://www.docker.com/products/docker-desktop/

2. **Configure a integração com WSL2:**
   - Abra Docker Desktop
   - Vá em Settings → Resources → WSL Integration
   - Ative a integração com sua distribuição WSL2
   - Aplique e reinicie

3. **Teste a instalação:**
   ```bash
   docker --version
   docker-compose --version
   ```

4. **Execute o projeto:**
   ```bash
   docker-compose up -d --build
   ```

## Opção 2: Instalar Docker nativamente no WSL2

Execute o script de instalação que criei:

```bash
./install-docker-wsl2.sh
```

Ou siga as instruções manuais no script para instalar o Docker diretamente no WSL2.

## Opção 3: Executar localmente (sem Docker)

Para desenvolvimento rápido sem Docker:

```bash
# Execute o script auxiliar
./run-local.sh
```

### Requisitos para execução local:
1. **PostgreSQL com PostGIS:**
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib postgis
   ```

2. **Python 3.8+:**
   ```bash
   python3 --version
   ```

3. **Configure o banco:**
   ```bash
   sudo service postgresql start
   sudo -u postgres createdb urbancad
   sudo -u postgres psql -d urbancad -f Script.sql
   ```

4. **Execute manualmente:**
   ```bash
   # Criar ambiente virtual
   python3 -m venv venv
   source venv/bin/activate

   # Instalar dependências
   pip install -r requirements.txt

   # Executar
   python app.py
   ```

## Próximos Passos

Após escolher e configurar uma das opções:

1. **Com Docker:** Acesse http://localhost
2. **Sem Docker:** Acesse http://localhost:5000

## Troubleshooting

### WSL2 não está ativado
```powershell
# No PowerShell como administrador
wsl --install
wsl --set-default-version 2
```

### PostgreSQL não inicia no WSL2
```bash
sudo service postgresql restart
sudo service postgresql status
```

### Porta já em uso
```bash
# Verificar processos nas portas
sudo lsof -i :5432  # PostgreSQL
sudo lsof -i :5000  # Flask
sudo lsof -i :80    # NGINX
```