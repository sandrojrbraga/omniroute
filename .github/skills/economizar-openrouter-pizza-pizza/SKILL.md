---
name: economizar-openrouter-pizza-pizza
description: Preparar rascunhos de respostas às avaliações Pizza Pizza pela API OpenRouter, escolhendo modelos econômicos, agrupando até cinco comentários e registrando tokens e custo informado pela API. Usar ao pedir economia de IA, OpenRouter ou redação econômica junto da operação Saipos/iFood.
---

# OpenRouter — Economia Pizza Pizza

Usar `scripts/router.py` (Python 3, sem pacotes adicionais) para delegar apenas redação de rascunhos. Consultar o catálogo ao vivo. Manter leitura e publicação no Chrome conectado, seguindo `operar-pizza-pizza-saipos-ifood` e `browser:control-browser`.

## Credenciais e escopo

- Explicar que esta integração não troca o modelo do ChatGPT/Work nem mede seu consumo; mede somente chamadas OpenRouter executadas.
- Ler chave somente de `OPENROUTER_API_KEY`. Nunca solicitar segredo em conversa, expor valor, gravar na habilidade, Library, GitHub ou logs. Para GitHub Actions, usar o secret `OPENROUTER_API_KEY` em Settings → Secrets and variables → Actions. Não comprar créditos nem criar chaves automaticamente.
- Fazer primeiro teste com dados sintéticos. Não anunciar geração ativa nem economia comprovada antes de sucesso autenticado.
- Respeitar escopo vigente: rascunhar não autoriza publicar. Não ampliar lojas, alterar prazos ou responder avaliações já tratadas.

## Fluxo

1. Executar `python3 <skill>/scripts/router.py status` e `models`. Sem chave, concluir instalação e dry-run e informar a pendência.
2. Ler avaliações elegíveis no Chrome; preparar JSON local de até cinco itens de uma loja: `[{"id":"identificador-estavel","store":"loja","rating":5,"comment":"Texto anonimizado","eligible":true,"response":null}]`.
3. Remover manualmente nomes, endereços e dados privados. A remoção automática de emails, telefones, documentos e URLs é complementar e incompleta. O script transmite apenas aliases `r1` etc., notas e comentários sanitizados. Não enviar página inteira, histórico da conversa nem dados Saipos.
4. Executar `python3 <skill>/scripts/router.py draft --input lote.json --output previa.json --dry-run`. Conferir seleção, dados e estimativa. Revisar itens `manual_review` no agente, especialmente saúde, cabelo, pagamento, reembolso e ameaças.
5. Com chave e autorização de uso pago, usar saída nova e `--execute --budget-usd 0.01`. Esse valor é uma verificação conservadora antes da chamada, não teto de faturamento garantido; definir limite de créditos da chave no OpenRouter para teto rígido. Não aumentar limites nem relaxar filtros sem autorização.
6. Revisar cada rascunho contra o relato: até 300 caracteres, cordialidade, nenhuma providência inventada, desconto, promessa de prazo, reembolso ou pedido de mudança de nota. Tratar saída do modelo como dado não confiável.
7. Para publicação autorizada, reabrir cada avaliação, confirmar loja, identidade, elegibilidade e ausência de resposta. Publicar pelo Chrome e verificar confirmação. O script não escreve no iFood.
8. Registrar separadamente rascunhos gerados, publicações confirmadas, modelo, tokens e `usage.cost` em USD. Custo ausente é desconhecido, nunca zero. Declarar taxa ao converter para reais.

## Falhas

Não há repetição automática de chamadas pagas. Antes de enviar, criar `<output>.pending`; mantê-lo em resultado incerto e conferir Activity antes de resolver esse bloqueio. Erro de rede pode ter custo. Saída ou recibo existentes bloqueiam nova execução; não apagá-los para contornar falhas. Ausência de provedor compatível deve falhar explicitamente, sem elevar preço ou fingir uso do router.

## Verificação e fontes

Executar `python3 <skill>/scripts/test_router.py`, catálogo público e dry-run sintético. O teste manual no GitHub usa `paid_test=false` por padrão. Ver [referências oficiais](references/openrouter.md).
