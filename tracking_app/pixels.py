import ptrack
class CustomTrackingPixel(ptrack.TrackingPixel):
    def record(self, request, *args, **kwargs):
        log.info(request.META['HTTP_USER_AGENT'])
        for arg in args:
            log.info(arg)
        for key, value in kwargs:
            if key == "testemail1":
                log.info("Recorded test email")
            else:
                log.info(key + ":" + value)

ptrack.tracker.register(CustomTrackingPixel)