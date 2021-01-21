import re
import os
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vmc.config.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from vmc.knowledge_base.documents import CveDocument
from vmc.knowledge_base import metrics

OUTPUT_FILE = os.path.join(os.getcwd(), 'input_data', 'cvss_2_3.csv')

def cvss_vector_v3(cve) -> str:
    vector = F'AV:{cve.attack_vector_v3.value}/'
    vector += F'AC:{cve.attack_complexity_v3.value}/'
    vector += F'PR:{cve.privileges_required_v3.value}/'
    vector += F'UI:{cve.user_interaction_v3.value}/'
    vector += F'S:{metrics.ScopeV3(cve.scope_v3).value}/'
    vector += F'C:{cve.confidentiality_impact_v3.value}/'
    vector += F'I:{cve.integrity_impact_v3.value}/'
    vector += F'A:{cve.availability_impact_v3.value}/'
    return vector


def cvss_vector_v2(cve) -> str:
    vector = F'AV:{cve.access_vector_v2.value}/'
    vector += F'AC:{cve.access_complexity_v2.value}/'
    vector += F'Au:{cve.authentication_v2.value}/'
    vector += F'C:{cve.confidentiality_impact_v2.value}/'
    vector += F'I:{cve.integrity_impact_v2.value}/'
    vector += F'A:{cve.availability_impact_v2.value}/'
    return vector


def civ(ci):
    if ci == metrics.ImpactV3.HIGH:
        return 2
    if ci == metrics.ImpactV3.LOW:
        return 1
    return 0


def attack_vector(attack):
    if attack == metrics.AttackVectorV3.NETWORK:
        return 3
    if attack == metrics.AttackVectorV3.ADJACENT_NETWORK:
        return 2
    if attack == metrics.AttackVectorV3.LOCAL:
        return 1
    return 0


def attack_complexity(comp):
    if comp == metrics.AttackComplexityV3.HIGH:
        return 1
    return 0


def privileges_required(pr):
    if pr == metrics.PrivilegesRequiredV3.HIGH:
        return 2
    if pr == metrics.PrivilegesRequiredV3.LOW:
        return 1
    return 0


def cwe_parse(cwe_id):
    i = cwe_id.split('-')[1]
    try:
        return int(i)/1000
    except Exception:
        return 0


def get_value(value):
    return if value else ''


def summary(d_cwe, d_cve):
    text = ' '.join([get_value(d_cwe.name),
                     get_value(d_cwe.description),
                     get_value(d_cwe.extended_description),
                     get_value(d_cve)])
    return text.translate(str.maketrans('', '', '\n\t\r')).replace('|', ' ')



if __name__ ==  'main':
    all_count =  CveDocument.search().count()
    print('All CVE count', all_count)
    search = CveDocument.search().filter('exists', field='base_score_v3')

    count = search.count()

    print('CVE with 3.1 score:', count)
    print('CVE CVSSv3/CVSSv2', count/all_count * 100)
    print('Downloading data')
    cves = [c for c in search.scan()]
    print('Downloaded data')

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        for cve in cves:
            k = '|'.join([
                    str(cve.base_score_v2),
                    str(cve.access_vector_v2.second_value),
                    str(cve.access_complexity_v2.second_value),
                    str(cve.authentication_v2.second_value),
                    str(cve.confidentiality_impact_v2.second_value),
                    str(cve.integrity_impact_v2.second_value),
                    str(cve.availability_impact_v2.second_value)])
            v = '|'.join([
                    str(attack_vector(cve.attack_vector_v3)),
                    str(attack_complexity(cve.attack_complexity_v3)),
                    str(privileges_required(cve.privileges_required_v3)),
                    str(0 if cve.scope_v3 == metrics.ScopeV3.UNCHANGED else 1),
                    str(0 if cve.user_interaction_v3 == metrics.UserInteractionV3.NONE else 1),
                    str(civ(cve.confidentiality_impact_v3)),
                    str(civ(cve.integrity_impact_v3)),
                    str(civ(cve.availability_impact_v3)),
                    str(cve.base_score_v3)
                ])
            out.write('|'.join([cve.id, summary(cve.cwe, cve.summary), k, v]))
            out.write('\n')
