import dotenv

dotenv.load_dotenv()

import os

stripe_secret_key = os.environ.get("SIGNING_SECRET")