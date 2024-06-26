from nexong.api.Terms.views import *
from .Event.views import *
from rest_framework.routers import DefaultRouter
from .CenterExit.views import *
from .Student.views import *
from .Suggestion.views import *
from .Authentication.views import *
from .Meeting.views import *
from .Event.views import *
from .Lesson.views import *
from .Donation.views import *
from .Evaluation.views import *
from .PunctualDonation.views import *
from .HomeDocument.views import *
from .Schedule.views import *
from .PunctualDonationByCard.views import *

router_api = DefaultRouter()
router_api.register(prefix="user", viewset=UserApiViewSet, basename="user")
router_api.register(prefix="meeting", viewset=MeetingApiViewSet, basename="meeting")
router_api.register(prefix="event", viewset=EventApiViewSet, basename="event")
router_api.register(prefix="lesson", viewset=LessonApiViewSet, basename="lesson")
router_api.register(
    prefix="lesson-attendance",
    viewset=LessonAttendanceApiViewSet,
    basename="lessonattendance",
)
router_api.register(prefix="donation", viewset=DonationApiViewSet, basename="donation")
router_api.register(
    prefix="volunteer", viewset=VolunteerApiViewSet, basename="volunteer"
)
router_api.register(
    prefix="lesson-event", viewset=LessonEventApiViewSet, basename="lessonevent"
)
router_api.register(prefix="student", viewset=StudentApiViewSet, basename="student")
router_api.register(
    prefix="center-exit", viewset=CenterExitApiViewSet, basename="centerexit"
)
router_api.register(
    prefix="student-evaluation",
    viewset=StudentEvaluationApiViewSet,
    basename="studentevaluation",
)
router_api.register(
    prefix="evaluation-type",
    viewset=EvaluationTypeApiViewSet,
    basename="evaluationtype",
)
router_api.register(prefix="educator", viewset=EducatorApiViewSet, basename="educator")
router_api.register(prefix="partner", viewset=PartnerApiViewSet, basename="partner")
router_api.register(prefix="family", viewset=FamilyApiViewSet, basename="family")
router_api.register(
    prefix="punctual-donation",
    viewset=PunctualDonationApiViewSet,
    basename="punctualdonation",
)
router_api.register(
    prefix="punctual-donation-by-card",
    viewset=PunctualDonationByCardApiViewSet,
    basename="punctualdonationbycard-list",
)
router_api.register(
    prefix="home-document", viewset=HomeDocumentApiViewSet, basename="homedocument"
)
router_api.register(
    prefix="education-center",
    viewset=EducationCenterApiViewSet,
    basename="educationcenter",
)
router_api.register(
    prefix="quarter-marks",
    viewset=QuarterMarksApiViewSet,
    basename="quartermarks",
)
router_api.register(
    prefix="suggestion", viewset=SuggestionApiViewSet, basename="suggestion"
)
router_api.register(prefix="schedule", viewset=ScheduleApiViewSet, basename="schedule")
router_api.register(prefix="terms", viewset=TermsApiViewSet, basename="terms")
