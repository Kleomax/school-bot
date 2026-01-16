from .admin.admin_qtn import router as AdminQuestions_router
from .admin.block_users import router as BlockUsers_router
from .admin.channel_mailing import router as ChannelMailing_router
from .admin.mailing import router as InBotMailing_router
from .admin.statistics import router as Statistics_router

from .admin.themes.all_theme import router as AllThemes_router
# from .admin.themes.director import router as DirectorTheme_router
# from .admin.themes.dnevnik_ru import router as DnevnikTheme_router
# from .admin.themes.education import router as EducationTheme_router
# from .admin.themes.studying import router as StudyingTheme_router

from .user.user_qtn import router as UserQuestions_router
from .user.active_users import router as ActivityUsers_router

from .change_data_btns import router as ChangeDataBtns_router
from .change_data_functions import router as ChangeDataFunctions_router
from .exam_info import router as ExamInfo_router
from .get_schedule import router as Schedule_router
from .homework_helper import router as HomeworkHelper_router
from .send_ideas import router as Ideas_router
from .maintenance import regular_router as Maintenance_router
from .any_message import router as AnyMessage_router 