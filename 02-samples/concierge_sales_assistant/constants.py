import uuid
import platform

os_type = platform.system().lower()

SESSION_ID = str(uuid.uuid4())
# SESSION_ID = os_type + str(uuid.uuid4())