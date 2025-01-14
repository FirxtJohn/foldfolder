CLICK_CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], 
                        max_content_width=120,
                        auto_envvar_prefix="FOLDER_ORG",
                        allow_extra_args=True,
                        token_normalize_func=lambda x: x.lower(),
                        )

import logging

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s - %(levelname)s - %(message)s'
)