
class CheckRecaptchaMixin(AccessMixin):

    error_message = 'Invalid reCAPTCHA. Please try again.'
    not_activated_redirect = ''
    def get_error_message(self):
        return self.error_message

    def dispatch(self,request, *args, **kwargs):

        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False

        return super(CheckRecaptchaMixin, self).dispatch(request,*args, **kwargs)

    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        if self.request.method == 'POST' and form.is_valid():
            if not self.request.recaptcha_is_valid:
                form.add_error(None,self.get_error_message())
        return form
