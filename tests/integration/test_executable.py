import json
from request import request_bytes

def test_executable_invalid_json_without_brackets(subtests):
    data_maps = [
        {
            'input': r'"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a": 4, "b": 7}}}',
            'output': {"auth_token": "Unknown", "id": "Unknown", 'data': [], 'error': 'trailing characters at line 1 column 13', 'query': r'"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a": 4, "b": 7}}}'},
        },
        {
            'input': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a": 4, "b": 7}}',
            'output': {"auth_token": "Unknown", "id": "Unknown", 'data': [], 'error': 'EOF while parsing an object at line 1 column 105', 'query': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a": 4, "b": 7}}'},
        },
        {
            'input': r'"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a": 4, "b": 7}}',
            'output': {"auth_token": "Unknown", "id": "Unknown", 'data': [], 'error': 'trailing characters at line 1 column 13', 'query': r'"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a": 4, "b": 7}}'},
        },
    ]
    for i, entry in enumerate(data_maps):
        with subtests.test(msg=f'item {i}'):
            data_bytes = bytes(entry['input'], encoding='utf8')
            received = request_bytes(data_bytes)
            received_json = json.loads(received)
            output = entry['output']
            assert received_json['auth_token'] == output['auth_token']
            assert received_json['id'] == output['id']
            assert received_json['data'] == output['data']
            assert (len(received_json['error']) > 0) == (len(output['error']) > 0)
            assert received_json['query'] == output['query']

def test_executable_invalid_json_cut():
    input = r'{"auth_token":"123zxy456!@#","id":"123","executable":{"nam'
    output = {"auth_token": "Unknown", "id": "Unknown", 'data': [], 'error': 'EOF while parsing a string at line 1 column 58', 'query': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"nam'}
    data_bytes = bytes(input, encoding='utf8')
    received = request_bytes(data_bytes)
    received_json = json.loads(received)
    assert received_json['auth_token'] == output['auth_token']
    assert received_json['id'] == output['id']
    assert received_json['data'] == output['data']
    assert (len(received_json['error']) > 0) == (len(output['error']) > 0)
    assert received_json['query'] == output['query']

def test_executable_invalid_key(subtests):
    data_maps = [
        {
            'input': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a":4,"b@@@":7}}}',
            'output': {"auth_token": "123zxy456!@#", "id": "123", 'data': [], 'error': 'Executable param \'b\' not found', 'query': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a": 4,"b@@@":7}}}'},
        },
        {
            'input': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a@@@":4,"b":7}}}',
            'output': {"auth_token": "123zxy456!@#", "id": "123", 'data': [], 'error': 'Executable param \'a\' not found', 'query': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params":{"a@@@":4,"b":7}}}'},
        },
        {
            'input': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params@@@":{"a":4,"b":7}}}',
            'output': {"auth_token": "123zxy456!@#", "id": "123", 'data': [], 'error': '[ApiQueryExecutable.fromJson] field \'params\' of type Map not found', 'query': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"executable-test","params@@@":{"a":4,"b":7}}}'},
        },
        {
            'input': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name@@@":"executable-test","params":{"a":4,"b":7}}}',
            'output': {"auth_token": "123zxy456!@#", "id": "123", 'data': [], 'error': '[ApiQueryExecutable.fromJson] field \'name\' of type String not found', 'query': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name@@@":"executable-test","params":{"a":4,"b":7}}}'},
        },
    ]
    for i, entry in enumerate(data_maps):
        with subtests.test(msg=f'item {i}'):
            data_map = entry['input']
            output = entry['output'] 
            data_bytes = bytes(data_map, encoding='utf8')
            received = request_bytes(data_bytes)
            received_json = json.loads(received)
            output = entry['output']
            assert received_json['auth_token'] == output['auth_token']
            assert received_json['id'] == output['id']
            assert received_json['data'] == output['data']
            assert (len(received_json['error']) > 0) == (len(output['error']) > 0)
            assert received_json['query'] == output['query']

def test_executable_known_service_with_name_of_another_service(subtests):
    data_maps = [
        {
            'input': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"py-test","params":{"a": 4, "b": 7}}}',
            'output': {"auth_token": "123zxy456!@#", "id": "123", 'data': [], 'error': 'ApiServer.build | Error: Executable service with the name \'py-test\' can\'t be found', 'query': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"py-test","params":{"a": 4, "b": 7}}}'},
        },
        {
            'input': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"database","params":{"a": 4, "b": 7}}}',
            'output': {"auth_token": "123zxy456!@#", "id": "123", 'data': [], 'error': 'ApiServer.build | Error: Executable service with the name \'database\' can\'t be found', 'query': r'{"auth_token":"123zxy456!@#","id":"123","executable":{"name":"database,"params":{"a": 4, "b": 7}}}'},
        },
    ]
    for i, entry in enumerate(data_maps):
        with subtests.test(msg=f'item {i}'):
            data_bytes = bytes(entry['input'], encoding='utf-8')
            received = request_bytes(data_bytes)
            received_json = json.loads(received)
            output = entry['output']
            assert received_json['auth_token'] == output['auth_token']
            assert received_json['id'] == output['id']
            assert received_json['data'] == output['data']
            assert (len(received_json['error']) > 0) == (len(output['error']) > 0)
            assert received_json['query'] == output['query']