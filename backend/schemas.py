# Application configuration constants
APP_TYPE = "data_agent"
TIME_STEP = 0.035
TIMEOUT_SECONDS = 90
STREAM_BLOCK_TYPES = ["image", "echarts"]
STREAM_TOKEN_TYPES = ["tool", "transition", "execution_result", "error", "kaggle_search", "kaggle_connect", "plain"]
EXECUTION_RESULT_MAX_TOKENS = 1000

HEARTBEAT_INTERVAL = 10

# HTTP error codes
UNAUTH = 401
UNFOUND = 404
OVERLOAD = 503
INTERNAL = 500
UNSUPPORTED = 403

# Language models requiring continuation prompts
NEED_CONTINUE_MODEL = {"claude-v1", "claude-2"}
DEFAULT_USER_ID = "DefaultUser"

