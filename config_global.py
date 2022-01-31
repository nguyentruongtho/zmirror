import os

# #####################################################
# ################## BASIC Settings ###################
# #####################################################

# ############## Local Domain Settings ##############
# Your domain name, eg: 'blah.foobar.com'
my_host_name = os.environ.get('CURRENT_DOMAIN', 'herokuapp.com')
my_host_scheme = os.environ.get('CURRENT_SCHEME', 'https://')
target_domain = os.environ.get('TARGET_DOMAIN', 'www.movieboxpro.app')
target_scheme = os.environ.get('TARGET_SCHEME', 'https://')
external_domains = tuple(x for x in os.environ.get('EXTERNAL_DOMAINS', '').split('|') if x != '')
force_https_domains = os.environ.get('FORCE_HTTPS_DOMAIN', 'NONE')

enable_automatic_domains_whitelist = True
domains_whitelist_auto_add_glob_list = tuple(
    x for x in os.environ.get('DOMAIN_WHITELIST_AAGL', '').split('|') if x != '')

verbose_level = int(os.environ.get('VERBOSE_LEVEL', '0'))
domains_alias_to_target_domain = os.environ.get('TARGET_DOMAIN_ALIASES').split('|') if 'TARGET_DOMAIN_ALIASES' in os.environ else []

url_custom_redirect_enable = os.environ.get('URL_CUSTOM_REDIRECT') is not None
plain_replace_domain_alias = [tuple(x.split('/')) for x in os.environ.get('PLAIN_REPLACE_DOMAIN_ALIAS', '').split('|')
                              if x != '']

human_ip_verification_description = r"""
This site ONLY allows limited people to access, please answer the following question(s).
"""

human_ip_verification_title = 'This site is only available for our members'
human_ip_verification_answers_hash_str = 'aQQ5gCrbkHY9Zoo6oM'

human_ip_verification_identity_record = tuple(
    tuple(x.split('#')) for x in os.environ.get('HUMAN_IP_VERIFICATION_IDENTITY_RECORD', '').split('|') if x != ''
)
human_ip_verification_questions = tuple(
    tuple(x.split('#')) for x in os.environ.get('HUMAN_IP_VERIFICATION_QUESTIONS', '').split('|') if x != ''
)
if not human_ip_verification_questions and 'DEFAULT_VERIFICATION_ANSWER' in os.environ:
    human_ip_verification_questions = (
        ("What is my first child's birthday?", os.environ['DEFAULT_VERIFICATION_ANSWER'], 'ddmmyyyy',),
    )

human_ip_verification_enabled = True if human_ip_verification_questions or human_ip_verification_identity_record else False

developer_do_not_verify_ssl = True
