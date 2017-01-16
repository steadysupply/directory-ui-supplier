import json

import jsonschema


def parse_sector_links(raw):
    # http://jsonschema.net/
    sectors = [
        'CREATIVE_AND_MEDIA',
        'HEALTHCARE_AND_MEDICAL',
        'FOOD_AND_DRINK',
        'SOFTWARE_AND_COMPUTER_SERVICES',
    ]
    sector_schema = {
        'type': 'object',
        'properties': {
            'company_one': {'type': 'string'},
            'company_two': {'type': 'string'},
            'case_study': {'type': 'string'}
        },
        'required': ['company_one', 'company_two', 'case_study'],
    }
    parsed = json.loads(raw)
    # side effect: raises ValidationError if `raw` was not expected schema
    jsonschema.validate(parsed, {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {sector: sector_schema for sector in sectors},
        'required': sectors,
    })
    return parsed