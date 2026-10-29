# Fontes oficiais e contrato

Integração própria baseada na habilidade oficial `openrouter-models`, inspecionada em 29/10/2026, SHA `31b9b85d4d7a3994f4740776e54ff72bccd7da44`:
https://github.com/OpenRouterTeam/skills/blob/main/skills/openrouter-models/SKILL.md

- Catálogo: https://openrouter.ai/docs/api/api-reference/models/get-models
- Provedores/filtros: https://openrouter.ai/docs/guides/routing/provider-selection
- Chat: https://openrouter.ai/docs/api/api-reference/chat/create-a-chat-completion
- Uso/custo: https://openrouter.ai/support

`GET https://openrouter.ai/api/v1/models` é público. `pricing.prompt`/`completion` são USD por token; multiplicar por 1.000.000 para preço por milhão. Confirmar `structured_outputs`.

`POST https://openrouter.ai/api/v1/chat/completions` requer Bearer token. Selecionar candidato econômico exato, ordenar provedores por preço, exigir parâmetros, `data_collection=deny` e `zdr=true`. `provider.max_price` aceita USD por milhão para prompt/completion e por chamada para request. Falhar se não houver provedor compatível.

Solicitar JSON Schema e `usage.include=true`. Registrar `usage.cost` com null quando desconhecido. Não confundir catálogo, estimativa e cobrança real.

Durante instalação, catálogo respondeu com sucesso; geração autenticada não foi testada porque não havia chave configurada. Catálogo não garante disponibilidade de provedor com todos os filtros nem qualidade das respostas.
