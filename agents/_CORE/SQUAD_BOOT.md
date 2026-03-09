# SQUAD_BOOT.md — Como o squad inicializa

## O que acontece quando o sistema liga

### Passo 1 — PULSE acorda primeiro (04h)
- Verifica Redis: está respondendo?
- Verifica Supabase: conexão ok?
- Lê erros das últimas 24h nos logs
- Se crítico → alerta Vivi e para o boot
- Se ok → registra no Redis: SET squad:state:boot_status "ok"

### Passo 2 — VAULT carrega memória do squad
- Lê squad_memory do Supabase (últimas 72h)
- Carrega decisões recentes da tabela decisions
- Escreve contexto consolidado no Redis: squad:memory:shared:context
- Máximo 50 itens — prioriza por data e relevância

### Passo 3 — NEXUS lê o estado atual
- Lê STATE.yaml
- Lê squad:memory:shared:context do Redis
- Verifica tarefas com status em_progresso ou bloqueado
- Define prioridades do dia

### Passo 4 — Agentes de heartbeat acordam nos horários
Cada agente realiza o seguinte ao acordar:
1. **Verifica Working Memory (Redis)**: `squad:session:{agent_id}:context`.
2. **Consulta Semântica (mem0)**: Executa `memory.search(limit=3)` para fatos críticos.
3. **Ignora MEMORY.md**: Este arquivo deve ser consultado apenas se mem0 falhar ou sob demanda explícita.
4. **Lê Tarefas Pendentes**: Do Supabase (status != concluido).
5. **Checa Fila de Peer Review**: `squad:peer_review:{task_id}` via Redis.

### Passo 5 — Registro de presença
Todo agente ao acordar executa:
- SADD squad:state:agents_online [SEU_NOME]
- SET squad:state:last_heartbeat:[SEU_NOME] [timestamp] EX 86400

## Ordem de prioridade ao receber tarefa
1. Lê cache Redis — já foi feito antes?
2. Lê contexto do squad — tem informação relevante?
3. Executa a tarefa
4. Salva resultado no Supabase
5. Publica no canal Redis correspondente
6. Atualiza STATE.yaml

## Encerramento seguro (Backup de Consciência)
Antes de qualquer compactação de contexto:
1. Salva decisões do dia no Supabase tabela decisions
2. **Executa `@nexus sync-brain *snapshot`** (Garante sync com mem0 e Obsidian)
3. Atualiza squad_memory com aprendizados da sessão
4. Atualiza STATE.yaml com status atual de todas as tarefas
5. Publica em squad:canal:geral: "encerramento e sync concluídos"
6. Remove nome de squad:state:agents_online
