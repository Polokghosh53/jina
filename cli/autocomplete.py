def _update_autocomplete():
    from jina.parsers import get_main_parser

    def _gaa(key, parser):
        _result = {}
        _compl = []
        for v in parser._actions:
            if v.option_strings:
                _compl.extend(v.option_strings)
            elif v.choices:
                _compl.extend(v.choices)
                for kk, vv in v.choices.items():
                    _result.update(_gaa(" ".join([key, kk]).strip(), vv))
        # filer out single dash, as they serve as abbrev
        _compl = [k for k in _compl if (not k.startswith("-") or k.startswith("--"))]
        _result.update({key: _compl})
        return _result

    compl = _gaa("", get_main_parser())
    cmd = compl.pop("")
    compl = {"commands": cmd, "completions": compl}

    with open(__file__, "a") as fp:
        fp.write(f"\nac_table = {compl}\n")


if __name__ == "__main__":
    _update_autocomplete()

ac_table = {
    'commands': ['--help', '--version', '--version-full', 'hello', 'exec', 'flow', 'ping', 'gateway', 'pea', 'client',
                 'export-api', 'pod'], 'completions': {
        'hello fashion': ['--help', '--workdir', '--download-proxy', '--index-data-url', '--index-labels-url',
                          '--index-request-size', '--query-data-url', '--query-labels-url', '--query-request-size',
                          '--num-query', '--top-k'],
        'hello chatbot': ['--help', '--workdir', '--download-proxy', '--index-data-url', '--port-expose', '--parallel',
                          '--unblock-query-flow'],
        'hello multimodal': ['--help', '--workdir', '--download-proxy', '--uses', '--index-data-url', '--demo-url',
                             '--port-expose', '--unblock-query-flow'],
        'hello': ['--help', 'fashion', 'chatbot', 'multimodal'],
        'exec': ['--help', '--name', '--description', '--workspace', '--log-config', '--quiet', '--quiet-error',
                 '--identity', '--port-ctrl', '--ctrl-with-ipc', '--timeout-ctrl', '--ssh-server', '--ssh-keyfile',
                 '--ssh-password', '--uses', '--py-modules', '--port-in', '--port-out', '--host-in', '--host-out',
                 '--socket-in', '--socket-out', '--load-interval', '--dump-interval', '--read-only', '--memory-hwm',
                 '--on-error-strategy', '--num-part', '--uses-internal', '--entrypoint', '--docker-kwargs',
                 '--pull-latest', '--volumes', '--host', '--port-expose', '--quiet-remote-logs', '--upload-files',
                 '--workspace-id', '--daemon', '--runtime-backend', '--runtime', '--runtime-cls', '--timeout-ready',
                 '--env', '--expose-public', '--pea-id', '--pea-role', '--noblock-on-start', '--uses-before',
                 '--uses-after', '--parallel', '--shards', '--replicas', '--polling', '--scheduling', '--pod-role',
                 '--peas-hosts'],
        'flow': ['--help', '--name', '--description', '--workspace', '--log-config', '--quiet', '--quiet-error',
                 '--identity', '--uses', '--inspect'], 'ping': ['--help', '--timeout', '--retries', '--print-response'],
        'gateway': ['--help', '--name', '--description', '--workspace', '--log-config', '--quiet', '--quiet-error',
                    '--identity', '--port-ctrl', '--ctrl-with-ipc', '--timeout-ctrl', '--ssh-server', '--ssh-keyfile',
                    '--ssh-password', '--uses', '--py-modules', '--port-in', '--port-out', '--host-in', '--host-out',
                    '--socket-in', '--socket-out', '--load-interval', '--dump-interval', '--read-only', '--memory-hwm',
                    '--on-error-strategy', '--num-part', '--max-message-size', '--proxy', '--prefetch',
                    '--prefetch-on-recv', '--restful', '--rest-api', '--compress', '--compress-min-bytes',
                    '--compress-min-ratio', '--host', '--port-expose', '--daemon', '--runtime-backend', '--runtime',
                    '--runtime-cls', '--timeout-ready', '--env', '--expose-public', '--pea-id', '--pea-role',
                    '--noblock-on-start'],
        'pea': ['--help', '--name', '--description', '--workspace', '--log-config', '--quiet', '--quiet-error',
                '--identity', '--port-ctrl', '--ctrl-with-ipc', '--timeout-ctrl', '--ssh-server', '--ssh-keyfile',
                '--ssh-password', '--uses', '--py-modules', '--port-in', '--port-out', '--host-in', '--host-out',
                '--socket-in', '--socket-out', '--load-interval', '--dump-interval', '--read-only', '--memory-hwm',
                '--on-error-strategy', '--num-part', '--uses-internal', '--entrypoint', '--docker-kwargs',
                '--pull-latest', '--volumes', '--host', '--port-expose', '--quiet-remote-logs', '--upload-files',
                '--workspace-id', '--daemon', '--runtime-backend', '--runtime', '--runtime-cls', '--timeout-ready',
                '--env', '--expose-public', '--pea-id', '--pea-role', '--noblock-on-start'],
        'client': ['--help', '--request-size', '--mode', '--top-k', '--mime-type', '--continue-on-error',
                   '--return-results', '--max-message-size', '--proxy', '--prefetch', '--prefetch-on-recv', '--restful',
                   '--rest-api', '--compress', '--compress-min-bytes', '--compress-min-ratio', '--host',
                   '--port-expose'], 'export-api': ['--help', '--yaml-path', '--json-path', '--schema-path'],
        'pod': ['--help', '--name', '--description', '--workspace', '--log-config', '--quiet', '--quiet-error',
                '--identity', '--port-ctrl', '--ctrl-with-ipc', '--timeout-ctrl', '--ssh-server', '--ssh-keyfile',
                '--ssh-password', '--uses', '--py-modules', '--port-in', '--port-out', '--host-in', '--host-out',
                '--socket-in', '--socket-out', '--load-interval', '--dump-interval', '--read-only', '--memory-hwm',
                '--on-error-strategy', '--num-part', '--uses-internal', '--entrypoint', '--docker-kwargs',
                '--pull-latest', '--volumes', '--host', '--port-expose', '--quiet-remote-logs', '--upload-files',
                '--workspace-id', '--daemon', '--runtime-backend', '--runtime', '--runtime-cls', '--timeout-ready',
                '--env', '--expose-public', '--pea-id', '--pea-role', '--noblock-on-start', '--uses-before',
                '--uses-after', '--parallel', '--shards', '--replicas', '--polling', '--scheduling', '--pod-role',
                '--peas-hosts']}}
