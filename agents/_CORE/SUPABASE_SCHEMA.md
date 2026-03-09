# SUPABASE_SCHEMA.md — Squad VY

## Status: PENDENTE — executar após criar projeto no Supabase

## Como criar o projeto
1. Acessa supabase.com
2. New Project → nome: squad-vy → região: West EU (Frankfurt)
3. Anota: Project URL + anon key + service_role key
4. Abre o SQL Editor e executa os blocos abaixo em ordem

---

## BLOCO 1 — Extensões necessárias
```sql
create extension if not exists "uuid-ossp";
create extension if not exists vector;
```

---

## BLOCO 2 — Tabela: squad_memory
Memória compartilhada de todos os agentes.
```sql
create table squad_memory (
  id uuid default uuid_generate_v4() primary key,
  agent_name text not null,
  memory_type text not null check (memory_type in ('fato','decisao','licao','contexto','lead','projeto')),
  content text not null,
  tags text[] default '{}',
  confidence text default 'MEDIA' check (confidence in ('ALTA','MEDIA','BAIXA')),
  embedding vector(1536),
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  expires_at timestamptz default null
);

create index on squad_memory using ivfflat (embedding vector_cosine_ops);
create index on squad_memory (agent_name);
create index on squad_memory (memory_type);
create index on squad_memory (created_at desc);
```

---

## BLOCO 3 — Tabela: tasks
Todas as tarefas do squad — o STATE.yaml vira banco aqui.
```sql
create table tasks (
  id uuid default uuid_generate_v4() primary key,
  title text not null,
  description text,
  owner_agent text not null,
  requested_by text,
  status text default 'pendente' check (status in ('pendente','em_progresso','bloqueado','concluido','cancelado')),
  priority text default 'media' check (priority in ('urgente','alta','media','baixa')),
  project text,
  depends_on uuid[] default '{}',
  output_path text,
  due_date timestamptz,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create index on tasks (owner_agent);
create index on tasks (status);
create index on tasks (priority);
create index on tasks (project);
```

---

## BLOCO 4 — Tabela: decisions
Registro de todas as decisões importantes do squad.
```sql
create table decisions (
  id uuid default uuid_generate_v4() primary key,
  title text not null,
  context text not null,
  decision_made text not null,
  decided_by text not null,
  alternatives_considered text[],
  mirror_verdict text check (mirror_verdict in ('APROVADO','APROVADO_COM_RESSALVAS','BLOQUEADO')),
  mirror_notes text,
  debate_rounds int default 0,
  project text,
  created_at timestamptz default now()
);

create index on decisions (decided_by);
create index on decisions (project);
create index on decisions (created_at desc);
```

---

## BLOCO 5 — Tabela: squad_messages
Canal de comunicação assíncrona entre agentes.
```sql
create table squad_messages (
  id uuid default uuid_generate_v4() primary key,
  from_agent text not null,
  to_agent text not null,
  message_type text not null check (message_type in ('tarefa','handoff','alerta','debate','aprovacao','resultado')),
  subject text,
  content text not null,
  payload jsonb default '{}',
  status text default 'nao_lido' check (status in ('nao_lido','lido','processado','arquivado')),
  priority text default 'normal' check (priority in ('urgente','alta','normal','baixa')),
  created_at timestamptz default now(),
  read_at timestamptz
);

create index on squad_messages (to_agent, status);
create index on squad_messages (from_agent);
create index on squad_messages (message_type);
create index on squad_messages (created_at desc);
```

---

## BLOCO 6 — Tabela: leads
Pipeline de leads do SCOUT, ARIA, HEIST e LUNA.
```sql
create table leads (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  contact text,
  platform text,
  source_agent text not null,
  pain_identified text,
  budget_range text,
  urgency text check (urgency in ('alta','media','baixa','desconhecida')),
  score int check (score between 1 and 10),
  status text default 'novo' check (status in ('novo','qualificado','proposta_enviada','negociando','fechado','perdido','frio')),
  owner_agent text,
  notes text,
  tags text[] default '{}',
  is_noiva boolean default false,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  last_contact_at timestamptz
);

create index on leads (status);
create index on leads (source_agent);
create index on leads (owner_agent);
create index on leads (score desc);
create index on leads (is_noiva);
```

