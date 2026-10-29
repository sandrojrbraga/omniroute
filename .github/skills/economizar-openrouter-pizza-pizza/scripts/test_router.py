#!/usr/bin/env python3
"""Offline safeguards and contract tests. No paid API calls."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import router

ROW = {'id': 'sample-review-1', 'store': 'Loja de teste', 'rating': 5,
       'comment': 'Pizza gostosa e chegou quentinha.', 'eligible': True, 'response': None}
CATALOG = {'data': [{'id': router.CANDIDATES[0], 'pricing': {'prompt': '0.0000001', 'completion': '0.0000004'},
                     'supported_parameters': ['structured_outputs']}]}


class RouterTests(unittest.TestCase):
    def test_anonymization_and_alias(self):
        wire, mapping, _ = router.prepare([{**ROW, 'comment': 'Muito boa. email teste@example.com, telefone (85) 99999-9999'}])
        text = json.dumps(wire)
        self.assertNotIn(ROW['id'], text)
        self.assertNotIn(ROW['store'], text)
        self.assertNotIn('teste@example.com', text)
        self.assertNotIn('99999', text)
        self.assertEqual(mapping['r1']['id'], ROW['id'])

    def test_ineligible_duplicate_and_cross_store(self):
        for rows in ([{**ROW, 'response': 'Obrigado'}], [{**ROW, 'eligible': False}], [ROW, ROW],
                     [ROW, {**ROW, 'id': 'other', 'store': 'Outra'}]):
            with self.subTest(rows=rows), self.assertRaises(router.RouterError):
                router.prepare(rows)

    def test_sensitive_review_stays_local(self):
        wire, _, manual = router.prepare([{**ROW, 'comment': 'Veio com cabelo.'}])
        self.assertEqual(wire, [])
        self.assertTrue(manual[0]['manual_review'])

    def test_expensive_and_unknown_models_fail(self):
        for data in ({'data': []}, {'data': [{**CATALOG['data'][0], 'pricing': {'prompt': 'NaN', 'completion': '1'}}]},
                     {'data': [{**CATALOG['data'][0], 'pricing': {'prompt': '0.01', 'completion': '0.01'}}]}):
            with self.subTest(data=data), self.assertRaises(router.RouterError):
                router.choose_model(data)

    def test_output_integrity(self):
        _, mapping, _ = router.prepare([ROW])
        for reply in ({'replies': []}, {'replies': [{'id': 'wrong', 'reply': 'Obrigado', 'manual_review': False}]},
                      {'replies': [{'id': 'r1', 'reply': 'x' * 301, 'manual_review': False}]}):
            with self.subTest(reply=reply), self.assertRaises(router.RouterError):
                router.validate_replies(reply, mapping)

    def exercise(self, argv, fake, key='test-placeholder'):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': key}), patch.object(router, 'request_json', side_effect=fake), contextlib.redirect_stdout(io.StringIO()):
            return router.main(argv)

    def test_missing_key_never_calls_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'in.json'
            source.write_text(json.dumps([ROW]))
            with patch.dict(os.environ, {'OPENROUTER_API_KEY': ''}), patch.object(router, 'request_json') as request:
                with self.assertRaises(router.RouterError):
                    router.main(['draft', '--input', str(source), '--output', str(Path(tmp)/'out.json'), '--execute', '--budget-usd', '.01'])
                request.assert_not_called()

    def test_budget_prevents_post(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp)/'in.json', Path(tmp)/'out.json'
            source.write_text(json.dumps([ROW]))
            calls = []
            def fake(path, *args):
                calls.append(path)
                return CATALOG
            with self.assertRaises(router.RouterError):
                self.exercise(['draft', '--input', str(source), '--output', str(output), '--execute', '--budget-usd', '.000001'], fake)
            self.assertEqual(calls, ['/models'])
            self.assertFalse(Path(str(output)+'.pending').exists())

    def test_receipt_unknown_cost_and_duplicate_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp)/'in.json', Path(tmp)/'out.json'
            source.write_text(json.dumps([ROW]))
            def fake(path, *args):
                if path == '/models':
                    return CATALOG
                return {'id': 'mock-generation', 'model': router.CANDIDATES[0], 'usage': {'prompt_tokens': 30, 'completion_tokens': 20},
                        'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps({'replies': [
                            {'id': 'r1', 'reply': 'Obrigado pelo carinho! 🍕', 'manual_review': False}]})}}]}
            args = ['draft', '--input', str(source), '--output', str(output), '--execute', '--budget-usd', '.01']
            self.exercise(args, fake)
            result = json.loads(output.read_text())
            self.assertIsNone(result['receipt']['cost_usd'])
            self.assertFalse(result['replies'][0]['published'])
            self.assertFalse(Path(str(output)+'.pending').exists())
            with self.assertRaises(router.RouterError):
                self.exercise(args, fake)

    def test_uncertain_call_keeps_block_and_does_not_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp)/'in.json', Path(tmp)/'out.json'
            source.write_text(json.dumps([ROW]))
            calls = []
            def fake(path, *args):
                calls.append(path)
                if path == '/models':
                    return CATALOG
                raise router.RouterError('Simulação de falha de rede')
            args = ['draft', '--input', str(source), '--output', str(output), '--execute', '--budget-usd', '.01']
            with self.assertRaises(router.RouterError):
                self.exercise(args, fake)
            self.assertEqual(calls, ['/models', '/chat/completions'])
            self.assertTrue(Path(str(output)+'.pending').exists())
            with self.assertRaises(router.RouterError):
                self.exercise(args, fake)
            self.assertEqual(len(calls), 2)


if __name__ == '__main__':
    unittest.main()
