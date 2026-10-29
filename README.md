# OpenRouter — Economia Pizza Pizza

Habilidade instalada para preparar rascunhos econômicos de avaliações em lotes de até cinco comentários. A redação pode usar a API OpenRouter; leitura e publicação continuam pelo Chrome conectado. Esta integração não troca o modelo do ChatGPT/Work nem mede seu custo.

## Estado validado

- Catálogo público consultado com sucesso em 29/10/2026.
- Nove testes locais aprovados e dry-run sintético validado.
- Geração autenticada pendente de chave OpenRouter e teste real.
- Nenhum segredo ou comentário de cliente real está neste repositório.

## Ativar teste pelo GitHub

1. Em OpenRouter, preparar uma chave com limite de créditos apropriado. Não enviar a chave em conversa nem criar arquivo com o valor.
2. Neste repositório: Settings → Secrets and variables → Actions → New repository secret.
3. Nome: `OPENROUTER_API_KEY`; valor: sua chave.
4. Actions → Validar OpenRouter → Run workflow. O padrão `paid_test=false` executa testes e simulação. Para um único lote sintético autenticado, marcar `paid_test=true`.

O teste autenticado tem verificação conservadora de orçamento de US$ 0,01 antes da chamada. Isso não substitui um teto de créditos na chave. `usage.cost` é o custo informado pela API e pode ser desconhecido; a estimativa de dry-run não é cobrança real. Não há repetição automática de chamadas pagas. O teste não responde clientes no iFood.

## Uso local

Python 3 sem bibliotecas extras. Configurar `OPENROUTER_API_KEY` no ambiente seguro do executor. Um secret de Actions fica disponível somente ao workflow, não automaticamente à sessão do ChatGPT.

```bash
python3 .github/skills/economizar-openrouter-pizza-pizza/scripts/router.py status
python3 .github/skills/economizar-openrouter-pizza-pizza/scripts/router.py models
python3 .github/skills/economizar-openrouter-pizza-pizza/scripts/router.py draft --input examples/avaliacoes_sinteticas.json --output previa.json --dry-run
```

Após configurar a chave e autorizar o uso pago, usar uma saída nova e `--execute --budget-usd 0.01`. Rever cada rascunho antes de publicar pelo fluxo autorizado do Chrome. Não colocar entradas reais, saídas, recibos ou segredos no repositório.

## Origem

Implementação própria baseada no contrato oficial da API e na habilidade [openrouter-models](https://github.com/OpenRouterTeam/skills/blob/main/skills/openrouter-models/SKILL.md). Fontes e limites estão em [.github/skills/economizar-openrouter-pizza-pizza/references/openrouter.md](.github/skills/economizar-openrouter-pizza-pizza/references/openrouter.md).
