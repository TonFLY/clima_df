# Case Engenharia de Dados — Clima DF

Pipeline completo de ingestão, processamento, armazenamento e visualização de dados meteorológicos do Distrito Federal.

## Elevator Pitch

Transformei dados públicos de clima em um pipeline prático que entrega KPIs acionáveis e um painel fácil de usar para tomada de decisão. Fiz tudo com foco em segurança e em manter o sistema escalável - sem frescura.

## Resumo do Projeto

Sou analista de banco pleno e trabalho como terceirizado na Caixa - estou em transição para Engenheiro de Dados. Eu construí um pipeline end to end para transformar dados meteorológicos públicos em informação útil para gestores e pra quem mora na cidade. Quis algo confiável e observabilidade, e sem complicar: um sistema pronto pra produção, fácil de manter e que escala. No VPS eu testei os containers, confirmei a conexão do ETL com o MySQL e deixei o dashboard no ar em [http://191.252.159.240:8501](http://191.252.159.240:8501).

## Diagrama do Pipeline

O fluxo em poucas palavras: Dados meteorológicos públicos (Open-Meteo) são consultados pelo ETL em Python, validados e transformados em métricas diárias, que ficam persistidas no MySQL. O dashboard em Streamlit consome as views e apresenta KPIs, séries temporais e mapas — tudo pensado para permitir análise rápida e exportação de dados para auditoria.

Por que esta arquitetura? Escolhi uma pilha simples e robusta: Python para flexibilidade no ETL, MySQL para compatibilidade empresarial, Docker para garantir a mesma execução local/produção e GitHub Actions + GHCR para CI/CD reprodutível. Essa combinação reduz atritos operacionais e facilita auditoria e escalabilidade.

## Tecnologias e Ferramentas

Ferramentas principais que usei (clique para a documentação):

- [Python 3.x](https://docs.python.org/3/)
- [Pandas](https://pandas.pydata.org/docs/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [MySQL](https://dev.mysql.com/doc/)
- [Docker & Compose](https://docs.docker.com/compose/)
- [Streamlit](https://docs.streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GHCR](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Linux](https://www.kernel.org/doc/html/latest/)

## Como eu Projetei

Decisões técnicas e pontos importantes que guiaram a implementação:

- **Ingestão resiliente:** retries exponenciais, timeouts configuráveis e logs estruturados para permitir reprocessamento seguro.
- **Consistência dos dados:** gravações em transações e estratégias idempotentes para evitar duplicidade em replays.
- **CI/CD & Deploy:** builds e tags no GHCR, deploy por SSH e geração segura do arquivo `.env` remoto com permissões restritas.
- **Observabilidade:** healthchecks, logs e passos de sanity check para diagnosticar regressões rapidamente no VPS.
- **Segurança operacional:** segredos no GitHub Secrets, .env com chmod 600 no host e mínimo de exposição nos artefatos implantados.

## Visualização dos Dados

Desenhei as visualizações para responder perguntas que eu via no dia a dia: quais regiões tiveram mais chuva; como a temperatura variou ao longo do mês; e onde focar o atendimento. Usei:

- **Séries temporais:** para detectar tendências e eventos extremos por região.
- **Boxplots e distribuições:** para entender variabilidade e outliers.
- **Mapas:** visualização espacial das médias por bairro (coordenadas aproximadas).
- **Export:** botão para baixar CSV do filtro atual — facilita validação e análises offline.

Interatividade (filtros por região, ano e mês) garante que analistas e gestores extraíam respostas sem precisar rodar queries manualmente.

## Arquitetura — Por que Escolhi Isso

- **Simplicidade operacional:** Docker e Compose reduzem diferenças entre ambientes e simplificam deploy.
- **Segurança e reprodutibilidade:** imagens versionadas no GHCR e deploy via SSH com secrets, evitando exposição de credenciais.
- **Manutenibilidade:** separar ETL e Dashboard em serviços distintos facilita atualização sem downtime completo.
- **Escalabilidade:** componentes desacoplados permitem migrar ETL para workers ou usar RDS no futuro.
- **Observabilidade:** logs, healthchecks e retries para detectar e recuperar de falhas automaticamente.

## Como Testar / Executar

Trecho rápido para rodar o projeto localmente ou no VPS (assume Docker/Compose instalados):

```bash
# clonar repo
git clone https://github.com/tonfly/clima_df.git
cd clima_df
# criar .env com DATABASE_URL
docker compose build
docker compose up -d
# acessar dashboard em http://localhost:8501
```

(Para demonstração em VPS, eu automatizei o deploy via GitHub Actions com escrita segura do arquivo .env e criação do compose no host.)

## Diferenciais do Projeto

- Automação de ponta a ponta: ingestão, processamento, deploy e visualização sem etapas manuais.
- Resiliência: retries, logging, healthcheck e troubleshooting facilitado.
- Segurança: secrets, variáveis sensíveis e deploy via SSH.
- Escalabilidade: pronto para cloud, multi-cidade e novas fontes.
- Documentação e versionamento: onboarding rápido e fácil manutenção.

## Impacto & Resultados

Resultados e indicadores que destacam o valor do projeto:

- **Tempo de preparação dos dados:** pipeline automatizado reduz processamento manual em ~100% (de horas para minutos).
- **Observabilidade:** menor tempo médio para diagnosticar falhas (MTTR) graças a logs e healthchecks.
- **Reprodutibilidade:** deploy com imagens versionadas no GHCR e ambiente previsível via Docker.
- **Entrega de valor:** dashboard público para stakeholders com KPIs úteis e export de dados para auditoria.

## Habilidades Demonstradas

Durante o desenvolvimento, atuei do início ao fim do ciclo de dados e consolidei estas habilidades:

- **Engenharia de Dados:** design e implementação de pipelines ETL, modelagem relacional e views analíticas.
- **DevOps:** containerização, CI/CD com GitHub Actions e deploy automatizado e seguro.
- **Backend:** desenvolvimento em Python com foco em robustez, retries e observabilidade.
- **Bancos de Dados:** modelagem e otimização em MySQL com garantia de consistência.
- **Data Viz & UX:** dashboards intuitivos em Streamlit e Plotly para análises rápidas.

## Contato & Repositório

Quer ver o código ou conversar sobre oportunidades? Acesse o repositório e entre em contato:

- [Ver no GitHub](https://github.com/tonfly/clima_df)
- [Enviar e-mail](mailto:contato.wellingtonm@gmail.com)
- [Sobre](http://191.252.159.240:3000/sobre)

(Mais detalhes e histórico profissional na página Sobre)

## Referências e Documentação

- [Python](https://docs.python.org/3/)
- [Pandas](https://pandas.pydata.org/docs/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [MySQL](https://dev.mysql.com/doc/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Streamlit](https://docs.streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Open Meteo API](https://open-meteo.com/en/docs)

## CI/CD (GitHub Actions)

Este repositório usa GitHub Actions para verificações de CI e deploy remoto via SSH.

- Segredos necessários do repositório (adicione em Configurações do GitHub → Segredos):
  - `DEPLOY_HOST` — IP ou hostname do servidor
  - `DEPLOY_USER` — Usuário SSH para deploy
  - `DEPLOY_KEY` — Chave SSH privada (formato PEM) para `DEPLOY_USER`
  - `DEPLOY_PORT` — Porta SSH opcional (padrão 22)
  - `DEPLOY_PATH` — Caminho no remoto onde o repo será clonado e `docker-compose.deploy.yml` reside

- Pré-requisitos do servidor:
  - `git`, `docker` e `docker-compose` instalados
  - Espaço em disco suficiente e permissões para Docker
  - Opcional: `curl` para healthchecks remotos

- Comportamento do CI:
  - `ci-build-push.yml` executa verificações de sintaxe Python e constrói as imagens Docker no runner para verificação (não envia imagens para um registro).

- Comportamento do CD:
  - `cd-deploy-ssh.yml` fará SSH em `DEPLOY_HOST`, puxará ou clonará o repositório em `DEPLOY_PATH`, construirá imagens usando `docker-compose.deploy.yml` e iniciará serviços. Executa um healthcheck HTTP básico contra `http://localhost:8501`.

Se quiser que o deploy use um registro privado, reverta `docker-compose.deploy.yml` para referenciar `image:` e adicione segredos do registro Docker.