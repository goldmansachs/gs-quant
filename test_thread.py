from concurrent.futures import ThreadPoolExecutor

def _resolve_rdates_threaded():
    rdate_entity_map = {1: [('r1', '2023-01-01'), ('r2', '2023-01-02')], 2: [('r3', '2023-01-03')]}

    with ThreadPoolExecutor() as executor:
        futures = []
        for entity_id, rules in rdate_entity_map.items():
             pass # just testing syntax

print("ok")
