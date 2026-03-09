# REDIS_CONFIG.md — Configuração Upstash Redis

UPSTASH_REDIS_URL=https://winning-lionfish-12190.upstash.io
UPSTASH_REDIS_TOKEN=AS-eAAIncDFlZTdkODdhNWZhNDc0ZmIxYjNhZWNlMGQ0MjZhZDgzMHAxMTIxOTA

## Schema de keys do Squad VY

### Memória compartilhada
squad:memory:{agente}        → o que cada agente sabe
squad:context:atual          → contexto ativo do momento

### Fila de tarefas
squad:queue:tarefas          → lista de tarefas pendentes
squad:queue:prioridade       → tarefas urgentes

### Cache de respostas
squad:cache:{hash_prompt}    → resposta cacheada (evita repetir LLM call)
squad:cache:ttl              → 3600 segundos padrão

### Pub/Sub — canais de comunicação
squad:canal:geral            → NEXUS coordena
squad:canal:conteudo         → ECHO KIRA STORM DANTE PINE CLIP
squad:canal:vendas           → SCOUT HEIST ARIA LUNA LEAD
squad:canal:visual           → PIXEL CANVAS NANO VIBE
squad:canal:tech             → LUMEN BYTE FLOW PULSE
squad:canal:intel            → SAGE ORACLE RADAR TREND LENS
squad:canal:alertas          → PULSE monitora tudo

## Como conectar (quando tiver as credenciais)
Todo agente que precisar do Redis usa as variáveis acima.
Upstash funciona via HTTP — compatível com qualquer ambiente.
Free tier: 256MB + 500K comandos/mês.
