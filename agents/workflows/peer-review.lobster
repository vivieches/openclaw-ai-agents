# peer-review.lobster

workflow "peer-review" {
  description "Protocolo de Peer Review do Squad VY — Garantia de Qualidade em 4 Fases"
  
  trigger on: "task_completion", agent: "*"
  
  step "fase-1-execucao" {
    agent "{{trigger.agent}}"
    action "Executar a tarefa delegada pela Frieren ou Vivi"
  }
  
  step "fase-2-critica-tecnica" {
    agent "STORM"
    input "{{step1.output}}"
    action "Redteam: encontrar falhas, inconsistências e 'enrolação' no output"
  }
  
  step "fase-3-refino-copy" {
    agent "ECHO"
    input "{{step2.output}}"
    action "Refinar o tom de voz para o padrão Vivi (Informal, Direto, Sem Filler)"
  }
  
  step "fase-4-veredicto-final" {
    agent "MIRROR"
    input "{{step3.output}}"
    action "Garantir que os objetivos de negócio da Vivi Developer foram atingidos. Aprovar ou Rejeitar."
  }
}