---

## BLOCO 7 — Tabela: content_calendar
Calendário de conteúdo gerenciado pelo KIRA, DANTE, PINE, CLIP.
```sql
create table content_calendar (
  id uuid default uuid_generate_v4() primary key,
  title text not null,
  content_type text not null check (content_type in ('post','reel','story','pin','email','newsletter','thread','artigo','video','short')),
  platform text not null check (platform in ('instagram','linkedin','pinterest','youtube','tiktok','email','twitter')),
  owner_agent text not null,
  status text default 'ideia' check (status in ('ideia','em_producao','revisao','aprovado','agendado','publicado','cancelado')),
  hook text,
  body text,
  cta text,
  visual_brief text,
  scheduled_at timestamptz,
  published_at timestamptz,
  performance jsonb default '{}',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create index on content_calendar (platform, status);
create index on content_calendar (owner_agent);
create index on content_calendar (scheduled_at);
create index on content_calendar (status);
```

---

## BLOCO 8 — Tabela: agent_metrics
Performance e saúde de cada agente — monitorado pelo PULSE e LENS.
```sql
create table agent_metrics (
  id uuid default uuid_generate_v4() primary key,
  agent_name text not null,
  metric_date date default current_date,
  tasks_completed int default 0,
  tasks_failed int default 0,
  debates_won int default 0,
  debates_lost int default 0,
  average_debate_rounds numeric(3,1) default 0,
  tokens_used int default 0,
  errors jsonb default '[]',
  notes text,
  created_at timestamptz default now()
);

create index on agent_metrics (agent_name);
create index on agent_metrics (metric_date desc);
```

---

## BLOCO 9 — Tabela: opportunities
Oportunidades de renda monitoradas pelo CASH e YIELD.
```sql
create table opportunities (
  id uuid default uuid_generate_v4() primary key,
  title text not null,
  opportunity_type text not null check (opportunity_type in ('freelance','afiliado','produto_digital','edital','parceria','saas','conteudo_pago')),
  platform text,
  url text,
  estimated_revenue text,
  effort text check (effort in ('baixo','medio','alto')),
  time_to_money text check (time_to_money in ('hoje','esta_semana','este_mes','longo_prazo')),
  status text default 'nova' check (status in ('nova','avaliando','em_andamento','concluida','descartada')),
  found_by text default 'CASH',
  expires_at timestamptz,
  created_at timestamptz default now()
);

create index on opportunities (status);
create index on opportunities (time_to_money);
create index on opportunities (opportunity_type);
create index on opportunities (created_at desc);
```

---

## BLOCO 10 — Tabela: study_progress
Progresso de estudos da Vivi gerenciado pelo MENTOR.
```sql
create table study_progress (
  id uuid default uuid_generate_v4() primary key,
  subject text not null check (subject in ('biologia','espanhol','historia','matematica')),
  topic text not null,
  subtopic text,
  status text default 'nao_iniciado' check (status in ('nao_iniciado','em_progresso','revisao','dominado')),
  difficulty text check (difficulty in ('facil','medio','dificil')),
  stuck_points text[],
  flashcards_created int default 0,
  last_reviewed_at timestamptz,
  exam_questions_tried int default 0,
  exam_questions_correct int default 0,
  notes text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create index on study_progress (subject, status);
create index on study_progress (status);
```

---

## BLOCO 11 — Realtime (ativar após criar tabelas)
Ativa notificações em tempo real para as tabelas principais.
No Supabase Dashboard → Database → Replication → ativa para:
- squad_messages
- tasks
- leads
- opportunities

---

## BLOCO 12 — Variáveis de ambiente
Após criar o projeto, adicionar no arquivo .env do workspace:
```
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
```

E atualizar o STATE.yaml:
```yaml
supabase:
  status: "configurado"
  url: "[colar aqui]"
```
