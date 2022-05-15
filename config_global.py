import os

# ############# New Features ##################
static_path = 'static'
static_url_path = os.path.join('_s', '')

custom_inject_content = {
    "head_first": [],
    "head_last": [],
}

all_injection_plugins = {
    'BLOCK_POPUP': {
        'head_first': [{
            "content": r'''
            <script type="text/javascript" src="/_s/popupblocker/installation.js"></script>
            <script type="text/javascript" src="https://userscripts.adtidy.org/release/popup-blocker/2.5/popupblocker.user.js"></script>''',
            "url_regex": None,
        }]
    },
    'XHR_MIRROR': {
        'head_first': [{
            "content": r'''<script type="text/javascript"">
(function() {
  const open = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method, url, ...rest) {
    if (!url.includes(window.location.host)) {
        var prepend = window.location.protocol + "//" + window.location.host + "/extdomains/";
        url = url.replace("https://", prepend);
        url = url.replace("http://", prepend);
        console.log(url);
    }
    return open.call(this, method, url, ...rest);
  };
})();
            </script>''',
            "url_regex": None,
        }]
    }
}

injection_plugins = [all_injection_plugins[x] for x in os.environ.get('INJECTION_PLUGINS', '').split(',')
                     if x in all_injection_plugins]
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
domains_whitelist_auto_remove_glob_list = tuple(
    x for x in os.environ.get('DOMAIN_WHITELIST_ARGL', '').split('|') if x != '')
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
headers_to_cache = []
