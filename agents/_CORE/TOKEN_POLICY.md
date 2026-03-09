# TOKEN_POLICY.md — Regime Custo Zero (Squad VY)

## 1. Model Tiering (OpenRouter Free)
- **Primary Tier**: `google/gemini-2.0-flash-exp:free` (Melhor raciocínio, 1M context, gratuito).
- **Secondary Tier**: `meta-llama/llama-3.3-70b-instruct:free` (Coding, instrução estruturada, rápido).
- **Audit Tier**: `mistralai/mistral-small-3.1:free` (Refactor, auditoria, economia extrema).

## 2. Protocolo de Resposta (Anti-Haiku-Filler)
- **Direct Output**: Proibido filler words ("Com certeza", "Vou fazer"). Responda no formato "Ação → Resultado".
- **Threshold**: Compactação de sessão (Compaction) em `40.000` tokens padrão.
- **Short Context**: Memória de curto prazo no Redis (`squad:session:{id}:context`) não deve exceder 5.000 tokens.

## 3. Caching e Retenção
- **Frieren**: `cacheRetention: long` (Mantém o contexto de mentoria quente).
- **Geral**: `cacheRetention: short` (Limpa cache após 5 minutos de inatividade).

## 4. Escala de Erro
- Se `Gemini Free` der 429 (Rate Limit), use `Llama 3.3 Free`. 
- Se o OpenRouter cair → @NEXUS pausar squad até normalização.
